# 💎 PLATINUM TIER - DEPLOYMENT GUIDE
# Platinum Tier کہاں Deploy کرنا Hai

---
**Language:** Urdu/Hindi + English
**Time Needed:** 90 minutes (automated)
**Cost:** FREE (using free tier)

---

## 🎯 PLATINUM TIER KYA HAI?

Platinum tier aapko **24/7 cloud monitoring** deta hai:

```
☁️  CLOUD AGENT (Oracle/AWS - Always Running)
    ├─ Monitors Gmail 24/7
    ├─ Creates task drafts
    ├─ NO secrets/passwords stored
    └─ Syncs via Git

🖥️  LOCAL AGENT (Aapka Computer - Your Control)
    ├─ Executes approved tasks
    ├─ Sends WhatsApp/Email
    ├─ ALL credentials stay with you
    └─ Syncs via Git
```

**Faida:** Cloud agent never sleeps, monitors 24/7. Local agent has full control and all secrets.

---

## 📍 KAHA DEPLOY KARNA HAI? (3 Locations)

### Location 1: **CLOUD VM** ☁️ (Required)
**Kya:** Virtual server jo 24/7 chalta rehta hai
**Options:**
1. ⭐ **Oracle Cloud** (FREE Forever - Recommended!)
2. **AWS EC2** (Free 12 months)
3. **Azure VM** (Free 12 months)
4. **DigitalOcean** ($5/month)

**Purpose:** Cloud agent runs here (monitoring only)

---

### Location 2: **GIT REPOSITORY** 📦 (Required)
**Kya:** File storage jo cloud aur local ko sync karta hai
**Options:**
1. ⭐ **GitHub** (FREE - Recommended!)
2. **GitLab** (FREE)
3. **Bitbucket** (FREE)

**Purpose:** Tasks ko cloud se local tak pohanchana

---

### Location 3: **YOUR COMPUTER** 🖥️ (Already Have!)
**Kya:** Aapka current machine
**Purpose:** Local agent runs here (execution with credentials)

---

## 🆓 RECOMMENDED SETUP (100% FREE!)

```
┌─────────────────────────────────────────────────────┐
│  ☁️  ORACLE CLOUD FREE TIER (Cloud Agent)          │
│     Location: Singapore/Tokyo/Any Region            │
│     Cost: FREE FOREVER                              │
│     Specs: 1 CPU, 1GB RAM (enough!)                 │
└─────────────────────────────────────────────────────┘
                        ↕️  (Git Sync)
┌─────────────────────────────────────────────────────┐
│  📦 GITHUB PRIVATE REPO (Vault Sync)                │
│     Cost: FREE                                      │
│     Storage: Unlimited for code                     │
└─────────────────────────────────────────────────────┘
                        ↕️  (Git Sync)
┌─────────────────────────────────────────────────────┐
│  🖥️  YOUR COMPUTER (Local Agent)                   │
│     Location: Your home/office                      │
│     Cost: FREE (already have!)                      │
└─────────────────────────────────────────────────────┘
```

**Total Cost: 🆓 COMPLETELY FREE!**

---

## 🚀 STEP-BY-STEP DEPLOYMENT

### STEP 1: ORACLE CLOUD VM SETUP (30 minutes)

#### 1.1 Create Oracle Cloud Account
1. **Website pe jao:** https://www.oracle.com/cloud/free/
2. **Sign Up** karo:
   - Email address
   - Password
   - Country: Pakistan/Your country
   - Phone number (verification ke liye)
3. **Credit card** add karo (sirf verification, charge nahi hoga!)
4. Account create ho jayega ✅

#### 1.2 Create Free VM Instance
1. **Login karo:** https://cloud.oracle.com
2. **Hamburger menu** (☰) → **Compute** → **Instances**
3. **Create Instance** button pe click
4. **Configure:**
   ```
   Name: ai-employee-cloud

   Image: Ubuntu 22.04 (Canonical)

   Shape: VM.Standard.E2.1.Micro (Always Free ⭐)

   Add SSH Keys: Generate new key pair (DOWNLOAD IT!)

   Boot Volume: 50GB (free tier limit)
   ```
5. **Create** button click
6. Wait 2-3 minutes
7. **Public IP** note karo (e.g., 123.45.67.89)

#### 1.3 Test SSH Connection
```bash
# Downloaded SSH key ka permission set karo
chmod 400 ~/Downloads/ssh-key-*.key

# SSH test karo
ssh -i ~/Downloads/ssh-key-*.key ubuntu@123.45.67.89
# (123.45.67.89 = your VM IP)

# Success! You're in Oracle Cloud VM ✅
```

---

### STEP 2: GITHUB REPOSITORY SETUP (10 minutes)

#### 2.1 Create Private Repository
1. **GitHub pe jao:** https://github.com
2. **Login** karo (ya Sign Up if new)
3. Click **New** (repository)
4. **Configure:**
   ```
   Repository name: ai-employee-vault-sync

   Description: AI Employee Vault - Cloud/Local Sync

   ✅ Private (IMPORTANT - secrets ko protect karne ke liye)

   ❌ Don't add README
   ❌ Don't add .gitignore (we already have)
   ```
5. Click **Create repository**
6. **Repository URL** copy karo:
   ```
   https://github.com/YOUR_USERNAME/ai-employee-vault-sync.git
   ```

#### 2.2 Generate Personal Access Token (for Git)
1. **GitHub** → **Settings** (top-right avatar)
2. **Developer settings** (bottom left)
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token (classic)**
5. **Configure:**
   ```
   Note: AI Employee Vault Sync

   Expiration: No expiration (or 1 year)

   Scopes:
   ✅ repo (full control of private repositories)
   ```
6. Click **Generate token**
7. **Copy token** (ghp_xxxxx...) - SAVE IT! (won't show again)

---

### STEP 3: RUN SETUP SCRIPT (20 minutes)

#### 3.1 Local Setup (Aapka Computer)
```bash
cd /mnt/e/all-d-files/Ai_Employee_Vault

# Platinum setup script run karo
bash setup_platinum_tier.sh
```

**Script kya karegi:**
1. ✅ Git repository initialize
2. ✅ Create .gitignore (security!)
3. ✅ Ask for GitHub URL
4. ✅ Configure Git remote
5. ✅ Create deployment scripts
6. ✅ Push to GitHub
7. ✅ Show next steps

**Script prompts (example):**
```
Do you have a GitHub/GitLab repository URL? (y/n) y
Enter repository URL: https://github.com/YOUR_USERNAME/ai-employee-vault-sync.git

Commit and push to repository? (y/n) y

✅ Pushed to repository
```

#### 3.2 Cloud Setup (Oracle VM)
```bash
# SSH into Oracle Cloud VM
ssh -i ~/Downloads/ssh-key-*.key ubuntu@123.45.67.89

# Download deployment script from local
# (Script was created by setup_platinum_tier.sh)
```

**Local machine pe (new terminal):**
```bash
cd /mnt/e/all-d-files/Ai_Employee_Vault

# Copy deployment script to cloud VM
scp -i ~/Downloads/ssh-key-*.key \
    cloud-agent/deployment/deploy_to_cloud.sh \
    ubuntu@123.45.67.89:~/
```

**Cloud VM pe (back to SSH terminal):**
```bash
# Run deployment script
bash deploy_to_cloud.sh
```

**Script kya karegi (on cloud VM):**
1. ✅ Update system (apt update)
2. ✅ Install Python, Node.js, PM2
3. ✅ Clone GitHub repository
4. ✅ Install dependencies
5. ✅ Create .env (read-only mode)
6. ✅ Start PM2 processes:
   - cloud-email-triage
   - vault-sync
   - health-monitor
7. ✅ Configure auto-restart on boot

---

### STEP 4: START LOCAL AGENT (5 minutes)

**Aapke computer pe:**
```bash
cd /mnt/e/all-d-files/Ai_Employee_Vault

# Start local approval agent
python3 local-agent/local_approval_agent.py &

# Start vault sync (local side)
python3 cloud-agent/vault_sync.py &
```

---

### STEP 5: TEST THE SYSTEM (10 minutes)

#### Test 1: Cloud → Local Sync
**On Cloud VM:**
```bash
cd ~/vault
echo "Test from cloud" > Needs_Action/test_cloud.md
git add .
git commit -m "Test from cloud"
git push origin main
```

**On Local Machine:**
```bash
cd /mnt/e/all-d-files/Ai_Employee_Vault
git pull origin main
cat Needs_Action/test_cloud.md
# Should show: "Test from cloud" ✅
```

#### Test 2: Local → Cloud Sync
**On Local Machine:**
```bash
echo "Test from local" > Done/test_local.md
git add Done/
git commit -m "Test from local"
git push origin main
```

**On Cloud VM:**
```bash
cd ~/vault
git pull origin main
cat Done/test_local.md
# Should show: "Test from local" ✅
```

#### Test 3: Check Cloud Processes
**On Cloud VM:**
```bash
pm2 status

# Should show:
# ✅ cloud-email-triage  online
# ✅ vault-sync          online
# ✅ health-monitor      online
```

---

## 📊 ARCHITECTURE DIAGRAM

```
┌────────────────────────────────────────────────────────────┐
│  ☁️  ORACLE CLOUD VM (Singapore)                           │
│  IP: 123.45.67.89                                          │
│                                                            │
│  PM2 Processes:                                            │
│  ├─ cloud-email-triage (Gmail read-only)                  │
│  ├─ vault-sync (Git push/pull every 5 min)                │
│  └─ health-monitor (Process monitoring)                    │
│                                                            │
│  What it does:                                             │
│  • Monitors Gmail 24/7                                     │
│  • Creates task drafts                                     │
│  • Pushes to GitHub                                        │
│  • NO secrets stored!                                      │
└────────────────────────────────────────────────────────────┘
                          ↕️
                     Git Sync
                          ↕️
┌────────────────────────────────────────────────────────────┐
│  📦 GITHUB PRIVATE REPO                                    │
│  https://github.com/YOUR_USERNAME/ai-employee-vault-sync   │
│                                                            │
│  What's synced:                                            │
│  ✅ Needs_Action/*.md (new tasks)                          │
│  ✅ Pending_Approval/*.md (drafts)                         │
│  ✅ Approved/*.md (ready to execute)                       │
│  ✅ Done/*.md (completed)                                  │
│                                                            │
│  What's NOT synced (security):                             │
│  ❌ .env (credentials)                                     │
│  ❌ credentials.json (OAuth)                               │
│  ❌ .whatsapp_session/ (login)                             │
│  ❌ *.log (sensitive logs)                                 │
└────────────────────────────────────────────────────────────┘
                          ↕️
                     Git Sync
                          ↕️
┌────────────────────────────────────────────────────────────┐
│  🖥️  YOUR COMPUTER (WSL/Ubuntu)                            │
│  Location: /mnt/e/all-d-files/Ai_Employee_Vault            │
│                                                            │
│  Processes:                                                │
│  ├─ local_approval_agent (executes approved tasks)        │
│  ├─ vault_sync (Git push/pull every 5 min)                │
│  ├─ whatsapp_watcher (WhatsApp monitoring)                │
│  └─ orchestrator (task coordination)                       │
│                                                            │
│  What it does:                                             │
│  • Pulls tasks from GitHub                                 │
│  • Executes with YOUR credentials                          │
│  • Sends WhatsApp/Email                                    │
│  • Pushes completed tasks back                             │
│  • ALL secrets stay here (secure!)                         │
└────────────────────────────────────────────────────────────┘
```

---

## 💰 COST BREAKDOWN

| Component | Service | Cost |
|-----------|---------|------|
| Cloud VM | Oracle Cloud Free Tier | 🆓 FREE (forever) |
| Git Repo | GitHub Private Repo | 🆓 FREE |
| Local Agent | Your Computer | 🆓 FREE |
| Domain | None (optional) | 🆓 FREE |
| **TOTAL** | | **🆓 COMPLETELY FREE!** |

---

## 🔐 SECURITY MODEL

### Cloud Agent (Oracle VM):
```bash
# .env file on cloud (NO SECRETS!)
CLOUD_MODE=true
DEPLOYMENT_ENVIRONMENT=cloud

# Gmail OAuth (read-only)
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_secret

# NO SMTP passwords!
# NO WhatsApp credentials!
# NO Odoo passwords!
```

### Local Agent (Your Computer):
```bash
# .env file on local (ALL SECRETS!)
CLOUD_MODE=false
DEPLOYMENT_ENVIRONMENT=local

# All credentials here
SMTP_USER=your-email@gmail.com
SMTP_PASS=your_app_password
WHATSAPP_HEADLESS=true
ODOO_PASSWORD=your_password
# ... everything
```

**Result:** Secrets never leave your computer! ✅

---

## 🎯 DAILY WORKFLOW (After Deployment)

### Morning (Subah - 5 min):
```bash
# Check cloud status (from local)
ssh ubuntu@123.45.67.89 "pm2 status"

# Pull new tasks from cloud
cd /mnt/e/all-d-files/Ai_Employee_Vault
git pull origin main

# Check pending approvals
find Pending_Approval/ -name '*.md'

# Approve tasks
mv Pending_Approval/whatsapp/*.md Approved/

# Push approvals back
git add Approved/
git commit -m "Morning approvals"
git push origin main
```

### Cloud Automatically:
- ✅ Monitors Gmail 24/7
- ✅ Creates drafts every 2 minutes
- ✅ Syncs to GitHub every 5 minutes

### Local Automatically:
- ✅ Pulls from GitHub every 5 minutes
- ✅ Executes approved tasks
- ✅ Pushes completed tasks back

**You just approve, system does rest!** 🎉

---

## 🛠️ MANAGEMENT COMMANDS

### Check Cloud Status (from anywhere):
```bash
ssh ubuntu@YOUR_VM_IP "pm2 status"
```

### View Cloud Logs:
```bash
ssh ubuntu@YOUR_VM_IP "pm2 logs cloud-email-triage"
ssh ubuntu@YOUR_VM_IP "pm2 logs vault-sync"
```

### Restart Cloud Processes:
```bash
ssh ubuntu@YOUR_VM_IP "pm2 restart all"
```

### Stop Cloud (temporarily):
```bash
ssh ubuntu@YOUR_VM_IP "pm2 stop all"
```

### Update Cloud Agent:
```bash
# Push changes from local
git push origin main

# Pull on cloud
ssh ubuntu@YOUR_VM_IP "cd ~/vault && git pull && pm2 restart all"
```

---

## ❓ COMMON QUESTIONS

### Q1: Oracle Cloud ke alawa koi aur option?
**A:** Haan! AWS EC2 ya Azure VM use kar sakte ho:
```bash
# AWS EC2 Free Tier
# Azure Free Tier

# Setup same hai, sirf VM provider alag hai
```

### Q2: GitHub private repo zaroori hai?
**A:** Haan! Public mat banao, secrets leak ho jayenge.

### Q3: Kya mobile se cloud manage kar sakta hoon?
**A:** Haan! SSH apps use karo:
- Termius (Android/iOS)
- JuiceSSH (Android)

### Q4: Cloud band ho jaye to?
**A:** Local agent chalta rahega. Cloud monitoring ruk jayegi.

### Q5: Kitna data GitHub me store hoga?
**A:** Bohot kam! Sirf task files (.md), no logs, no credentials.

---

## 🎉 DEPLOYMENT SUMMARY

### What You Need:
1. ✅ Oracle Cloud account (FREE)
2. ✅ GitHub account (FREE)
3. ✅ Your computer (already have)
4. ✅ 90 minutes time

### What You Get:
1. ✅ 24/7 cloud monitoring
2. ✅ Local execution (secure)
3. ✅ Auto-sync (Git-based)
4. ✅ Complete separation (cloud/local)
5. ✅ Zero monthly cost

### Quick Start:
```bash
# One command!
bash setup_platinum_tier.sh
```

---

## 📖 DETAILED GUIDES

**Step-by-step videos/tutorials:**
- Oracle Cloud VM: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm
- GitHub Setup: https://docs.github.com/en/get-started
- PM2 Process Manager: https://pm2.keymetrics.io/docs/usage/quick-start/

**Or simply:**
```bash
bash setup_platinum_tier.sh
# Script will guide you step-by-step!
```

---

## ✅ FINAL CHECKLIST

- [ ] Oracle Cloud account created
- [ ] VM instance created (Ubuntu 22.04)
- [ ] SSH key downloaded
- [ ] Can SSH into VM
- [ ] GitHub account created
- [ ] Private repository created
- [ ] Personal access token generated
- [ ] Run `setup_platinum_tier.sh` on local
- [ ] Copy `deploy_to_cloud.sh` to VM
- [ ] Run deployment script on VM
- [ ] Test cloud → local sync
- [ ] Test local → cloud sync
- [ ] PM2 processes running
- [ ] Local agent running

**All done? 🎉 Platinum tier deployed!**

---

*Last Updated: 2026-03-11*
*Deployment Time: ~90 minutes*
*Cost: 🆓 FREE*
*Difficulty: Medium (automated scripts help!)*
