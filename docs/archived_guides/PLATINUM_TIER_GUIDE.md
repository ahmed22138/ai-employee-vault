## 💎 PLATINUM TIER - Complete Setup Guide

**Tagline**: Always-On Cloud + Local Executive Architecture

---

## What is Platinum Tier?

Platinum Tier transforms your AI Employee into a **true 24/7 autonomous system** with:

- **Cloud Agent (24/7)**: Runs on Oracle/AWS/Azure, monitors emails & drafts replies
- **Local Agent**: Runs on your machine, handles approvals & secure actions
- **Git Sync**: Vault syncs between Cloud and Local
- **Work-Zone Specialization**: Cloud drafts, Local executes
- **Claim-by-Move**: Prevents double-work between agents
- **Health Monitoring**: Auto-restarts failed processes
- **Security First**: Secrets NEVER sync to cloud

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     CLOUD AGENT (24/7)                      │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  │
│  │ Email Triage  │  │  Vault Sync   │  │Health Monitor │  │
│  │  (Draft Only) │  │   (Git Pull/  │  │ (Auto-restart)│  │
│  │               │  │    Push)      │  │               │  │
│  └───────┬───────┘  └───────┬───────┘  └───────────────┘  │
└──────────┼──────────────────┼────────────────────────────────┘
           │                  │
           │   Git Repository │
           │   (Vault Sync)   │
           │                  │
┌──────────┼──────────────────┼────────────────────────────────┐
│          ▼                  ▼                                │
│                     LOCAL AGENT                              │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  │
│  │   Approvals   │  │   WhatsApp    │  │   Payments    │  │
│  │   (HITL)      │  │   (Session)   │  │   (Banking)   │  │
│  │               │  │               │  │               │  │
│  └───────────────┘  └───────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### Required (From Previous Tiers)
- ✅ Bronze Tier Complete (file management, dashboard)
- ✅ Silver Tier Complete (Gmail, orchestrator, MCP servers)
- ✅ Gold Tier Complete (WhatsApp, Odoo, Ralph Wiggum, error recovery)

### New Requirements for Platinum
- **Cloud VM**: Oracle Cloud Free Tier / AWS / Azure (recommended: 2 CPU, 4GB RAM)
- **Git Repository**: GitHub/GitLab for vault sync (private repo recommended)
- **Domain (Optional)**: For Odoo HTTPS access
- **Static IP (Optional)**: For stable cloud access

---

## Part 1: Cloud Deployment (60 minutes)

### Step 1: Provision Cloud VM

**Option A: Oracle Cloud Free Tier (Recommended)**
```bash
# Oracle offers 2 free VMs (ARM) - perfect for this!
# 1. Sign up at: https://cloud.oracle.com/free
# 2. Create Ubuntu 22.04 VM instance (ARM or AMD)
# 3. Download SSH key
# 4. SSH into VM: ssh ubuntu@your-vm-ip
```

**Option B: AWS EC2**
```bash
# Use t2.micro (free tier eligible)
# Ubuntu 22.04 LTS
```

**Option C: Azure**
```bash
# Use B1s (free tier)
# Ubuntu 22.04 LTS
```

### Step 2: Deploy Cloud Agent

```bash
# SSH into your cloud VM
ssh ubuntu@your-cloud-vm-ip

# Clone your vault (we'll setup proper Git sync later)
git clone https://github.com/yourusername/ai-employee-vault.git /opt/ai-employee-vault
cd /opt/ai-employee-vault

# Run deployment script
chmod +x cloud-agent/deployment/deploy_cloud.sh
sudo ./cloud-agent/deployment/deploy_cloud.sh
```

**What This Script Does:**
- Installs Python 3.13, Node.js, PM2
- Creates `ai-employee` system user
- Installs dependencies
- Sets up systemd service
- Configures auto-start on boot

### Step 3: Configure Cloud Environment

```bash
# Create .env for Cloud (NO SECRETS!)
sudo nano /opt/ai-employee-vault/cloud-agent/.env
```

**Cloud .env (Minimal - NO sensitive data):**
```bash
# Cloud Agent Configuration
CLOUD_MODE=true
VAULT_PATH=/opt/ai-employee-vault
SYNC_INTERVAL=60
GMAIL_CHECK_INTERVAL=120

# Gmail API (OAuth credentials - read-only)
GMAIL_CREDENTIALS_PATH=/opt/ai-employee-vault/credentials_cloud.json

# IMPORTANT: Cloud has LIMITED Gmail credentials (read-only)
# Cloud CANNOT send emails (no SMTP credentials)
```

### Step 4: Setup Git Sync

```bash
# Configure Git for automatic sync
cd /opt/ai-employee-vault
git config user.name "Cloud Agent"
git config user.email "cloud@yourdomain.com"

# Setup SSH key for GitHub (password-less push)
ssh-keygen -t ed25519 -C "cloud-agent"
cat ~/.ssh/id_ed25519.pub
# Add this key to your GitHub repo: Settings > Deploy keys
```

### Step 5: Start Cloud Processes

```bash
# Using PM2
pm2 start /opt/ai-employee-vault/cloud-agent/ecosystem.config.js
pm2 save
pm2 startup

# Check status
pm2 list
pm2 logs
```

---

## Part 2: Local Agent Setup (30 minutes)

### Step 1: Update Local Vault

```bash
# On your local machine
cd /mnt/e/all-d-files/Ai_Employee_Vault

# Pull latest from Git (includes Platinum files)
git pull origin main

# Install local agent dependencies
pip install watchdog psutil GitPython
```

### Step 2: Configure Local Agent

Your existing `.env` already has full credentials. Just add:

```bash
# Add to your existing .env
CLOUD_MODE=false
LOCAL_AGENT=true
SYNC_INTERVAL=60
```

### Step 3: Start Local Approval Agent

**Option A: Run in terminal (for testing)**
```bash
python local-agent/local_approval_agent.py
```

**Option B: PM2 (for always-on local)**
```bash
pm2 start local-agent/local_approval_agent.py --interpreter python3 --name local-agent
pm2 save
```

### Step 4: Setup Local Vault Sync

```bash
# Your local machine should push/pull regularly
# Option 1: Manual (run when needed)
cd /mnt/e/all-d-files/Ai_Employee_Vault
git pull
git add .
git commit -m "Local changes"
git push

# Option 2: Automated (runs every minute)
pm2 start cloud-agent/vault_sync.py --interpreter python3 --name vault-sync-local
```

---

## Part 3: Work-Zone Specialization

### Cloud Owns (Draft-Only)
- ✅ Email triage (detects important emails)
- ✅ Email reply drafts (saved to /Pending_Approval/email/)
- ✅ Social media post drafts (saved to /Pending_Approval/social/)
- ✅ Research tasks (data gathering)
- ❌ **NEVER sends emails or posts**
- ❌ **NEVER accesses payments**

### Local Owns (Execution)
- ✅ All approvals (reviews Cloud's drafts)
- ✅ Email sending (via SMTP)
- ✅ WhatsApp (has session)
- ✅ Payments (has banking credentials)
- ✅ Final send/post actions

---

## Part 4: Claim-by-Move Coordination

### How It Works

**Scenario**: New email arrives

1. **Cloud detects email** → creates file in `/Needs_Action/email/`
2. **Cloud claims task** → moves to `/In_Progress/cloud/email/`
3. **Cloud creates draft** → writes to `/Pending_Approval/email/`
4. **Cloud syncs vault** → pushes to Git
5. **Local pulls vault** → sees draft in Pending_Approval
6. **You review & approve** → move to `/Approved/email/`
7. **Local agent sends** → moves to `/Done/email/`

**Key Rule**: If file is in `/In_Progress/cloud/`, Local CANNOT touch it (and vice versa)

---

## Part 5: Deploy Odoo on Cloud (Optional - 45 minutes)

```bash
# SSH into cloud VM
cd /opt/ai-employee-vault

# Deploy Odoo Community Edition
chmod +x cloud-agent/deployment/deploy_odoo.sh
sudo ./cloud-agent/deployment/deploy_odoo.sh

# After deployment:
# 1. Access Odoo: http://your-cloud-ip:8069
# 2. Create database (set master password)
# 3. Setup company, accounting
# 4. Configure Cloud MCP to connect (draft-only accounting)
```

---

## Part 6: Testing Platinum Demo

**Minimum Passing Gate**: Email arrives while Local is offline → Cloud drafts reply → Local approves later

### Test Scenario

1. **Start Cloud Agent** (on Cloud VM)
   ```bash
   pm2 list  # Should show all processes running
   ```

2. **Stop Local Agent** (simulate being offline)
   ```bash
   pm2 stop local-agent
   ```

3. **Send test email** to your Gmail
   - Subject: "IMPORTANT: Test Platinum Tier"
   - Body: "This is a test of offline cloud handling"

4. **Wait 2 minutes** (Cloud checks every 120 seconds)

5. **Check Cloud created draft**
   ```bash
   # On Cloud VM
   ls /opt/ai-employee-vault/Pending_Approval/email/
   # Should see DRAFT_REPLY_*.md
   ```

6. **Sync to Local** (simulate coming back online)
   ```bash
   # On Local machine
   git pull
   ls Pending_Approval/email/
   # Draft should appear!
   ```

7. **Approve draft** (move to Approved)
   ```bash
   mv Pending_Approval/email/DRAFT_REPLY_*.md Approved/email/
   ```

8. **Start Local Agent** (will detect and send)
   ```bash
   pm2 start local-agent
   ```

9. **Verify email sent**
   - Check recipient inbox
   - Check `/Done/email/` folder

✅ **If email arrived → Draft created by Cloud → Approved by you → Sent by Local = PLATINUM WORKING!**

---

## Security Verification Checklist

### Critical Security Rules

- [ ] `.env` file in `.gitignore` (NEVER syncs)
- [ ] `credentials.json` in `.gitignore`
- [ ] `token.json` in `.gitignore`
- [ ] `.whatsapp_session` in `.gitignore`
- [ ] Cloud `.env` has NO SMTP credentials
- [ ] Cloud `.env` has NO payment credentials
- [ ] Cloud `.env` has read-only Gmail credentials
- [ ] Local `.env` has full credentials
- [ ] Git repo is PRIVATE (not public)

**Verify**:
```bash
# Check what Git would commit
git status
# Should NOT show .env, credentials.json, tokens, sessions

# Check .gitignore
cat .gitignore | grep -E "(\.env|credentials|token|whatsapp)"
# Should show all sensitive files
```

---

## Monitoring & Maintenance

### Cloud Health Dashboard

```bash
# Check all processes
pm2 list

# View logs
pm2 logs cloud-email-triage
pm2 logs vault-sync
pm2 logs health-monitor

# System health
pm2 monit
```

### Health Metrics

Health monitor logs to: `/opt/ai-employee-vault/Logs/health_monitor.log`

**Alerts** are written to: `/opt/ai-employee-vault/Updates/ALERT_*.md`

Local agent sees these alerts and can notify you.

---

## Troubleshooting

### Cloud Agent Not Running

```bash
# Check PM2 status
pm2 list

# If errored, check logs
pm2 logs cloud-email-triage --lines 50

# Common issues:
# 1. Missing credentials
# 2. Git sync conflicts
# 3. Out of memory

# Restart
pm2 restart all
```

### Vault Sync Not Working

```bash
# Check git status
cd /opt/ai-employee-vault
git status

# If conflicts:
git stash
git pull --rebase
git stash pop

# If auth issues:
ssh -T git@github.com
# Should show: "Hi username! You've successfully authenticated"
```

### Emails Not Being Triaged

```bash
# Check Cloud has Gmail access
cd /opt/ai-employee-vault
ls credentials_cloud.json  # Should exist

# Check credentials work
python3 -c "from google.oauth2.credentials import Credentials; Credentials.from_authorized_user_file('credentials_cloud.json')"

# No errors = working
```

---

## Cost Analysis

### Monthly Cloud Costs

| Provider | Instance Type | Cost |
|----------|--------------|------|
| Oracle Cloud Free Tier | ARM VM | $0 (Free Forever) |
| AWS EC2 t2.micro | First year free | $0 → $10/mo after |
| Azure B1s | Free trial | $0 → $15/mo |
| DigitalOcean Droplet | Basic | $6/mo |

**Recommended**: Oracle Cloud Free Tier (genuinely free, no credit card charges)

### Total System Cost

| Component | Monthly Cost |
|-----------|-------------|
| Bronze Tier | $0 (local only) |
| Silver Tier | $20 (Claude API) |
| Gold Tier | $20 (Claude API) |
| **Platinum Tier** | **$0-10** (Cloud VM) |
| **Total** | **$20-30/mo** |

**Compare to hiring a human assistant**: $3,000-5,000/month

**ROI**: 99% cost savings! 🚀

---

## Next Steps After Platinum

Once Platinum is working:

1. **Scale Up**: Add more Cloud agents (social media poster, researcher)
2. **Multi-Region**: Deploy Cloud agents in different regions
3. **Advanced A2A**: Implement direct agent-to-agent messaging (Phase 2)
4. **Custom FTEs**: Build specialized Digital FTEs for specific domains
5. **Team Coordination**: Multiple Local agents coordinating via Cloud

---

## Summary

✅ **Cloud Agent**: 24/7 email triage & draft generation
✅ **Local Agent**: Approval & secure action execution
✅ **Git Sync**: Vault synchronized between Cloud & Local
✅ **Claim-by-Move**: No double-work coordination
✅ **Health Monitoring**: Auto-restart on failure
✅ **Odoo Cloud**: 24/7 accounting system (optional)
✅ **Security**: Secrets NEVER leave local machine

**Your AI Employee is now truly autonomous** - working even when you're offline! 💎

---

**Status**: Platinum Tier Complete 🏆
**Version**: 1.0
**Last Updated**: 2026-02-24
