# 📚 AI EMPLOYEE - COMPLETE URDU/HINDI GUIDE
# پورا گائیڈ - AI Employee کو استعمال کرنے کا طریقہ

---
created: 2026-03-09
language: Urdu/Hindi (Roman)
tier: Gold Tier Complete
---

## 📂 FOLDER STRUCTURE (Folders ka Matlab)

```
Ai_Employee_Vault/
│
├── 📥 Inbox/                     ← Yaha FILES DROP karo
│   └── Koi bhi file yaha dalo (PDF, image, doc, etc.)
│   └── Watcher automatically detect karega
│
├── 🚨 Needs_Action/              ← NEW TASKS (Action chahiye)
│   └── WhatsApp messages, emails, files - sab yaha aate hain
│   └── AI inko process karega
│
├── 🔄 In_Progress/               ← CLAIMED TASKS (Kaam chal raha hai)
│   ├── local/                    ← Local agent ka kaam
│   └── cloud/                    ← Cloud agent ka kaam
│
├── ⏸️  Pending_Approval/         ← APPROVAL CHAHIYE (Aapka review)
│   ├── whatsapp/                 ← WhatsApp replies
│   ├── email/                    ← Email drafts
│   └── linkedin/                 ← LinkedIn posts
│
├── ✅ Approved/                  ← APPROVED (Ready to execute)
│   └── Aap yaha move karoge to execute hoga
│
├── ❌ Rejected/                  ← REJECTED (Cancel kar diya)
│   └── Jo approve nahi karna
│
├── ✔️  Done/                     ← COMPLETE (Khatam ho gaya)
│   └── Sab completed tasks yaha archive hote hain
│   └── Audit trail ke liye
│
├── 📊 Dashboard.md               ← SYSTEM STATUS (Live updates)
├── 📖 Company_Handbook.md        ← RULES (AI ke liye guidelines)
├── 🎯 Business_Goals.md          ← YOUR GOALS (Business targets)
│
└── 🤖 watchers/                  ← AUTOMATION SCRIPTS
    ├── whatsapp_watcher.py       ← WhatsApp monitor
    ├── gmail_watcher.py          ← Email monitor
    ├── filesystem_watcher.py     ← File monitor
    └── orchestrator.py           ← Main coordinator
```

---

## 🎯 FILE KA COMPLETE JOURNEY (Step by Step)

```
┌─────────────────────────────────────────────────────┐
│ 1️⃣  DETECTION (Detect hona)                         │
├─────────────────────────────────────────────────────┤
│ WhatsApp me message aaya                            │
│ → Watcher detect karta hai                          │
│ → File create hoti hai: Needs_Action/               │
│                                                      │
│ Example: WHATSAPP_20260305_034935_Ahmed.md          │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 2️⃣  CLAIM (Claim karna - Kaam shuru)                │
├─────────────────────────────────────────────────────┤
│ File move hoti hai:                                 │
│ Needs_Action/ → In_Progress/local/                  │
│                                                      │
│ Matlab: Task claim kar liya, ab process karunga     │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 3️⃣  AI ANALYSIS (AI sochta hai)                     │
├─────────────────────────────────────────────────────┤
│ AI padhta hai:                                       │
│ - Original message                                   │
│ - Business_Goals.md                                  │
│ - Company_Handbook.md                                │
│                                                      │
│ AI decide karta hai:                                 │
│ - Priority kya hai (HIGH/MEDIUM/LOW)                │
│ - Response kya hoga                                  │
│ - Approval chahiye ya nahi                          │
│                                                      │
│ Draft banata hai: Pending_Approval/whatsapp/         │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 4️⃣  HUMAN APPROVAL (Aapka review - IMPORTANT!)      │
├─────────────────────────────────────────────────────┤
│ AAP dekhte ho draft:                                 │
│ cat Pending_Approval/whatsapp/DRAFT_*.md             │
│                                                      │
│ AAP decide karte ho:                                 │
│ ✅ Approve → mv Pending_Approval/file Approved/     │
│ ❌ Reject  → mv Pending_Approval/file Rejected/     │
│ ✏️  Edit    → Edit karo, phir Approved/ me move    │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 5️⃣  EXECUTION (Kaam hona)                           │
├─────────────────────────────────────────────────────┤
│ Orchestrator detect karta hai (har 2 min check)     │
│                                                      │
│ Action execute hota hai:                             │
│ - WhatsApp message send                             │
│ - Email send                                         │
│ - LinkedIn post                                      │
│                                                      │
│ Log banata hai: Logs/                                │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 6️⃣  COMPLETION (Khatam - Archive)                   │
├─────────────────────────────────────────────────────┤
│ Sab files move hoti hain: Done/                     │
│                                                      │
│ Contains:                                            │
│ 1. Original message                                  │
│ 2. AI draft                                          │
│ 3. Execution log                                     │
│ 4. Complete timeline                                 │
│                                                      │
│ ✅ COMPLETE AUDIT TRAIL                             │
└─────────────────────────────────────────────────────┘
```

---

## 💻 COMMANDS (Kaunsa command kab use kare)

### 📱 WhatsApp Watcher Commands

```bash
# START KARNA (WhatsApp monitoring shuru)
python3 watchers/whatsapp_watcher.py

# BACKGROUND ME CHALANA (terminal band hone pe bhi chale)
python3 watchers/whatsapp_watcher.py &

# STATUS CHECK KARNA
ps aux | grep whatsapp

# STOP KARNA
pkill -f whatsapp_watcher

# LOGS DEKHNA
tail -f Logs/whatsapp_watcher.log
```

### 🎯 Orchestrator Commands (Main Coordinator)

```bash
# START KARNA
python3 watchers/orchestrator.py

# BACKGROUND ME CHALANA
python3 watchers/orchestrator.py &

# STATUS CHECK
ps aux | grep orchestrator

# LOGS DEKHNA
tail -f orchestrator.log
```

### 📧 Gmail Watcher Commands

```bash
# START KARNA
python3 watchers/gmail_watcher.py

# BACKGROUND ME
python3 watchers/gmail_watcher.py &

# CHECK KARNA
ps aux | grep gmail
```

### 📊 File/Folder Commands (Daily Use)

```bash
# NEEDS_ACTION ME KITNE FILES HAIN?
ls -1 Needs_Action/ | wc -l

# NEEDS_ACTION KI FILES DEKHNA
ls -la Needs_Action/

# PENDING APPROVAL DEKHNA
ls -la Pending_Approval/whatsapp/

# SPECIFIC FILE PADHNA
cat Needs_Action/WHATSAPP_*.md

# FILE APPROVE KARNA
mv Pending_Approval/whatsapp/DRAFT_Ahmed.md Approved/

# FILE REJECT KARNA
mv Pending_Approval/whatsapp/DRAFT_Ahmed.md Rejected/

# DONE FOLDER DEKHNA (Completed tasks)
ls -la Done/

# DASHBOARD DEKHNA
cat Dashboard.md
```

### 🔍 System Monitoring Commands

```bash
# SAB RUNNING PROCESSES DEKHNA
ps aux | grep -E "(whatsapp|orchestrator|gmail)"

# FOLDER STATUS CHECK
echo "Needs_Action: $(ls -1 Needs_Action/ | wc -l)"
echo "Pending: $(find Pending_Approval/ -name '*.md' | wc -l)"
echo "Approved: $(find Approved/ -name '*.md' | wc -l)"
echo "Done: $(find Done/ -name '*.md' | wc -l)"

# LOGS DEKHNA (Kya ho raha hai system me)
tail -100 orchestrator.log
tail -100 Logs/whatsapp_watcher.log

# SAB LOGS EK SAATH
tail -f orchestrator.log Logs/*.log
```

---

## 🚀 DAILY WORKFLOW (Har Din Kya Karna Hai)

### 🌅 Morning Routine (5 minutes)

```bash
# 1. System status check
ps aux | grep -E "(whatsapp|orchestrator)"

# 2. Pending tasks dekhna
ls -la Needs_Action/
ls -la Pending_Approval/

# 3. Dashboard padhna
cat Dashboard.md

# 4. Urgent items check
grep -r "priority: high" Needs_Action/
```

### 📅 During Day (Jab chahiye)

```bash
# New tasks check (har 1-2 ghante)
ls -1 Needs_Action/ | wc -l

# Pending approvals process karna
cat Pending_Approval/whatsapp/DRAFT_*.md
# Review karo aur approve/reject karo

# Logs dekhna agar kuch galat lag raha
tail -50 orchestrator.log
```

### 🌙 Evening Routine (5 minutes)

```bash
# Aaj kitne tasks complete hue?
ls -1 Done/ | grep $(date +%Y%m%d) | wc -l

# Pending approvals check (kal ke liye)
find Pending_Approval/ -name '*.md'

# System health check
ps aux | grep orchestrator
```

---

## 🎬 LIVE EXAMPLE (Real Example - Ahmed ka Message)

### Situation:
Ahmed ne WhatsApp pe message kiya: **"URGENT: INVOICE PAYMENT NEEDED ASAP"**

### Journey:

```bash
# STEP 1: Detection (03:49:35)
# WhatsApp Watcher ne detect kiya
# File created: Needs_Action/WHATSAPP_20260305_034935_Ahmed.md

# STEP 2: Check new file
cat Needs_Action/WHATSAPP_20260305_034935_Ahmed.md
# Output:
# ---
# type: whatsapp_message
# from: Ahmed
# priority: high
# ---
# Message: URGENT: INVOICE PAYMENT NEEDED ASAP

# STEP 3: AI Analysis (Manual demo)
# AI ne draft banaya: Pending_Approval/whatsapp/DRAFT_RESPONSE_Ahmed_Invoice_Payment.md
# 3 options diye:
#   A. Request invoice details (RECOMMENDED)
#   B. Immediate payment confirmation
#   C. Request extension

# STEP 4: Review draft
cat Pending_Approval/whatsapp/DRAFT_RESPONSE_Ahmed_Invoice_Payment.md
# Padhkar decision liya: Option A select kiya

# STEP 5: Approve
mv Pending_Approval/whatsapp/DRAFT_RESPONSE_Ahmed_Invoice_Payment.md Approved/

# STEP 6: Orchestrator auto-execute (01:09:20)
# Orchestrator ne detect kiya Approved/ me file hai
# Automatically Done/ me move kar diya
# Log entry create ki

# STEP 7: Verification
ls -la Done/ | grep Ahmed
# Output:
# WHATSAPP_20260305_034935_Ahmed.md
# DRAFT_RESPONSE_Ahmed_Invoice_Payment.md
# ✅ COMPLETE!
```

---

## ⚙️ AUTOMATION LEVELS (Kitna automate hai)

### Level 1: Detection Only (Basic) ✅ CURRENT
```
✅ WhatsApp Watcher running
✅ Files create ho rahe hain Needs_Action/ me
❌ Manual review zaruri har file ka
```

### Level 2: Orchestrator + AI (Silver Tier) ✅ RUNNING NOW!
```
✅ WhatsApp Watcher
✅ Orchestrator running
✅ AI drafts create ho rahe hain
⏸️  Aap approve karte ho
✅ Semi-automatic
```

### Level 3: Full Automation (Platinum Tier)
```
✅ Cloud Agent (24/7 monitoring)
✅ Local Agent (execution)
✅ Complete automation
⏸️  Sirf sensitive actions me approval
```

---

## 🔧 TROUBLESHOOTING (Agar kuch problem ho)

### WhatsApp Watcher not running
```bash
# Check karo running hai ya nahi
ps aux | grep whatsapp

# Agar nahi chal raha, start karo
python3 watchers/whatsapp_watcher.py &

# Agar error aa raha
tail -50 Logs/whatsapp_watcher.log
```

### Orchestrator stopped
```bash
# Check status
ps aux | grep orchestrator

# Restart karo
python3 watchers/orchestrator.py &

# Logs check karo
tail -50 orchestrator.log
```

### Files not moving to Done/
```bash
# Orchestrator running hai?
ps aux | grep orchestrator

# Approved/ me files hain?
ls -la Approved/

# Wait karo 2 minutes (orchestrator har 2 min check karta)
# Ya manually move karo:
mv Approved/*.md Done/
```

### QR Code scan chahiye (WhatsApp)
```bash
# Non-headless mode me run karo
WHATSAPP_HEADLESS=false python3 watchers/whatsapp_watcher.py

# Browser window open hoga
# QR code scan karo phone se
# Login save ho jayega ~/.whatsapp_session me
```

---

## 📝 IMPORTANT FILES (Zaruri Files)

### Dashboard.md
```bash
# Real-time status dekhne ke liye
cat Dashboard.md

# Live updates
tail -f Dashboard.md
```

### Business_Goals.md
```bash
# Apne business goals edit karo
nano Business_Goals.md

# AI yahi padh kar decisions leta hai
```

### Company_Handbook.md
```bash
# AI ke liye rules
nano Company_Handbook.md

# Example rules:
# - Financial transactions require approval
# - Email response time < 24 hours
# - Invoice payment rate > 90%
```

---

## 🎯 QUICK REFERENCE (Jaldi Commands)

```bash
# ============= MONITORING =============
# System check
ps aux | grep -E "(whatsapp|orchestrator|gmail)" | grep -v grep

# File counts
echo "Needs: $(ls -1 Needs_Action/ | wc -l), Pending: $(find Pending_Approval/ -name '*.md' | wc -l), Done: $(find Done/ -name '*.md' | wc -l)"

# Recent logs
tail -20 orchestrator.log

# ============= STARTING SERVICES =============
# Start WhatsApp Watcher
python3 watchers/whatsapp_watcher.py &

# Start Orchestrator
python3 watchers/orchestrator.py &

# Start Gmail Watcher
python3 watchers/gmail_watcher.py &

# ============= FILE OPERATIONS =============
# List pending approvals
find Pending_Approval/ -name '*.md'

# Approve a file
mv Pending_Approval/whatsapp/DRAFT_*.md Approved/

# Reject a file
mv Pending_Approval/whatsapp/DRAFT_*.md Rejected/

# Check completed today
ls -1 Done/ | grep $(date +%Y%m%d)

# ============= DEBUGGING =============
# Kill all watchers
pkill -f "whatsapp_watcher|orchestrator|gmail_watcher"

# Restart everything
python3 watchers/whatsapp_watcher.py &
python3 watchers/orchestrator.py &

# Watch live logs
tail -f orchestrator.log
```

---

## 📚 DOCUMENTATION FILES

```
README.md                    ← Complete English documentation
QUICKSTART.md                ← Quick start guide
URDU_COMPLETE_GUIDE.md       ← THIS FILE (Urdu/Hindi guide)
WHATSAPP_COMPLETE_GUIDE_A_TO_Z.md  ← WhatsApp specific guide
GOLD_TIER_SETUP_GUIDE.md     ← Gold tier setup
COMPLETE_VERIFICATION_REPORT.md    ← System verification
```

---

## 🎓 SUMMARY (Kya kya seekha)

1. **Folder Structure**: Needs_Action → In_Progress → Pending_Approval → Approved → Done
2. **File Journey**: 6 steps me complete workflow
3. **Commands**: Start/stop watchers, check status, approve/reject files
4. **Daily Workflow**: Morning/day/evening routine
5. **Automation Levels**: Level 1 → Level 2 ✅ → Level 3
6. **Troubleshooting**: Common problems aur solutions

---

## ✅ CHECKLIST (Apni System Check Karo)

```
□ WhatsApp Watcher running?          ps aux | grep whatsapp
□ Orchestrator running?               ps aux | grep orchestrator
□ Files in Needs_Action?              ls -1 Needs_Action/
□ Pending approvals?                  ls -1 Pending_Approval/
□ Dashboard updated?                  cat Dashboard.md
□ Logs koi error?                     tail -50 orchestrator.log
□ Done folder archiving?              ls -1 Done/ | wc -l
```

---

**🎉 Congratulations! Ab aap complete AI Employee system use kar sakte ho!**

---

*Last Updated: 2026-03-09*
*Version: Gold Tier - Urdu/Hindi Guide v1.0*
*Created by: Claude Code*
