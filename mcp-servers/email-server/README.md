# Email MCP Server

Simple Model Context Protocol (MCP) server for sending emails via SMTP.

## Features

- Send emails via SMTP (Gmail, Outlook, custom SMTP servers)
- Draft emails for approval workflow
- Dry-run mode for testing
- Attachment support
- HTML and plain text emails

## Setup

### 1. Install Dependencies

```bash
cd mcp-servers/email-server
npm install
```

### 2. Configure Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
EMAIL_FROM=your-email@gmail.com

# Optional
SMTP_HOST=smtp.gmail.com          # Default: smtp.gmail.com
SMTP_PORT=587                      # Default: 587
SMTP_SECURE=false                  # Default: false
DRY_RUN=false                      # Set to 'true' for testing
```

### 3. Gmail Setup (Recommended)

If using Gmail:

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Navigate to Security → 2-Step Verification
3. Scroll to "App passwords"
4. Generate a new app password for "Mail"
5. Use this password as `SMTP_PASSWORD`

**Never use your actual Gmail password!**

### 4. Configure in Claude Code

Add to your Claude Code MCP config (`~/.config/claude-code/mcp.json`):

```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/Ai_Employee_Vault/mcp-servers/email-server/index.js"],
      "env": {
        "SMTP_USER": "your-email@gmail.com",
        "SMTP_PASSWORD": "your-app-password",
        "EMAIL_FROM": "your-email@gmail.com"
      }
    }
  ]
}
```

## Usage

### From Claude Code

Once configured, Claude Code can use these tools:

#### Send Email
```javascript
// Claude Code will automatically call this
{
  "tool": "send_email",
  "params": {
    "to": "recipient@example.com",
    "subject": "Test Email",
    "body": "This is a test email from AI Employee"
  }
}
```

#### Draft Email
```javascript
{
  "tool": "draft_email",
  "params": {
    "to": "recipient@example.com",
    "subject": "Test Draft",
    "body": "This is a draft",
    "draftPath": "/path/to/vault/Plans/EMAIL_draft.md"
  }
}
```

### Manual Testing

Start the server manually:

```bash
cd mcp-servers/email-server
DRY_RUN=true node index.js
```

Then send a test request via stdin:

```json
{"id": 1, "method": "tools/call", "params": {"name": "send_email", "arguments": {"to": "test@example.com", "subject": "Test", "body": "Test body"}}}
```

## Security Best Practices

1. **Never commit credentials** - Use environment variables or .env files
2. **Add .env to .gitignore** immediately
3. **Use app-specific passwords** - Never use your main email password
4. **Enable dry-run mode** during testing
5. **Implement HITL approval** for production emails

## Troubleshooting

### "SMTP connection failed"

- Check SMTP credentials are correct
- Verify SMTP host and port
- Ensure less secure app access is enabled (if required)
- Check firewall/network settings

### "Invalid login"

- Use app-specific password, not your main password
- Enable 2-factor authentication on Gmail
- Generate fresh app password

### "Message not sent"

- Check recipient email is valid
- Verify SMTP quotas not exceeded
- Check spam/junk folder
- Review SMTP server logs

## Integration with AI Employee

This MCP server integrates with the HITL approval workflow:

1. AI drafts email → creates file in `/Plans/`
2. AI requests approval → moves to `/Pending_Approval/`
3. Human reviews → moves to `/Approved/`
4. Orchestrator detects approved file → calls MCP server
5. Email sent → logged in `/Logs/`

## Limitations

- Basic SMTP only (no OAuth2 yet)
- No email reading/fetching (use Gmail Watcher for that)
- No email threading/conversations
- No calendar invites or rich formatting

These are planned for Gold tier.

---

*Part of the Silver Tier AI Employee System*
