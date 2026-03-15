#!/usr/bin/env node
/**
 * Simple Email MCP Server - Silver Tier Component
 * Provides email sending capabilities via SMTP
 */

import nodemailer from 'nodemailer';
import { readFile } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// MCP Server Implementation
class EmailMCPServer {
  constructor() {
    this.transporter = null;
    this.config = null;
    this.isDryRun = process.env.DRY_RUN === 'true';
  }

  async initialize() {
    // Load email configuration
    this.config = {
      smtp: {
        host: process.env.SMTP_HOST || 'smtp.gmail.com',
        port: parseInt(process.env.SMTP_PORT || '587'),
        secure: process.env.SMTP_SECURE === 'true',
        auth: {
          user: process.env.SMTP_USER,
          pass: process.env.SMTP_PASSWORD
        }
      },
      from: process.env.EMAIL_FROM || process.env.SMTP_USER
    };

    // Validate configuration
    if (!this.config.smtp.auth.user || !this.config.smtp.auth.pass) {
      throw new Error('SMTP credentials not configured. Set SMTP_USER and SMTP_PASSWORD environment variables.');
    }

    // Create transporter
    this.transporter = nodemailer.createTransport(this.config.smtp);

    // Verify connection
    if (!this.isDryRun) {
      try {
        await this.transporter.verify();
        console.log('[Email MCP] SMTP connection verified successfully');
      } catch (error) {
        console.error('[Email MCP] SMTP connection failed:', error.message);
        throw error;
      }
    } else {
      console.log('[Email MCP] Running in DRY RUN mode - no emails will be sent');
    }
  }

  /**
   * Send an email
   * @param {Object} params - Email parameters
   * @param {string} params.to - Recipient email address
   * @param {string} params.subject - Email subject
   * @param {string} params.body - Email body (plain text or HTML)
   * @param {string} params.from - Sender email (optional)
   * @param {Array} params.attachments - Attachments (optional)
   * @returns {Promise<Object>} - Send result
   */
  async sendEmail(params) {
    const { to, subject, body, from, attachments = [] } = params;

    // Validate required fields
    if (!to || !subject || !body) {
      throw new Error('Missing required fields: to, subject, body');
    }

    // Email options
    const mailOptions = {
      from: from || this.config.from,
      to,
      subject,
      text: body,
      html: body.includes('<') ? body : undefined, // Auto-detect HTML
      attachments
    };

    // Dry run mode
    if (this.isDryRun) {
      console.log('[Email MCP] DRY RUN - Would send email:');
      console.log(JSON.stringify(mailOptions, null, 2));
      return {
        success: true,
        messageId: 'dry-run-' + Date.now(),
        dryRun: true
      };
    }

    // Send email
    try {
      const info = await this.transporter.sendMail(mailOptions);
      console.log('[Email MCP] Email sent successfully:', info.messageId);
      return {
        success: true,
        messageId: info.messageId,
        response: info.response
      };
    } catch (error) {
      console.error('[Email MCP] Failed to send email:', error.message);
      throw error;
    }
  }

  /**
   * Draft an email (save to file without sending)
   * @param {Object} params - Email parameters
   * @param {string} params.draftPath - Path to save draft
   * @returns {Promise<Object>} - Draft result
   */
  async draftEmail(params) {
    const { to, subject, body, draftPath } = params;

    const draftContent = `---
type: email_draft
to: ${to}
subject: ${subject}
created: ${new Date().toISOString()}
status: draft
---

## Email Draft

**To:** ${to}
**Subject:** ${subject}

**Body:**

${body}

---
*Draft created by Email MCP Server*
*To send: Move to /Approved and use send_email action*
`;

    try {
      await writeFile(draftPath, draftContent, 'utf-8');
      console.log('[Email MCP] Draft saved:', draftPath);
      return {
        success: true,
        draftPath
      };
    } catch (error) {
      console.error('[Email MCP] Failed to save draft:', error.message);
      throw error;
    }
  }

  /**
   * MCP Protocol: List available tools
   */
  listTools() {
    return [
      {
        name: 'send_email',
        description: 'Send an email via SMTP',
        inputSchema: {
          type: 'object',
          properties: {
            to: { type: 'string', description: 'Recipient email address' },
            subject: { type: 'string', description: 'Email subject' },
            body: { type: 'string', description: 'Email body (plain text or HTML)' },
            from: { type: 'string', description: 'Sender email address (optional)' },
            attachments: {
              type: 'array',
              description: 'Email attachments (optional)',
              items: {
                type: 'object',
                properties: {
                  filename: { type: 'string' },
                  path: { type: 'string' }
                }
              }
            }
          },
          required: ['to', 'subject', 'body']
        }
      },
      {
        name: 'draft_email',
        description: 'Create an email draft without sending',
        inputSchema: {
          type: 'object',
          properties: {
            to: { type: 'string', description: 'Recipient email address' },
            subject: { type: 'string', description: 'Email subject' },
            body: { type: 'string', description: 'Email body' },
            draftPath: { type: 'string', description: 'Path to save draft file' }
          },
          required: ['to', 'subject', 'body', 'draftPath']
        }
      }
    ];
  }

  /**
   * MCP Protocol: Execute a tool
   */
  async executeTool(toolName, params) {
    switch (toolName) {
      case 'send_email':
        return await this.sendEmail(params);
      case 'draft_email':
        return await this.draftEmail(params);
      default:
        throw new Error(`Unknown tool: ${toolName}`);
    }
  }

  /**
   * Start MCP server (stdio mode)
   */
  async start() {
    console.log('[Email MCP] Server starting...');
    await this.initialize();
    console.log('[Email MCP] Server ready');
    console.log('[Email MCP] Available tools:', this.listTools().map(t => t.name).join(', '));

    // MCP stdio protocol implementation
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', async (data) => {
      try {
        const request = JSON.parse(data);
        let response;

        switch (request.method) {
          case 'tools/list':
            response = { tools: this.listTools() };
            break;
          case 'tools/call':
            const result = await this.executeTool(request.params.name, request.params.arguments);
            response = { content: [{ type: 'text', text: JSON.stringify(result) }] };
            break;
          default:
            throw new Error(`Unknown method: ${request.method}`);
        }

        process.stdout.write(JSON.stringify({ id: request.id, result: response }) + '\n');
      } catch (error) {
        process.stdout.write(JSON.stringify({
          id: request?.id,
          error: { message: error.message }
        }) + '\n');
      }
    });

    console.log('[Email MCP] Listening on stdin...');
  }
}

// Start server
const server = new EmailMCPServer();
server.start().catch(error => {
  console.error('[Email MCP] Fatal error:', error);
  process.exit(1);
});
