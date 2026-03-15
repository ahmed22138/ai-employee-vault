# AI Employee - Platinum Tier 💎

## Overview
This is a **Platinum Tier** implementation of the Personal AI Employee system from the Panaversity Hackathon. It provides a **24/7 autonomous FTE (Full-Time Employee)** with cloud-local hybrid architecture, featuring always-on cloud monitoring, secure local execution, cross-domain integration (Gmail, WhatsApp, Odoo, social media), browser automation, self-healing error recovery, and intelligent task coordination between cloud and local agents.

## Architecture (Platinum - Cloud + Local Hybrid)
- **Cloud Agent (24/7)**: Always-on email triage, vault sync, health monitoring
- **Local Agent**: Secure execution of approvals, payments, WhatsApp, final sends
- **Brain**: Claude Code (reasoning engine) + Ralph Wiggum Loop (autonomous iteration)
- **Memory**: Obsidian Vault (synced via Git between cloud and local)
- **Senses**: Multiple Watchers (File System + Gmail + WhatsApp + Error Recovery)
- **Hands**: Agent Skills + MCP Servers (Email, Browser, Odoo, Social Media)
- **Coordination**: Claim-by-Move task ownership + Orchestrator scheduling
- **Self-Healing**: Error Recovery + Cloud Health Monitoring with auto-restart
- **Security**: Secrets never sync to cloud, work-zone specialization

## Folder Structure
```
Ai_Employee_Vault/
├── Inbox/                  # Drop files here for processing
├── Needs_Action/           # Tasks requiring attention (by domain: email, social, etc.)
├── In_Progress/            # Claimed tasks (Platinum: /cloud/ and /local/ subfolders) 💎
├── Done/                   # Completed tasks
├── Updates/                # Cloud agent updates for local agent (Platinum) 💎
├── Plans/                  # AI-generated plans
│   └── LinkedIn/           # LinkedIn post drafts
├── Pending_Approval/       # Actions awaiting approval
├── Approved/               # Approved actions (ready for execution)
├── Rejected/               # Rejected actions
├── Logs/                   # System logs and action history
├── Briefings/              # Generated reports and CEO briefings
├── Accounting/             # Financial tracking
├── watchers/               # Watcher scripts (local)
│   ├── base_watcher.py     # Base class for all watchers
│   ├── filesystem_watcher.py  # File system monitor (Bronze)
│   ├── gmail_watcher.py    # Gmail monitor (Silver)
│   ├── whatsapp_watcher.py # WhatsApp monitor (Gold) 🏆
│   ├── orchestrator.py     # Scheduling coordinator (Silver)
│   ├── error_recovery.py   # Error recovery system (Gold) 🏆
│   └── ralph_wiggum.py     # Autonomous loop manager (Gold) 🏆
├── cloud-agent/            # Cloud agent (24/7 processes) - Platinum 💎
│   ├── watchers/
│   │   └── cloud_email_triage.py  # Cloud email monitoring (draft-only)
│   ├── vault_sync.py       # Git-based vault synchronization
│   ├── task_coordinator.py # Claim-by-move coordination
│   ├── health_monitor.py   # Cloud health monitoring & auto-restart
│   ├── ecosystem.config.js # PM2 process management config
│   └── deployment/         # Cloud deployment scripts
│       ├── deploy_cloud.sh # Cloud agent deployment
│       └── deploy_odoo.sh  # Odoo cloud deployment
├── local-agent/            # Local agent (secure execution) - Platinum 💎
│   └── local_approval_agent.py  # Approval handler & email sender
├── mcp-servers/            # MCP servers for external actions
│   ├── email-server/       # Email sending MCP (Silver)
│   ├── odoo-server/        # Odoo accounting MCP (Gold) 🏆
│   ├── social-media-server/ # Multi-platform social MCP (Gold) 🏆
│   └── browser-server/     # Browser automation MCP (Gold) 🏆
├── .claude/                # Claude Code configuration
│   ├── hooks/              # CLI hooks
│   │   └── ralph-wiggum-stop.sh  # Autonomous loop hook (Gold) 🏆
│   └── skills/             # Agent Skills
│       ├── vault-manager/  # Task processing (Bronze)
│       ├── linkedin-poster/  # LinkedIn automation (Silver)
│       └── weekly-auditor/ # Business audit skill (Gold) 🏆
├── Dashboard.md            # Real-time status dashboard
├── Company_Handbook.md     # Rules of engagement
├── Business_Goals.md       # Business objectives and metrics (Silver) ✨
├── SILVER_TIER_SETUP_GUIDE.md  # Setup instructions (Silver) ✨
└── README.md               # This file
```

## Features

### Bronze Tier (Foundation) ✅
- ✅ Obsidian vault with Dashboard and Company Handbook
- ✅ File system watcher for Inbox monitoring
- ✅ Claude Code integration for reading/writing vault
- ✅ Complete folder structure for task management
- ✅ Vault Manager Agent Skill
- ✅ Human-in-the-loop approval workflow
- ✅ Comprehensive audit logging

### Silver Tier (Functional Assistant) ✅
- ✅ **Gmail Watcher** - Monitors inbox for important emails with OAuth2
- ✅ **LinkedIn Poster Skill** - Generates and schedules LinkedIn posts
- ✅ **Email MCP Server** - Sends emails via SMTP for external actions
- ✅ **Orchestrator** - Scheduled task management and coordination
- ✅ **Business Goals Template** - Strategic alignment and metrics tracking
- ✅ **Enhanced HITL Workflow** - Expanded approval system for emails and posts
- ✅ **Claude Reasoning Loop** - Creates Plan.md files for complex tasks
- ✅ **Automated Scheduling** - Cron-like task scheduling built-in

### Gold Tier (Full Autonomous FTE) 🏆
- ✅ **WhatsApp Watcher** - Monitors WhatsApp Web for urgent messages with Playwright
- ✅ **Ralph Wiggum Loop** - Autonomous multi-iteration task completion
- ✅ **Browser MCP Server** - Web automation and scraping with Playwright
- ✅ **Odoo MCP Server** - Accounting integration via JSON-RPC API
- ✅ **Social Media MCP** - Cross-platform posting (Facebook, Instagram, Twitter/X)
- ✅ **Error Recovery System** - Process monitoring with graceful degradation
- ✅ **Weekly Auditor Skill** - Automated CEO briefings with financial analysis
- ✅ **Cross-Domain Integration** - Unified business operations platform

## Installation

### Prerequisites
- Python 3.13 or higher
- Node.js v24+ (for MCP servers)
- Claude Code installed
- Gmail account (for email automation)
- LinkedIn account (for social posting)
- Obsidian (optional, for GUI viewing)

### Quick Start (Gold Tier)

**For detailed setup instructions, see [GOLD_TIER_SETUP_GUIDE.md](GOLD_TIER_SETUP_GUIDE.md)**

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Install Node.js dependencies** (for all MCP servers):
```bash
# Email MCP
cd mcp-servers/email-server && npm install

# Browser MCP (Gold Tier)
cd ../browser-server && npm install && npm run install-browsers

# Odoo MCP (Gold Tier)
cd ../odoo-server && npm install

# Social Media MCP (Gold Tier)
cd ../social-media-server && npm install
```

3. **Configure Gmail API**:
   - Create Google Cloud project
   - Enable Gmail API
   - Download `credentials.json`
   - Place in vault root

4. **Configure Email MCP**:
   - Get Gmail app password
   - Set environment variables:
     ```bash
     export SMTP_USER=your-email@gmail.com
     export SMTP_PASSWORD=your-app-password
     ```

5. **Start all watchers**:
```bash
# Option 1: Manual (3 terminals)
python watchers/filesystem_watcher.py
python watchers/gmail_watcher.py
python watchers/orchestrator.py

# Option 2: PM2 (recommended)
pm2 start watchers/filesystem_watcher.py --interpreter python3 --name fs-watcher
pm2 start watchers/gmail_watcher.py --interpreter python3 --name gmail-watcher
pm2 start watchers/orchestrator.py --interpreter python3 --name orchestrator
pm2 save
```

6. **Customize Business Goals**:
   - Edit `Business_Goals.md` with your targets and strategy

7. **Test the system**:
   - Send yourself an important email
   - Check `Needs_Action/` folder
   - Use LinkedIn Poster skill in Claude Code

## Usage

### Starting the System

**Using PM2 (Recommended for production):**
```bash
pm2 list                    # Check status
pm2 logs                    # View all logs
pm2 logs gmail-watcher      # View specific watcher
pm2 restart all             # Restart all watchers
pm2 stop all                # Stop all watchers
```

**Manual start (good for testing):**
```bash
# Terminal 1: File System Watcher
cd watchers && python filesystem_watcher.py

# Terminal 2: Gmail Watcher
cd watchers && python gmail_watcher.py

# Terminal 3: Orchestrator
cd watchers && python orchestrator.py
```

### Automated Workflows

**Gmail Monitoring:**
- Gmail Watcher checks every 2 minutes for important emails
- Creates action items in `Needs_Action/`
- Updates Dashboard automatically
- Tracks processed message IDs to avoid duplicates

**Email Sending:**
1. AI drafts email and creates file in `Pending_Approval/`
2. Human reviews and moves to `Approved/`
3. Orchestrator detects approved email (checks every 2 min)
4. Calls Email MCP server to send
5. Logs action and moves to `Done/`

**LinkedIn Posting:**
1. Use LinkedIn Poster skill to generate post draft
2. Draft created in `Plans/LinkedIn/`
3. Review and move to `Pending_Approval/`
4. Human approves by moving to `Approved/`
5. Copy approved text and post manually to LinkedIn
6. Orchestrator logs and archives

**Weekly CEO Briefing:**
- Runs automatically every Monday at 7:00 AM
- Analyzes week's activities
- Reviews Business_Goals.md
- Generates briefing in `Briefings/`
- Proactive suggestions included

### Using Claude Code

**Silver Tier prompts:**
```
"Use the linkedin-poster skill to create a post about [topic]"
"Process all emails in Needs_Action"
"Create a weekly summary and post draft for LinkedIn"
"Review Business_Goals.md and suggest optimizations"
"Generate Monday morning CEO briefing"
```

**Bronze Tier prompts (still work):**
```
"Read Dashboard.md and summarize current status"
"Check the Needs_Action folder for tasks"
"Move completed tasks to Done folder"
```

### Using Agent Skills

**Available Skills:**
- **vault-manager** (Bronze) - Task processing and file management
- **linkedin-poster** (Silver) - Social media content generation

To use a skill in Claude Code:
```
Use the [skill-name] skill to [task description]
```

Example:
```
Use the linkedin-poster skill to create a post about completing Silver Tier
```

## Human-in-the-Loop Workflow

For sensitive actions:
1. AI creates file in `Pending_Approval/`
2. You review the action details
3. Move to `Approved/` to proceed or `Rejected/` to cancel
4. AI executes approved actions automatically

## Security Notes
- All credentials stored in `.env` (never committed)
- All actions logged to `Logs/` folder
- No auto-approval for sensitive actions
- Regular audit recommended

## Daily Operations

### Morning Routine (5 minutes)
1. Check `Dashboard.md` for overnight activity
2. Review `Needs_Action/` for new tasks
3. Process `Pending_Approval/` items
4. Check PM2 logs for errors: `pm2 logs --lines 50`

### Weekly Routine (15 minutes - Mondays)
1. Read Monday Morning CEO Briefing in `Briefings/`
2. Update `Business_Goals.md` if needed
3. Review week's completed tasks in `Done/`
4. Plan LinkedIn posts for the week
5. Check subscription usage and costs

### Next Steps (Gold Tier)
Ready to level up? Gold Tier adds:
- WhatsApp Watcher for messaging automation
- Ralph Wiggum autonomous loop for multi-step tasks
- Multiple MCP servers (Calendar, Browser, Payment portals)
- LinkedIn API for automated posting (no manual copy/paste)
- Social media cross-posting (Facebook, Instagram, Twitter/X)
- Odoo accounting integration with MCP
- Automated weekly business and accounting audits
- Error recovery and graceful degradation
- Production deployment with cloud components

See the hackathon PDF for Gold Tier requirements.

## Troubleshooting

### Watcher not starting
- Check Python version: `python --version` (need 3.13+)
- Install dependencies: `pip install -r requirements.txt`
- Check permissions on Inbox folder

### Files not being detected
- Ensure watcher is running
- Check that files are in `Inbox/` not subfolders
- Check logs in `Logs/` folder

### Claude Code not finding files
- Ensure you're in the vault directory
- Check file paths are absolute or relative to vault root

## Contributing
This is a personal project for the Panaversity Hackathon. Customize as needed for your workflow.

## License
MIT License - Feel free to modify and adapt

## Resources
- [Hackathon Document](./Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.pdf)
- [Claude Code Documentation](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows)
- [Panaversity Website](https://www.panaversity.org)

---
**Status**: Gold Tier Build Complete 🏆 (Ready for Configuration)
**Version**: 3.0 (Gold Tier - Full Autonomous FTE)
**Last Updated**: 2026-02-23

## Quick Links
- [Gold Tier Setup Guide](GOLD_TIER_SETUP_GUIDE.md) - Detailed configuration instructions
- [Gold Tier Completion Report](Briefings/2026-02-23_Gold_Tier_Completion_Report.md) - Full build report
- [Silver Tier Completion Report](Briefings/2026-02-20_Silver_Tier_Completion_Report.md) - Silver tier build report
- [Bronze Tier Report](Briefings/2026-02-20_Bronze_Tier_Completion_Report.md) - Foundation verification
- [Hackathon PDF](./Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.pdf) - Original guide
