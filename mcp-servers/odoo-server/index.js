#!/usr/bin/env node
/**
 * Odoo Accounting MCP Server - Gold Tier Component
 * Provides accounting integration via Odoo's JSON-RPC API
 */

import axios from 'axios';

class OdooMCPServer {
  constructor() {
    this.config = {
      url: process.env.ODOO_URL || 'http://localhost:8069',
      db: process.env.ODOO_DB || 'odoo',
      username: process.env.ODOO_USERNAME,
      password: process.env.ODOO_PASSWORD
    };

    this.uid = null;
    this.isDryRun = process.env.DRY_RUN === 'true';
  }

  async initialize() {
    console.log('[Odoo MCP] Server starting...');

    // Validate configuration
    if (!this.config.username || !this.config.password) {
      throw new Error('ODOO_USERNAME and ODOO_PASSWORD must be set');
    }

    // Authenticate with Odoo
    if (!this.isDryRun) {
      try {
        await this.authenticate();
        console.log('[Odoo MCP] Authenticated successfully');
      } catch (error) {
        console.error('[Odoo MCP] Authentication failed:', error.message);
        throw error;
      }
    } else {
      console.log('[Odoo MCP] Running in DRY RUN mode');
    }

    console.log('[Odoo MCP] Server ready');
  }

  /**
   * Authenticate with Odoo using JSON-RPC
   */
  async authenticate() {
    const response = await axios.post(
      `${this.config.url}/jsonrpc`,
      {
        jsonrpc: '2.0',
        method: 'call',
        params: {
          service: 'common',
          method: 'authenticate',
          args: [this.config.db, this.config.username, this.config.password, {}]
        },
        id: Date.now()
      },
      {
        headers: { 'Content-Type': 'application/json' }
      }
    );

    if (response.data.error) {
      throw new Error(response.data.error.message);
    }

    this.uid = response.data.result;

    if (!this.uid) {
      throw new Error('Authentication failed: Invalid credentials');
    }

    return this.uid;
  }

  /**
   * Execute Odoo method via JSON-RPC
   */
  async execute(model, method, args = [], kwargs = {}) {
    if (this.isDryRun) {
      console.log('[Odoo MCP] DRY RUN - Would execute:', { model, method, args, kwargs });
      return { success: true, dryRun: true };
    }

    const response = await axios.post(
      `${this.config.url}/jsonrpc`,
      {
        jsonrpc: '2.0',
        method: 'call',
        params: {
          service: 'object',
          method: 'execute_kw',
          args: [
            this.config.db,
            this.uid,
            this.config.password,
            model,
            method,
            args,
            kwargs
          ]
        },
        id: Date.now()
      },
      {
        headers: { 'Content-Type': 'application/json' }
      }
    );

    if (response.data.error) {
      throw new Error(response.data.error.message);
    }

    return response.data.result;
  }

  /**
   * Get account balances
   */
  async getAccountBalances(accountIds = []) {
    const domain = accountIds.length > 0 ? [['id', 'in', accountIds]] : [];

    const accounts = await this.execute(
      'account.account',
      'search_read',
      [domain],
      {
        fields: ['code', 'name', 'balance', 'company_currency_id'],
        limit: 100
      }
    );

    return {
      success: true,
      accounts: accounts || [],
      total_count: accounts?.length || 0
    };
  }

  /**
   * Get invoices
   */
  async getInvoices(params = {}) {
    const {
      state = null,
      partner_id = null,
      date_from = null,
      date_to = null,
      limit = 50
    } = params;

    const domain = [];
    if (state) domain.push(['state', '=', state]);
    if (partner_id) domain.push(['partner_id', '=', partner_id]);
    if (date_from) domain.push(['invoice_date', '>=', date_from]);
    if (date_to) domain.push(['invoice_date', '<=', date_to]);

    const invoices = await this.execute(
      'account.move',
      'search_read',
      [domain],
      {
        fields: [
          'name', 'partner_id', 'invoice_date', 'invoice_date_due',
          'amount_total', 'amount_residual', 'state', 'move_type'
        ],
        limit
      }
    );

    return {
      success: true,
      invoices: invoices || [],
      total_count: invoices?.length || 0
    };
  }

  /**
   * Create invoice (draft only - requires approval)
   */
  async createInvoiceDraft(params) {
    const {
      partner_id,
      invoice_date,
      invoice_lines,
      move_type = 'out_invoice'
    } = params;

    // Validate required fields
    if (!partner_id || !invoice_lines || invoice_lines.length === 0) {
      throw new Error('partner_id and invoice_lines are required');
    }

    // Create invoice in draft state
    const invoice_id = await this.execute(
      'account.move',
      'create',
      [{
        partner_id,
        move_type,
        invoice_date,
        state: 'draft',
        invoice_line_ids: invoice_lines.map(line => [0, 0, {
          product_id: line.product_id,
          quantity: line.quantity,
          price_unit: line.price_unit,
          name: line.description || ''
        }])
      }]
    );

    return {
      success: true,
      invoice_id,
      message: 'Invoice draft created successfully'
    };
  }

  /**
   * Get revenue summary
   */
  async getRevenueSummary(params = {}) {
    const {
      date_from = null,
      date_to = null
    } = params;

    const domain = [
      ['move_type', '=', 'out_invoice'],
      ['state', '=', 'posted']
    ];

    if (date_from) domain.push(['invoice_date', '>=', date_from]);
    if (date_to) domain.push(['invoice_date', '<=', date_to]);

    const invoices = await this.execute(
      'account.move',
      'search_read',
      [domain],
      {
        fields: ['amount_total', 'invoice_date', 'partner_id'],
        limit: 1000
      }
    );

    const total_revenue = invoices.reduce((sum, inv) => sum + (inv.amount_total || 0), 0);
    const invoice_count = invoices.length;

    return {
      success: true,
      total_revenue,
      invoice_count,
      invoices
    };
  }

  /**
   * Get expense summary
   */
  async getExpenseSummary(params = {}) {
    const {
      date_from = null,
      date_to = null
    } = params;

    const domain = [
      ['move_type', '=', 'in_invoice'],
      ['state', '=', 'posted']
    ];

    if (date_from) domain.push(['invoice_date', '>=', date_from]);
    if (date_to) domain.push(['invoice_date', '<=', date_to]);

    const bills = await this.execute(
      'account.move',
      'search_read',
      [domain],
      {
        fields: ['amount_total', 'invoice_date', 'partner_id'],
        limit: 1000
      }
    );

    const total_expenses = bills.reduce((sum, bill) => sum + (bill.amount_total || 0), 0);
    const bill_count = bills.length;

    return {
      success: true,
      total_expenses,
      bill_count,
      bills
    };
  }

  /**
   * MCP Protocol: List available tools
   */
  listTools() {
    return [
      {
        name: 'get_account_balances',
        description: 'Get account balances from Odoo',
        inputSchema: {
          type: 'object',
          properties: {
            accountIds: {
              type: 'array',
              description: 'Optional array of account IDs to filter',
              items: { type: 'number' }
            }
          }
        }
      },
      {
        name: 'get_invoices',
        description: 'Get customer invoices',
        inputSchema: {
          type: 'object',
          properties: {
            state: { type: 'string', description: 'Invoice state (draft, posted, paid, etc.)' },
            partner_id: { type: 'number', description: 'Customer ID' },
            date_from: { type: 'string', description: 'Start date (YYYY-MM-DD)' },
            date_to: { type: 'string', description: 'End date (YYYY-MM-DD)' },
            limit: { type: 'number', description: 'Maximum number of records' }
          }
        }
      },
      {
        name: 'create_invoice_draft',
        description: 'Create invoice draft (requires approval to post)',
        inputSchema: {
          type: 'object',
          properties: {
            partner_id: { type: 'number', description: 'Customer ID', required: true },
            invoice_date: { type: 'string', description: 'Invoice date (YYYY-MM-DD)' },
            move_type: { type: 'string', description: 'Invoice type (out_invoice, out_refund)' },
            invoice_lines: {
              type: 'array',
              description: 'Invoice line items',
              items: {
                type: 'object',
                properties: {
                  product_id: { type: 'number' },
                  quantity: { type: 'number' },
                  price_unit: { type: 'number' },
                  description: { type: 'string' }
                }
              }
            }
          },
          required: ['partner_id', 'invoice_lines']
        }
      },
      {
        name: 'get_revenue_summary',
        description: 'Get revenue summary for a date range',
        inputSchema: {
          type: 'object',
          properties: {
            date_from: { type: 'string', description: 'Start date (YYYY-MM-DD)' },
            date_to: { type: 'string', description: 'End date (YYYY-MM-DD)' }
          }
        }
      },
      {
        name: 'get_expense_summary',
        description: 'Get expense summary for a date range',
        inputSchema: {
          type: 'object',
          properties: {
            date_from: { type: 'string', description: 'Start date (YYYY-MM-DD)' },
            date_to: { type: 'string', description: 'End date (YYYY-MM-DD)' }
          }
        }
      }
    ];
  }

  /**
   * MCP Protocol: Execute a tool
   */
  async executeTool(toolName, params) {
    switch (toolName) {
      case 'get_account_balances':
        return await this.getAccountBalances(params.accountIds);

      case 'get_invoices':
        return await this.getInvoices(params);

      case 'create_invoice_draft':
        return await this.createInvoiceDraft(params);

      case 'get_revenue_summary':
        return await this.getRevenueSummary(params);

      case 'get_expense_summary':
        return await this.getExpenseSummary(params);

      default:
        throw new Error(`Unknown tool: ${toolName}`);
    }
  }

  /**
   * Start MCP server (stdio mode)
   */
  async start() {
    await this.initialize();

    console.log('[Odoo MCP] Available tools:', this.listTools().map(t => t.name).join(', '));
    console.log('[Odoo MCP] Listening on stdin...');

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
  }
}

// Start server
const server = new OdooMCPServer();
server.start().catch(error => {
  console.error('[Odoo MCP] Fatal error:', error);
  process.exit(1);
});
