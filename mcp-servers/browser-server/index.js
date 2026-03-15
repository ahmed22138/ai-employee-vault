#!/usr/bin/env node
/**
 * Browser Automation MCP Server - Gold Tier Component
 * Provides browser automation capabilities via Playwright
 */

import { chromium } from 'playwright';
import { writeFile } from 'fs/promises';
import { join } from 'path';

class BrowserMCPServer {
  constructor() {
    this.browser = null;
    this.page = null;
    this.isDryRun = process.env.DRY_RUN === 'true';
    this.vaultPath = process.env.VAULT_PATH || '/mnt/e/all-d-files/Ai_Employee_Vault';
    this.screenshotsPath = join(this.vaultPath, 'Screenshots');
  }

  async initialize() {
    console.log('[Browser MCP] Server starting...');

    if (this.isDryRun) {
      console.log('[Browser MCP] Running in DRY RUN mode - no browser will be launched');
    } else {
      try {
        // Launch browser
        this.browser = await chromium.launch({
          headless: process.env.BROWSER_HEADLESS !== 'false',
          args: ['--no-sandbox', '--disable-setuid-sandbox']
        });

        // Create new page
        this.page = await this.browser.newPage();

        console.log('[Browser MCP] Browser launched successfully');
      } catch (error) {
        console.error('[Browser MCP] Failed to launch browser:', error.message);
        throw error;
      }
    }

    console.log('[Browser MCP] Server ready');
  }

  /**
   * Navigate to a URL
   */
  async navigate(params) {
    const { url, waitUntil = 'load' } = params;

    if (!url) {
      throw new Error('URL is required');
    }

    if (this.isDryRun) {
      console.log('[Browser MCP] DRY RUN - Would navigate to:', url);
      return {
        success: true,
        dryRun: true,
        url
      };
    }

    try {
      await this.page.goto(url, { waitUntil });
      const title = await this.page.title();

      return {
        success: true,
        url,
        title,
        message: `Navigated to ${url}`
      };

    } catch (error) {
      throw new Error(`Navigation failed: ${error.message}`);
    }
  }

  /**
   * Take a screenshot
   */
  async screenshot(params) {
    const { filename, fullPage = false } = params;

    if (this.isDryRun) {
      console.log('[Browser MCP] DRY RUN - Would take screenshot:', filename);
      return {
        success: true,
        dryRun: true,
        filename
      };
    }

    try {
      const screenshotFilename = filename || `screenshot_${Date.now()}.png`;
      const filepath = join(this.screenshotsPath, screenshotFilename);

      await this.page.screenshot({
        path: filepath,
        fullPage
      });

      return {
        success: true,
        filepath,
        message: `Screenshot saved to ${filepath}`
      };

    } catch (error) {
      throw new Error(`Screenshot failed: ${error.message}`);
    }
  }

  /**
   * Click an element
   */
  async click(params) {
    const { selector } = params;

    if (!selector) {
      throw new Error('Selector is required');
    }

    if (this.isDryRun) {
      console.log('[Browser MCP] DRY RUN - Would click:', selector);
      return {
        success: true,
        dryRun: true,
        selector
      };
    }

    try {
      await this.page.click(selector);

      return {
        success: true,
        selector,
        message: `Clicked element: ${selector}`
      };

    } catch (error) {
      throw new Error(`Click failed: ${error.message}`);
    }
  }

  /**
   * Fill a form field
   */
  async fill(params) {
    const { selector, value } = params;

    if (!selector || value === undefined) {
      throw new Error('Selector and value are required');
    }

    if (this.isDryRun) {
      console.log('[Browser MCP] DRY RUN - Would fill:', selector, 'with:', value);
      return {
        success: true,
        dryRun: true,
        selector,
        value
      };
    }

    try {
      await this.page.fill(selector, String(value));

      return {
        success: true,
        selector,
        message: `Filled ${selector} with value`
      };

    } catch (error) {
      throw new Error(`Fill failed: ${error.message}`);
    }
  }

  /**
   * Extract text from page
   */
  async extractText(params) {
    const { selector } = params;

    if (this.isDryRun) {
      console.log('[Browser MCP] DRY RUN - Would extract text from:', selector);
      return {
        success: true,
        dryRun: true,
        text: 'Dry run text'
      };
    }

    try {
      let text;

      if (selector) {
        const element = await this.page.locator(selector);
        text = await element.textContent();
      } else {
        text = await this.page.textContent('body');
      }

      return {
        success: true,
        selector: selector || 'body',
        text
      };

    } catch (error) {
      throw new Error(`Text extraction failed: ${error.message}`);
    }
  }

  /**
   * Wait for element
   */
  async waitForElement(params) {
    const { selector, timeout = 30000 } = params;

    if (!selector) {
      throw new Error('Selector is required');
    }

    if (this.isDryRun) {
      console.log('[Browser MCP] DRY RUN - Would wait for:', selector);
      return {
        success: true,
        dryRun: true,
        selector
      };
    }

    try {
      await this.page.waitForSelector(selector, { timeout });

      return {
        success: true,
        selector,
        message: `Element appeared: ${selector}`
      };

    } catch (error) {
      throw new Error(`Wait failed: ${error.message}`);
    }
  }

  /**
   * Execute JavaScript on page
   */
  async evaluate(params) {
    const { script } = params;

    if (!script) {
      throw new Error('Script is required');
    }

    if (this.isDryRun) {
      console.log('[Browser MCP] DRY RUN - Would execute script:', script);
      return {
        success: true,
        dryRun: true,
        result: null
      };
    }

    try {
      const result = await this.page.evaluate(script);

      return {
        success: true,
        result,
        message: 'Script executed successfully'
      };

    } catch (error) {
      throw new Error(`Script execution failed: ${error.message}`);
    }
  }

  /**
   * Get page content
   */
  async getPageContent(params) {
    if (this.isDryRun) {
      console.log('[Browser MCP] DRY RUN - Would get page content');
      return {
        success: true,
        dryRun: true,
        content: '<html>Dry run content</html>'
      };
    }

    try {
      const content = await this.page.content();
      const url = this.page.url();
      const title = await this.page.title();

      return {
        success: true,
        url,
        title,
        content,
        contentLength: content.length
      };

    } catch (error) {
      throw new Error(`Failed to get page content: ${error.message}`);
    }
  }

  /**
   * Close browser
   */
  async closeBrowser() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
      this.page = null;
      console.log('[Browser MCP] Browser closed');
    }

    return {
      success: true,
      message: 'Browser closed'
    };
  }

  /**
   * MCP Protocol: List available tools
   */
  listTools() {
    return [
      {
        name: 'navigate',
        description: 'Navigate to a URL',
        inputSchema: {
          type: 'object',
          properties: {
            url: { type: 'string', description: 'URL to navigate to', required: true },
            waitUntil: {
              type: 'string',
              description: 'Wait condition (load, domcontentloaded, networkidle)',
              enum: ['load', 'domcontentloaded', 'networkidle']
            }
          },
          required: ['url']
        }
      },
      {
        name: 'screenshot',
        description: 'Take a screenshot of the current page',
        inputSchema: {
          type: 'object',
          properties: {
            filename: { type: 'string', description: 'Screenshot filename' },
            fullPage: { type: 'boolean', description: 'Capture full scrollable page (default: false)' }
          }
        }
      },
      {
        name: 'click',
        description: 'Click an element on the page',
        inputSchema: {
          type: 'object',
          properties: {
            selector: { type: 'string', description: 'CSS selector or text selector', required: true }
          },
          required: ['selector']
        }
      },
      {
        name: 'fill',
        description: 'Fill a form field',
        inputSchema: {
          type: 'object',
          properties: {
            selector: { type: 'string', description: 'CSS selector for input field', required: true },
            value: { type: 'string', description: 'Value to fill', required: true }
          },
          required: ['selector', 'value']
        }
      },
      {
        name: 'extract_text',
        description: 'Extract text content from page or element',
        inputSchema: {
          type: 'object',
          properties: {
            selector: { type: 'string', description: 'CSS selector (optional, defaults to body)' }
          }
        }
      },
      {
        name: 'wait_for_element',
        description: 'Wait for an element to appear',
        inputSchema: {
          type: 'object',
          properties: {
            selector: { type: 'string', description: 'CSS selector to wait for', required: true },
            timeout: { type: 'number', description: 'Timeout in milliseconds (default: 30000)' }
          },
          required: ['selector']
        }
      },
      {
        name: 'evaluate',
        description: 'Execute JavaScript on the page',
        inputSchema: {
          type: 'object',
          properties: {
            script: { type: 'string', description: 'JavaScript code to execute', required: true }
          },
          required: ['script']
        }
      },
      {
        name: 'get_page_content',
        description: 'Get the full HTML content of the current page',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      },
      {
        name: 'close_browser',
        description: 'Close the browser',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      }
    ];
  }

  /**
   * MCP Protocol: Execute a tool
   */
  async executeTool(toolName, params) {
    switch (toolName) {
      case 'navigate':
        return await this.navigate(params);

      case 'screenshot':
        return await this.screenshot(params);

      case 'click':
        return await this.click(params);

      case 'fill':
        return await this.fill(params);

      case 'extract_text':
        return await this.extractText(params);

      case 'wait_for_element':
        return await this.waitForElement(params);

      case 'evaluate':
        return await this.evaluate(params);

      case 'get_page_content':
        return await this.getPageContent(params);

      case 'close_browser':
        return await this.closeBrowser();

      default:
        throw new Error(`Unknown tool: ${toolName}`);
    }
  }

  /**
   * Start MCP server (stdio mode)
   */
  async start() {
    await this.initialize();

    console.log('[Browser MCP] Available tools:', this.listTools().map(t => t.name).join(', '));
    console.log('[Browser MCP] Listening on stdin...');

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
            const result = await this.executeTool(request.params.name, request.params.arguments || {});
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

    // Cleanup on exit
    process.on('SIGINT', async () => {
      console.log('\n[Browser MCP] Shutting down...');
      await this.closeBrowser();
      process.exit(0);
    });
  }
}

// Start server
const server = new BrowserMCPServer();
server.start().catch(error => {
  console.error('[Browser MCP] Fatal error:', error);
  process.exit(1);
});
