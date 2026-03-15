# Silver Tier Setup Guide

**Quick Start Guide for Configuring Your AI Employee Silver Tier System**

---

## Prerequisites

Before starting, ensure you have:
- ✅ Completed Bronze Tier setup
- ✅ Claude Code installed and working
- ✅ Obsidian vault at `/mnt/e/all-d-files/Ai_Employee_Vault`
- ✅ Python 3.13+ installed
- ✅ Node.js v24+ installed
- ✅ Gmail account for email automation
- ✅ LinkedIn account for social posting

**Estimated setup time:** 30-60 minutes

---

## Phase 1: Install Dependencies (10 minutes)

### Step 1.1: Install Python Dependencies

```bash
cd /mnt/e/all-d-files/Ai_Employee_Vault
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed google-api-python-client-2.100.0
Successfully installed google-auth-httplib2-0.1.1
Successfully installed google-auth-oauthlib-1.1.0
Successfully installed schedule-1.2.0
Successfully installed requests-2.31.0
```

### Step 1.2: Install Node.js Dependencies

```bash
cd mcp-servers/email-server
npm install
```

**Expected output:**
```
added 1 package in 2s
```

### Step 1.3: Verify Installations

```bash
# Check Python packages
pip list | grep -E 'google|schedule|watchdog'

# Check Node packages
cd mcp-servers/email-server
npm list
```

---

## Phase 2: Configure Gmail API (15 minutes)

### Step 2.1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Select a Project" → "New Project"
3. Name: "AI Employee"
4. Click "Create"

### Step 2.2: Enable Gmail API

1. In Google Cloud Console, select your project
2. Go to "APIs & Services" → "Library"
3. Search for "Gmail API"
4. Click "Enable"

### Step 2.3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: "AI Employee"
   - User support email: your-email@gmail.com
   - Developer contact: your-email@gmail.com
   - Add scope: `https://www.googleapis.com/auth/gmail.readonly`
   - Add test user: your-email@gmail.com
   - Save and continue
4. Create OAuth client ID:
   - Application type: Desktop app
   - Name: "AI Employee Gmail Watcher"
   - Click "Create"
5. Download JSON file
6. Rename to `credentials.json`
7. Move to vault directory:
   ```bash
   mv ~/Downloads/credentials.json /mnt/e/all-d-files/Ai_Employee_Vault/
   ```

### Step 2.4: Test Gmail Watcher

```bash
cd /mnt/e/all-d-files/Ai_Employee_Vault/watchers
VAULT_PATH=/mnt/e/all-d-files/Ai_Employee_Vault python3 gmail_watcher.py
```

**First run:** Browser will open for Gmail authorization
1. Select your Gmail account
2. Click "Continue" (if warned about unverified app)
3. Click "Continue" to grant permissions
4. You should see "Authentication successful"
5. Close browser
6. Press Ctrl+C to stop watcher

**Successful output:**
```
[INFO] Gmail Watcher initialized successfully
[INFO] SMTP connection verified successfully
[INFO] Gmail Watcher started - monitoring for important emails
```

---

## Phase 3: Configure Email MCP Server (10 minutes)

### Step 3.1: Get Gmail App Password

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification if not enabled
3. Go to "Security" → "2-Step Verification"
4. Scroll to "App passwords"
5. Click "App passwords"
6. Select app: "Mail"
7. Select device: "Other" (enter "AI Employee")
8. Click "Generate"
9. Copy the 16-character password

### Step 3.2: Set Environment Variables

**For current session (Linux/Mac/WSL):**
```bash
export SMTP_USER=your-email@gmail.com
export SMTP_PASSWORD=your-16-char-app-password
export EMAIL_FROM=your-email@gmail.com
export VAULT_PATH=/mnt/e/all-d-files/Ai_Employee_Vault
```

**For permanent (add to ~/.bashrc or ~/.zshrc):**
```bash
echo "export SMTP_USER=your-email@gmail.com" >> ~/.bashrc
echo "export SMTP_PASSWORD=your-16-char-app-password" >> ~/.bashrc
echo "export EMAIL_FROM=your-email@gmail.com" >> ~/.bashrc
echo "export VAULT_PATH=/mnt/e/all-d-files/Ai_Employee_Vault" >> ~/.bashrc
source ~/.bashrc
```

### Step 3.3: Test Email MCP (Dry Run)

```bash
cd /mnt/e/all-d-files/Ai_Employee_Vault/mcp-servers/email-server
DRY_RUN=true node index.js
```

**Expected output:**
```
[Email MCP] Running in DRY RUN mode - no emails will be sent
[Email MCP] Server starting...
[Email MCP] Server ready
[Email MCP] Available tools: send_email, draft_email
[Email MCP] Listening on stdin...
```

Press Ctrl+C to stop.

### Step 3.4: Configure Claude Code MCP

Create or edit `~/.config/claude-code/mcp.json`:

```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/mnt/e/all-d-files/Ai_Employee_Vault/mcp-servers/email-server/index.js"],
      "env": {
        "SMTP_USER": "your-email@gmail.com",
        "SMTP_PASSWORD": "your-16-char-app-password",
        "EMAIL_FROM": "your-email@gmail.com"
      }
    }
  ]
}
```

**Replace with your actual email and password!**

---

## Phase 4: Customize Business Goals (5 minutes)

Edit `Business_Goals.md`:

```bash
cd /mnt/e/all-d-files/Ai_Employee_Vault
# Use your preferred editor
nano Business_Goals.md
# or
code Business_Goals.md
```

**Update these sections:**
1. Revenue Target - Your actual monthly goal
2. Active Projects - Your current projects
3. Target Audience - Your ideal clients
4. Value Proposition - Your business value
5. LinkedIn Strategy - Your posting goals
6. Subscriptions - Your actual subscriptions

**Save and close** (Ctrl+X, Y, Enter for nano)

---

## Phase 5: Start the System (5 minutes)

### Option A: Manual Start (Good for Testing)

Open **3 terminal windows:**

**Terminal 1: File System Watcher**
```bash
cd /mnt/e/all-d-files/Ai_Employee_Vault/watchers
VAULT_PATH=/mnt/e/all-d-files/Ai_Employee_Vault python3 filesystem_watcher.py
```

**Terminal 2: Gmail Watcher**
```bash
cd /mnt/e/all-d-files/Ai_Employee_Vault/watchers
VAULT_PATH=/mnt/e/all-d-files/Ai_Employee_Vault python3 gmail_watcher.py
```

**Terminal 3: Orchestrator**
```bash
cd /mnt/e/all-d-files/Ai_Employee_Vault/watchers
VAULT_PATH=/mnt/e/all-d-files/Ai_Employee_Vault python3 orchestrator.py
```

### Option B: Process Manager (Recommended for Production)

**Install PM2:**
```bash
npm install -g pm2
```

**Start all watchers:**
```bash
cd /mnt/e/all-d-files/Ai_Employee_Vault/watchers

pm2 start filesystem_watcher.py --interpreter python3 --name fs-watcher \
  --log-date-format 'YYYY-MM-DD HH:mm:ss' \
  -- --env VAULT_PATH=/mnt/e/all-d-files/Ai_Employee_Vault

pm2 start gmail_watcher.py --interpreter python3 --name gmail-watcher \
  --log-date-format 'YYYY-MM-DD HH:mm:ss' \
  -- --env VAULT_PATH=/mnt/e/all-d-files/Ai_Employee_Vault

pm2 start orchestrator.py --interpreter python3 --name orchestrator \
  --log-date-format 'YYYY-MM-DD HH:mm:ss' \
  -- --env VAULT_PATH=/mnt/e/all-d-files/Ai_Employee_Vault
```

**Save configuration:**
```bash
pm2 save
```

**Enable startup on boot:**
```bash
pm2 startup
# Follow the command it outputs
```

**Useful PM2 commands:**
```bash
pm2 list              # Show all processes
pm2 logs              # Show logs
pm2 logs fs-watcher   # Show specific process logs
pm2 monit             # Monitor in real-time
pm2 restart all       # Restart all processes
pm2 stop all          # Stop all processes
pm2 delete all        # Remove all processes
```

---

## Phase 6: Test the Complete Workflow (15 minutes)

### Test 1: Gmail Detection

1. **Send yourself a test email** (from another account or same account)
   - Subject: "URGENT: Test from AI Employee"
   - Mark as Important (star it)

2. **Wait up to 2 minutes** (Gmail Watcher polls every 120 seconds)

3. **Check Needs_Action folder:**
   ```bash
   ls /mnt/e/all-d-files/Ai_Employee_Vault/Needs_Action/
   ```

4. **Expected:** You should see a file like `EMAIL_20260220_URGENT_Test.md`

**✅ Test passed if file appears**

### Test 2: LinkedIn Post Draft

1. **Open Claude Code** in the vault directory:
   ```bash
   cd /mnt/e/all-d-files/Ai_Employee_Vault
   claude
   ```

2. **Prompt Claude:**
   ```
   Use the linkedin-poster skill to create a post about completing the Silver Tier AI Employee system
   ```

3. **Expected:** Claude should create a draft in `/Plans/LinkedIn/`

4. **Review the draft** and move to `/Pending_Approval/` if you like it

**✅ Test passed if draft is created**

### Test 3: Email Sending (End-to-End)

1. **Create a test approval file** in `/Pending_Approval/`:
   ```bash
   cat > /mnt/e/all-d-files/Ai_Employee_Vault/Pending_Approval/EMAIL_test.md << 'EOF'
   ---
   action: send_email
   to: your-email@gmail.com
   subject: Test Email from AI Employee
   ---

   ## Email Content

   This is a test email sent by the AI Employee system.

   Testing the complete workflow:
   1. Email draft created
   2. Moved to Pending_Approval
   3. Human reviewed and approved
   4. Orchestrator detected
   5. Email MCP sent email

   Success! 🎉
   EOF
   ```

2. **Move to Approved:**
   ```bash
   mv /mnt/e/all-d-files/Ai_Employee_Vault/Pending_Approval/EMAIL_test.md \
      /mnt/e/all-d-files/Ai_Employee_Vault/Approved/
   ```

3. **Wait up to 2 minutes** (Orchestrator checks every 2 minutes)

4. **Check your email** - you should receive the test email

5. **Check Done folder:**
   ```bash
   ls /mnt/e/all-d-files/Ai_Employee_Vault/Done/ | grep EMAIL_test
   ```

**✅ Test passed if email received and file moved to Done**

### Test 4: Orchestrator Scheduling

1. **Check orchestrator logs:**
   ```bash
   # If using PM2
   pm2 logs orchestrator

   # If manual
   tail -f /mnt/e/all-d-files/Ai_Employee_Vault/watchers/orchestrator.log
   ```

2. **Expected log entries:**
   ```
   [INFO] Orchestrator starting...
   [INFO] Setting up scheduled tasks
   [INFO] Schedules configured:
   [INFO]   - Check Needs_Action: Every 5 minutes
   [INFO]   - Check Approved: Every 2 minutes
   [INFO]   - Weekly briefing: Monday 7:00 AM
   [INFO]   - Health check: Daily 6:00 AM
   [INFO] Orchestrator running. Press Ctrl+C to stop.
   ```

**✅ Test passed if schedules are configured**

---

## Phase 7: Daily Operations

### Morning Routine (5 minutes)

1. **Check Dashboard:**
   ```bash
   cd /mnt/e/all-d-files/Ai_Employee_Vault
   cat Dashboard.md
   ```

2. **Review Needs_Action folder:**
   ```bash
   ls Needs_Action/
   ```

3. **Process pending approvals:**
   ```bash
   ls Pending_Approval/
   # Review each file, move to Approved/ or Rejected/
   ```

4. **Check logs for any errors:**
   ```bash
   pm2 logs --lines 50
   ```

### Weekly Routine (15 minutes)

**Every Monday morning:**

1. **Review Monday Morning CEO Briefing:**
   ```bash
   cd /mnt/e/all-d-files/Ai_Employee_Vault/Briefings
   ls -lt | head -5
   # Open most recent briefing
   ```

2. **Update Business_Goals.md** if needed

3. **Review completed tasks** from last week:
   ```bash
   ls Done/ | grep $(date -d "7 days ago" +%Y-%m-%d)
   ```

4. **Plan LinkedIn posts** for the week

---

## Troubleshooting

### Gmail Watcher Not Detecting Emails

**Problem:** No files appearing in Needs_Action/

**Solutions:**
1. Check Gmail Watcher is running:
   ```bash
   pm2 list | grep gmail-watcher
   ```

2. Check logs:
   ```bash
   pm2 logs gmail-watcher
   ```

3. Verify email is marked as "Important" in Gmail

4. Check processed IDs file:
   ```bash
   cat .gmail_processed_ids.txt
   # If your email ID is here, it won't be processed again
   ```

5. Force reprocess by deleting processed IDs:
   ```bash
   rm .gmail_processed_ids.txt
   pm2 restart gmail-watcher
   ```

### Email MCP Not Sending

**Problem:** Emails not being sent from Approved folder

**Solutions:**
1. Check SMTP credentials:
   ```bash
   echo $SMTP_USER
   echo $SMTP_PASSWORD
   ```

2. Test MCP in dry-run mode:
   ```bash
   cd mcp-servers/email-server
   DRY_RUN=true node index.js
   ```

3. Check Gmail app password is correct (16 characters, no spaces)

4. Verify 2-Step Verification is enabled on Google account

5. Check orchestrator logs:
   ```bash
   pm2 logs orchestrator | grep -i email
   ```

### Orchestrator Not Processing

**Problem:** Files staying in Approved/ folder

**Solutions:**
1. Check orchestrator is running:
   ```bash
   pm2 list | grep orchestrator
   ```

2. Check logs for errors:
   ```bash
   pm2 logs orchestrator --lines 100
   ```

3. Verify file format has correct frontmatter:
   ```yaml
   ---
   action: send_email
   to: email@example.com
   subject: Test
   ---
   ```

4. Manually trigger processing:
   ```bash
   pm2 restart orchestrator
   ```

---

## Next Steps

### Week 1: Get Comfortable
- [ ] Monitor all three watchers daily
- [ ] Process 5+ emails through the system
- [ ] Create and publish 1 LinkedIn post
- [ ] Review all logs for errors

### Week 2: Optimize
- [ ] Adjust Gmail Watcher check interval if needed
- [ ] Customize LinkedIn post templates
- [ ] Add more subscription tracking to Business_Goals.md
- [ ] Set up email filters in Gmail for better detection

### Week 3: Scale
- [ ] Increase LinkedIn posting to 2-3 times per week
- [ ] Add more automated email responses
- [ ] Create custom prompts for Claude
- [ ] Document your workflow improvements

### Gold Tier Preparation
- [ ] Review Gold Tier requirements in hackathon PDF
- [ ] Identify which advanced features you need
- [ ] Plan WhatsApp integration if needed
- [ ] Consider additional MCP servers (calendar, browser)

---

## Support & Resources

### Documentation
- **Bronze Tier:** See `Briefings/2026-02-20_Bronze_Tier_Completion_Report.md`
- **Silver Tier:** See `Briefings/2026-02-20_Silver_Tier_Completion_Report.md`
- **Technical:** See `README.md`
- **Quick Start:** See `QUICKSTART.md`
- **Hackathon Guide:** See the PDF in vault root

### Community
- **Weekly Meetings:** Every Wednesday 10:00 PM on Zoom
- **YouTube:** https://www.youtube.com/@panaversity
- **Submission:** https://forms.gle/JR9T1SJq5rmQyGkGA

### Logs Location
- Orchestrator: `watchers/orchestrator.log`
- Actions: `Logs/YYYY-MM-DD_actions.json`
- PM2: `~/.pm2/logs/`

---

## Success Checklist

Your Silver Tier system is fully operational when:

- [x] All Python dependencies installed
- [x] All Node.js dependencies installed
- [x] Gmail API configured and authenticated
- [x] Email MCP configured with SMTP
- [x] Business_Goals.md customized
- [ ] All 3 watchers running (fs, gmail, orchestrator)
- [ ] Gmail detection test passed
- [ ] LinkedIn draft test passed
- [ ] Email sending test passed
- [ ] Orchestrator scheduling confirmed
- [ ] First Monday briefing generated
- [ ] Complete workflow tested end-to-end

---

**Congratulations! Your Silver Tier AI Employee is now operational!** 🎉

For any issues, review the troubleshooting section or check the logs. The system is designed to be resilient and self-healing with proper configuration.

**Ready for Gold Tier?** Review the hackathon PDF for advanced features including WhatsApp integration, Ralph Wiggum autonomous loops, and multi-MCP orchestration.

---

*Setup Guide Version 1.0 - Generated 2026-02-20*
*Part of the Silver Tier AI Employee System*
