# Gold Tier Setup Guide

**AI Employee System v3.0 - Full Autonomous FTE**

This guide provides step-by-step instructions for configuring and running the Gold Tier AI Employee system with all autonomous capabilities.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Architecture](#system-architecture)
3. [Installation Steps](#installation-steps)
4. [Component Configuration](#component-configuration)
5. [Running the System](#running-the-system)
6. [Testing Components](#testing-components)
7. [Troubleshooting](#troubleshooting)
8. [Security Best Practices](#security-best-practices)

---

## Prerequisites

### Required Software
- **Python 3.13+** - Main programming language
- **Node.js v24+** - For MCP servers
- **Claude Code** - AI reasoning engine
- **PM2** (optional but recommended) - Process management
- **Obsidian** (optional) - For GUI vault viewing

### Required Accounts
- **Gmail Account** - For email automation (Silver tier)
- **LinkedIn Account** - For social posting (Silver tier)
- **WhatsApp Account** - For WhatsApp monitoring (Gold tier)
- **Odoo Instance** - For accounting integration (Gold tier, optional)
- **Facebook Developer Account** - For Facebook/Instagram posting (Gold tier, optional)
- **Twitter Developer Account** - For Twitter posting (Gold tier, optional)

### System Requirements
- **OS**: Linux, macOS, or WSL2 on Windows
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 2GB free space
- **Network**: Internet connection for API calls

---

## System Architecture

### Gold Tier Components

#### Watchers (Python)
1. **filesystem_watcher.py** (Bronze) - Monitors Inbox folder
2. **gmail_watcher.py** (Silver) - Monitors Gmail inbox
3. **whatsapp_watcher.py** (Gold) - Monitors WhatsApp Web via Playwright
4. **orchestrator.py** (Silver) - Schedules and coordinates tasks
5. **error_recovery.py** (Gold) - Monitors and restarts failed processes

#### MCP Servers (Node.js)
1. **email-server** (Silver) - Sends emails via SMTP
2. **browser-server** (Gold) - Browser automation via Playwright
3. **odoo-server** (Gold) - Odoo accounting integration
4. **social-media-server** (Gold) - Facebook/Instagram/Twitter posting

#### Agent Skills
1. **vault-manager** (Bronze) - Task processing
2. **linkedin-poster** (Silver) - LinkedIn content generation
3. **weekly-auditor** (Gold) - CEO briefing generation

#### Autonomous Systems
1. **Ralph Wiggum Loop** (Gold) - Multi-iteration task completion
2. **Error Recovery** (Gold) - Self-healing system monitoring

---

## Installation Steps

### Step 1: Install Python Dependencies

```bash
# Navigate to vault directory
cd /mnt/e/all-d-files/Ai_Employee_Vault

# Install all dependencies (Bronze, Silver, and Gold)
pip install -r requirements.txt
```

This installs:
- watchdog (file monitoring)
- google-api-python-client (Gmail)
- schedule (orchestration)
- playwright (browser automation)
- beautifulsoup4 (web scraping)
- httpx (HTTP client)
- pandas (data analysis)
- python-dateutil (date utilities)

### Step 2: Install Playwright Browsers

```bash
# Install Playwright browser binaries
playwright install chromium

# Or install all browsers
playwright install
```

### Step 3: Install Node.js Dependencies

```bash
# Email MCP Server (Silver)
cd mcp-servers/email-server
npm install

# Browser MCP Server (Gold)
cd ../browser-server
npm install
npm run install-browsers  # Install Playwright browsers

# Odoo MCP Server (Gold)
cd ../odoo-server
npm install

# Social Media MCP Server (Gold)
cd ../social-media-server
npm install

# Return to vault root
cd ../..
```

### Step 4: Install PM2 (Optional but Recommended)

```bash
# Install PM2 globally
npm install -g pm2

# Verify installation
pm2 --version
```

---

## Component Configuration

### 1. Gmail Watcher (Silver Tier - Required)

**Already configured if you completed Silver Tier setup.**

If not:
1. Create Google Cloud project
2. Enable Gmail API
3. Download OAuth2 credentials
4. Save as `credentials.json` in vault root
5. Run watcher once to authenticate: `python watchers/gmail_watcher.py`
6. Follow OAuth flow in browser
7. Token saved to `token.json`

### 2. Email MCP Server (Silver Tier - Required)

**Set environment variables:**

```bash
# Gmail SMTP (recommended)
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASSWORD=your-app-password  # Get from Google Account settings

# Or add to ~/.bashrc or ~/.zshrc for persistence
echo 'export SMTP_USER=your-email@gmail.com' >> ~/.bashrc
echo 'export SMTP_PASSWORD=your-app-password' >> ~/.bashrc
source ~/.bashrc
```

**Get Gmail App Password:**
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to App Passwords
4. Generate password for "Mail"
5. Use this password for SMTP_PASSWORD

### 3. WhatsApp Watcher (Gold Tier)

**Configuration:**

The WhatsApp watcher uses Playwright to automate WhatsApp Web. On first run, you'll need to scan a QR code.

**Environment Variables:**
```bash
# Optional: Custom session path
export WHATSAPP_SESSION_PATH=/path/to/session/folder

# Dry run mode (for testing without actual WhatsApp)
export DRY_RUN=true  # Remove for production
```

**First-Time Setup:**
```bash
# Start watcher in foreground (first time only)
python watchers/whatsapp_watcher.py

# Browser will open to WhatsApp Web
# Scan QR code with your phone
# Session will be saved for future runs
# Press Ctrl+C after successful login
```

**Customizing Keywords:**

Edit `watchers/whatsapp_watcher.py` line 17:
```python
self.keywords = ['urgent', 'asap', 'emergency', 'help', 'invoice', 'payment', 'deadline']
# Add your own keywords
```

### 4. Browser MCP Server (Gold Tier)

**Environment Variables:**
```bash
# Optional configuration
export BROWSER_HEADLESS=true  # Set to false to see browser window
export VAULT_PATH=/mnt/e/all-d-files/Ai_Employee_Vault
export DRY_RUN=false  # Set to true for testing
```

**No additional setup required** - MCP server is configured via Claude Code's MCP settings.

### 5. Odoo MCP Server (Gold Tier - Optional)

**Only configure if you have an Odoo instance.**

**Environment Variables:**
```bash
export ODOO_URL=https://your-instance.odoo.com
export ODOO_DB=your-database-name
export ODOO_USERNAME=your-username
export ODOO_PASSWORD=your-password
export DRY_RUN=false  # Set to true for testing without Odoo
```

**Testing Odoo Connection:**
```bash
# Test authentication
cd mcp-servers/odoo-server
node -e "
const { OdooMCPServer } = require('./index.js');
const server = new OdooMCPServer();
server.authenticate().then(() => console.log('Success!')).catch(console.error);
"
```

### 6. Social Media MCP Server (Gold Tier - Optional)

**Facebook/Instagram Configuration:**

1. **Create Facebook App:**
   - Go to https://developers.facebook.com
   - Create new app
   - Add Facebook Login product
   - Get App ID and App Secret

2. **Get Page Access Token:**
   - Use Graph API Explorer
   - Select your app
   - Get token with permissions: `pages_manage_posts`, `instagram_basic`, `instagram_content_publish`

3. **Set Environment Variables:**
```bash
export FACEBOOK_PAGE_ACCESS_TOKEN=your-page-token
export FACEBOOK_PAGE_ID=your-page-id
export INSTAGRAM_ACCOUNT_ID=your-instagram-business-account-id
```

**Twitter/X Configuration:**

1. **Create Twitter App:**
   - Go to https://developer.twitter.com
   - Create new app
   - Get API keys

2. **Set Environment Variables:**
```bash
export TWITTER_API_KEY=your-api-key
export TWITTER_API_SECRET=your-api-secret
export TWITTER_ACCESS_TOKEN=your-access-token
export TWITTER_ACCESS_SECRET=your-access-secret
```

**Dry Run Mode (for testing):**
```bash
export DRY_RUN=true  # All posts will be simulated
```

### 7. Error Recovery System (Gold Tier)

**No configuration required** - Uses default settings.

**Optional Configuration:**

Edit `watchers/error_recovery.py` line 34-36:
```python
self.max_retries = 3  # Maximum restart attempts
self.backoff_base = 2  # Exponential backoff base (seconds)
self.max_backoff = 300  # Maximum backoff (5 minutes)
```

**Monitored Processes:**
- filesystem_watcher
- gmail_watcher
- whatsapp_watcher
- orchestrator

### 8. Ralph Wiggum Autonomous Loop (Gold Tier)

**No setup required** - Activated via stop hook.

**Configuration:**

The stop hook is located at `.claude/hooks/ralph-wiggum-stop.sh` and automatically intercepts Claude Code exit.

**How it works:**
1. You start a task in Claude Code
2. Ralph Wiggum tracks task file
3. When Claude tries to exit, hook checks if task is in Done/
4. If not done, Claude restarts automatically
5. Continues until task moves to Done/ or max iterations reached

**To disable:**
```bash
# Rename or remove hook
mv .claude/hooks/ralph-wiggum-stop.sh .claude/hooks/ralph-wiggum-stop.sh.disabled
```

### 9. Weekly Auditor Skill (Gold Tier)

**Prerequisites:**
- Business_Goals.md file exists and is up to date
- At least one completed task in Done/ folder
- Odoo MCP configured (optional but recommended)
- Social Media MCP configured (optional)

**Usage:**
```
Use the weekly-auditor skill to generate this week's business audit and CEO briefing
```

**Output Location:**
- Briefings/YYYY-MM-DD_Weekly_Audit.md

---

## Running the System

### Option 1: PM2 (Recommended for Production)

**Start all watchers:**
```bash
# From vault root directory
pm2 start watchers/filesystem_watcher.py --interpreter python3 --name fs-watcher
pm2 start watchers/gmail_watcher.py --interpreter python3 --name gmail-watcher
pm2 start watchers/whatsapp_watcher.py --interpreter python3 --name whatsapp-watcher
pm2 start watchers/orchestrator.py --interpreter python3 --name orchestrator
pm2 start watchers/error_recovery.py --interpreter python3 --name error-recovery

# Save configuration
pm2 save

# Set up startup script (optional)
pm2 startup
```

**Manage processes:**
```bash
pm2 list                    # View all processes
pm2 logs                    # View all logs
pm2 logs whatsapp-watcher   # View specific watcher
pm2 restart all             # Restart all processes
pm2 stop all                # Stop all processes
pm2 delete all              # Remove all processes
```

### Option 2: Manual Start (Good for Testing)

**Open 5 terminal windows:**

```bash
# Terminal 1: File System Watcher
cd /mnt/e/all-d-files/Ai_Employee_Vault
python watchers/filesystem_watcher.py

# Terminal 2: Gmail Watcher
cd /mnt/e/all-d-files/Ai_Employee_Vault
python watchers/gmail_watcher.py

# Terminal 3: WhatsApp Watcher
cd /mnt/e/all-d-files/Ai_Employee_Vault
python watchers/whatsapp_watcher.py

# Terminal 4: Orchestrator
cd /mnt/e/all-d-files/Ai_Employee_Vault
python watchers/orchestrator.py

# Terminal 5: Error Recovery
cd /mnt/e/all-d-files/Ai_Employee_Vault
python watchers/error_recovery.py
```

### Option 3: Background Processes (Simple)

```bash
# Start all watchers in background
cd /mnt/e/all-d-files/Ai_Employee_Vault
nohup python watchers/filesystem_watcher.py > Logs/fs_watcher.log 2>&1 &
nohup python watchers/gmail_watcher.py > Logs/gmail_watcher.log 2>&1 &
nohup python watchers/whatsapp_watcher.py > Logs/whatsapp_watcher.log 2>&1 &
nohup python watchers/orchestrator.py > Logs/orchestrator.log 2>&1 &
nohup python watchers/error_recovery.py > Logs/error_recovery.log 2>&1 &

# View logs
tail -f Logs/*.log
```

---

## Testing Components

### Test 1: File System Watcher (Bronze)

```bash
# Create test file
echo "Test task" > Inbox/test_$(date +%s).md

# Check Dashboard.md for update
# Check Needs_Action/ for new file
```

### Test 2: Gmail Watcher (Silver)

```bash
# Send yourself an email with "IMPORTANT" in subject
# Wait 2 minutes
# Check Needs_Action/ for action item
```

### Test 3: WhatsApp Watcher (Gold)

```bash
# Send yourself a WhatsApp message with keyword "urgent"
# Wait 30 seconds
# Check Needs_Action/ for new action item
```

### Test 4: Browser MCP (Gold)

Use Claude Code:
```
Use the browser MCP to navigate to https://example.com and take a screenshot
```

Expected: Screenshot saved to Screenshots/ folder

### Test 5: Odoo MCP (Gold)

Use Claude Code:
```
Use the Odoo MCP to get account balances
```

Expected: List of account balances returned

### Test 6: Social Media MCP (Gold)

Use Claude Code:
```
Use the social media MCP to generate a summary of recent Facebook posts
```

Expected: Summary of recent posts with engagement metrics

### Test 7: Weekly Auditor Skill (Gold)

Use Claude Code:
```
Use the weekly-auditor skill to generate this week's business audit
```

Expected: Briefing created in Briefings/ folder

### Test 8: Error Recovery (Gold)

```bash
# Kill a watcher process
pkill -f gmail_watcher

# Wait 60 seconds
# Check error recovery logs
cat Logs/error_recovery.log

# Process should restart automatically
```

### Test 9: Ralph Wiggum Loop (Gold)

Use Claude Code:
```
Create a file in Needs_Action/ called "multi_step_task.md" with the content:
"Research and summarize the top 3 trends in AI for 2026"

Then use Ralph Wiggum to complete this task autonomously.
```

Expected: Claude continues working until task moves to Done/

---

## Troubleshooting

### WhatsApp Watcher Issues

**Problem: QR code not appearing**
```bash
# Run with visible browser
export BROWSER_HEADLESS=false
python watchers/whatsapp_watcher.py
```

**Problem: Session expired**
```bash
# Delete session and re-authenticate
rm -rf ~/.whatsapp_session
python watchers/whatsapp_watcher.py
# Scan QR code again
```

**Problem: Messages not detected**
```bash
# Check keyword configuration
# Edit watchers/whatsapp_watcher.py line 17
# Add your keywords
```

### Browser MCP Issues

**Problem: Playwright not found**
```bash
# Install Playwright
pip install playwright
playwright install chromium
```

**Problem: Browser crashes**
```bash
# Check system resources
free -h  # Check RAM
# Reduce concurrent browser instances
```

### Odoo MCP Issues

**Problem: Authentication failed**
```bash
# Verify credentials
echo $ODOO_URL
echo $ODOO_DB
echo $ODOO_USERNAME

# Test connection
curl -X POST $ODOO_URL/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"version"},"id":1}'
```

**Problem: Odoo version incompatible**
- Odoo MCP requires Odoo 19+
- Check Odoo version: Settings > About

### Social Media MCP Issues

**Problem: Facebook token expired**
```bash
# Tokens expire after 60 days
# Get new token from Graph API Explorer
# Update FACEBOOK_PAGE_ACCESS_TOKEN
```

**Problem: Twitter rate limit**
- Twitter API has rate limits
- Wait 15 minutes and retry
- Consider upgrading Twitter API tier

### Error Recovery Issues

**Problem: Process not restarting**
```bash
# Check error recovery logs
cat Logs/error_recovery.log

# Verify process names match
cat watchers/error_recovery.py | grep "self.processes"
```

**Problem: Too many restarts**
```bash
# Check max_retries setting
# Edit watchers/error_recovery.py line 34
self.max_retries = 5  # Increase if needed
```

### Ralph Wiggum Loop Issues

**Problem: Loop not stopping**
```bash
# Ensure task file moved to Done/
# Check loop state file
cat .ralph_wiggum_loop_state.json

# Manually stop
rm .ralph_wiggum_loop_state.json
```

**Problem: Loop exiting too early**
```bash
# Check completion promise in state file
# Ensure task file name matches
```

---

## Security Best Practices

### 1. Environment Variables

**Never commit credentials to git:**
```bash
# Create .env file
cat > .env << EOF
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ODOO_URL=https://your-instance.odoo.com
ODOO_PASSWORD=your-password
FACEBOOK_PAGE_ACCESS_TOKEN=your-token
TWITTER_API_KEY=your-key
EOF

# Secure permissions
chmod 600 .env

# Add to .gitignore
echo ".env" >> .gitignore
```

**Load environment variables:**
```bash
# Add to shell startup file
echo 'export $(cat /path/to/.env | xargs)' >> ~/.bashrc
source ~/.bashrc
```

### 2. File Permissions

```bash
# Secure credentials
chmod 600 credentials.json
chmod 600 token.json
chmod 600 .env

# Secure hooks
chmod 700 .claude/hooks/ralph-wiggum-stop.sh
```

### 3. Audit Logging

**All actions are logged to:**
- Logs/filesystem_watcher.log
- Logs/gmail_watcher.log
- Logs/whatsapp_watcher.log
- Logs/orchestrator.log
- Logs/error_recovery.log
- Logs/action_log.json

**Review logs regularly:**
```bash
# View recent activity
tail -100 Logs/action_log.json | jq

# Search for errors
grep -i error Logs/*.log
```

### 4. WhatsApp Security

- WhatsApp session stored in `~/.whatsapp_session`
- Contains authentication cookies
- Secure with: `chmod 700 ~/.whatsapp_session`
- Never share session folder

### 5. MCP Server Security

- MCP servers run on stdio (no network exposure)
- Credentials passed via environment only
- No credentials stored in code
- Dry run mode available for testing

---

## Gold Tier Workflows

### Daily CEO Morning Routine (5 minutes)

1. **Check Dashboard** - `Dashboard.md` for overnight activity
2. **Process Urgent** - Review `Needs_Action/` for WhatsApp/email urgent items
3. **Approve Actions** - Move items from `Pending_Approval/` to `Approved/`
4. **Monitor Health** - Check PM2 status: `pm2 list`

### Monday Morning Workflow (15 minutes)

1. **Generate Weekly Audit** - Use weekly-auditor skill
2. **Review Briefing** - Read `Briefings/YYYY-MM-DD_Weekly_Audit.md`
3. **Update Goals** - Edit `Business_Goals.md` based on audit
4. **Plan Week** - Create action items in `Needs_Action/`
5. **Schedule Posts** - Use linkedin-poster for weekly content

### Using Ralph Wiggum for Complex Tasks

Example: Multi-step research task
```
Create a task in Needs_Action/ called "competitive_analysis.md":

"Research our top 3 competitors, analyze their pricing, features, and market positioning.
Create a comprehensive report with recommendations."

Use Ralph Wiggum to complete this autonomously.
```

Ralph Wiggum will:
1. Start working on the task
2. Iterate multiple times if needed
3. Continue even if Claude Code restarts
4. Stop only when task moves to Done/

---

## Advanced Configuration

### Custom Scheduling

Edit `watchers/orchestrator.py` to add scheduled tasks:

```python
def setup_schedules(self):
    # Monday 7 AM - Weekly audit
    schedule.every().monday.at("07:00").do(self.run_weekly_audit)

    # Add your custom schedules
    schedule.every().friday.at("17:00").do(self.run_weekly_summary)
    schedule.every().day.at("09:00").do(self.run_daily_standup)
```

### Custom Keywords for WhatsApp

Edit `watchers/whatsapp_watcher.py`:

```python
# Industry-specific keywords
self.keywords = [
    'urgent', 'asap', 'emergency',
    'invoice', 'payment', 'overdue',  # Finance
    'bug', 'critical', 'outage',      # Engineering
    'complaint', 'escalation',        # Customer service
]
```

### Custom Error Recovery Rules

Edit `watchers/error_recovery.py`:

```python
self.processes = {
    'filesystem_watcher': {
        'command': 'python3 watchers/filesystem_watcher.py',
        'critical': True,  # System stops if this fails
        'restart_on_failure': True
    },
    'whatsapp_watcher': {
        'command': 'python3 watchers/whatsapp_watcher.py',
        'critical': False,  # System continues if this fails
        'restart_on_failure': True
    },
}
```

---

## Next Steps

Now that Gold Tier is configured:

1. ✅ **Run System Tests** - Test each component
2. ✅ **Configure Credentials** - Set up all API keys
3. ✅ **Start Watchers** - Use PM2 to start all processes
4. ✅ **Monitor Logs** - Watch for errors in first 24 hours
5. ✅ **Update Business Goals** - Ensure goals are current
6. ✅ **Generate First Audit** - Run weekly-auditor skill
7. ✅ **Test Ralph Wiggum** - Try a complex multi-step task
8. ✅ **Review Security** - Verify all credentials secured

---

## Support

**Resources:**
- [Hackathon PDF](./Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.pdf)
- [Claude Code Docs](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows)
- [Panaversity Website](https://www.panaversity.org)

**Common Issues:**
- Check Logs/ folder for error details
- Review Dashboard.md for system status
- Use dry run modes for testing
- Verify environment variables are set

---

**Gold Tier Setup Complete!** 🏆

You now have a fully autonomous AI Employee with:
- ✅ Cross-domain integration (Gmail, WhatsApp, Odoo, Social Media)
- ✅ Browser automation capabilities
- ✅ Self-healing error recovery
- ✅ Autonomous task completion (Ralph Wiggum)
- ✅ Weekly business audits
- ✅ Multi-platform social media posting

**Version**: 3.0 (Gold Tier)
**Last Updated**: 2026-02-23
