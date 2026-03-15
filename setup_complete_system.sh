#!/bin/bash
# 🎯 COMPLETE SYSTEM SETUP - ALL TIERS
# Master setup script for AI Employee Vault

set -e

clear

echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║    🎯 AI EMPLOYEE VAULT - COMPLETE SETUP             ║"
echo "║    Bronze → Silver → Gold → Platinum                 ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Check if running in correct directory
if [ ! -f "Company_Handbook.md" ]; then
    echo "❌ Error: Please run this script from the Ai_Employee_Vault directory"
    echo "   cd /mnt/e/all-d-files/Ai_Employee_Vault"
    exit 1
fi

echo "📋 This master script will guide you through setting up:"
echo ""
echo "   🥉 TIER 1: BRONZE - File Monitoring (5 min)"
echo "   🥈 TIER 2: SILVER - Email + LinkedIn (22 min)"
echo "   🥇 TIER 3: GOLD - WhatsApp + Browser (20 min)"
echo "   💎 TIER 4: PLATINUM - Cloud Deployment (90 min)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Function to check component status
check_status() {
    local component=$1
    local check_command=$2

    if eval "$check_command" &>/dev/null; then
        echo "   ✅ $component"
        return 0
    else
        echo "   ❌ $component"
        return 1
    fi
}

# Current system status
echo "📊 CURRENT SYSTEM STATUS:"
echo ""

echo "🥉 BRONZE TIER:"
check_status "Folders structure" "[ -d 'Inbox' ] && [ -d 'Needs_Action' ] && [ -d 'Done' ]"
check_status "Filesystem watcher" "[ -f 'watchers/filesystem_watcher.py' ]"

echo ""
echo "🥈 SILVER TIER:"
check_status "Gmail watcher" "[ -f 'watchers/gmail_watcher.py' ]"
check_status "Orchestrator" "[ -f 'watchers/orchestrator.py' ]"
check_status "Gmail OAuth" "[ -f 'credentials.json' ]"
check_status "Gmail token" "[ -f 'token.json' ]"
check_status ".env configuration" "[ -f '.env' ]"

echo ""
echo "🥇 GOLD TIER:"
check_status "WhatsApp watcher" "[ -f 'watchers/whatsapp_watcher.py' ]"
check_status "Playwright installed" "pip list 2>/dev/null | grep -q playwright"
check_status "Chromium browser" "[ -d '$HOME/.cache/ms-playwright' ]"
check_status "WhatsApp session" "[ -d '$HOME/.whatsapp_session' ]"

echo ""
echo "💎 PLATINUM TIER:"
check_status "Cloud agent" "[ -f 'cloud-agent/vault_sync.py' ]"
check_status "Local agent" "[ -f 'local-agent/local_approval_agent.py' ]"
check_status "Git repository" "[ -d '.git' ]"
check_status "Git remote" "git remote | grep -q origin 2>/dev/null"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Main menu
while true; do
    echo ""
    echo "🎯 SETUP OPTIONS:"
    echo ""
    echo "   1. 🥉 Setup Bronze Tier (File Monitoring)"
    echo "   2. 🥈 Setup Silver Tier (Email + LinkedIn)"
    echo "   3. 🥇 Setup Gold Tier (WhatsApp + Browser)"
    echo "   4. 💎 Setup Platinum Tier (Cloud Deployment)"
    echo ""
    echo "   5. 🚀 Quick Start (Bronze + Gold only)"
    echo "   6. 🔧 Complete Setup (All Tiers)"
    echo ""
    echo "   7. 📊 Check System Status"
    echo "   8. 📖 View Documentation"
    echo "   9. ❌ Exit"
    echo ""
    read -p "Choose option (1-9): " -n 1 -r OPTION
    echo ""
    echo ""

    case $OPTION in
        1)
            echo "🥉 Setting up Bronze Tier..."
            echo ""
            echo "Bronze Tier provides:"
            echo "   • File monitoring (Inbox folder)"
            echo "   • Task creation"
            echo "   • Human approval workflow"
            echo ""

            # Check folders
            echo "📂 Checking folder structure..."
            FOLDERS=("Inbox" "Needs_Action" "In_Progress" "Pending_Approval" "Approved" "Rejected" "Done" "Logs" "Briefings")
            for folder in "${FOLDERS[@]}"; do
                if [ ! -d "$folder" ]; then
                    mkdir -p "$folder"
                    echo "   ✅ Created: $folder/"
                else
                    echo "   ✅ Exists: $folder/"
                fi
            done

            echo ""
            echo "✅ Bronze Tier ready!"
            echo ""
            echo "🚀 Start Bronze:"
            echo "   python3 watchers/filesystem_watcher.py &"
            echo ""
            echo "📝 Test:"
            echo "   echo 'test' > Inbox/test.txt"
            echo "   ls Needs_Action/"
            ;;

        2)
            echo "🥈 Setting up Silver Tier..."
            if [ -f "setup_silver_tier.sh" ]; then
                bash setup_silver_tier.sh
            else
                echo "❌ setup_silver_tier.sh not found"
            fi
            ;;

        3)
            echo "🥇 Setting up Gold Tier..."
            if [ -f "setup_gold_tier.sh" ]; then
                bash setup_gold_tier.sh
            else
                echo "❌ setup_gold_tier.sh not found"
            fi
            ;;

        4)
            echo "💎 Setting up Platinum Tier..."
            if [ -f "setup_platinum_tier.sh" ]; then
                bash setup_platinum_tier.sh
            else
                echo "❌ setup_platinum_tier.sh not found"
            fi
            ;;

        5)
            echo "🚀 Quick Start Setup (Bronze + Gold)"
            echo ""
            echo "This will setup the most essential features:"
            echo "   • File monitoring (Bronze)"
            echo "   • WhatsApp monitoring (Gold)"
            echo ""
            read -p "Continue? (y/n) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                # Setup Bronze
                echo "📂 Setting up folders..."
                FOLDERS=("Inbox" "Needs_Action" "In_Progress" "Pending_Approval" "Approved" "Rejected" "Done" "Logs" "Briefings")
                for folder in "${FOLDERS[@]}"; do
                    mkdir -p "$folder" 2>/dev/null
                done

                # Setup Gold (WhatsApp)
                if [ -f "setup_gold_tier.sh" ]; then
                    bash setup_gold_tier.sh
                fi

                echo ""
                echo "✅ Quick Start complete!"
                echo ""
                echo "🚀 Start system:"
                echo "   python3 watchers/filesystem_watcher.py &"
                echo "   python3 watchers/whatsapp_watcher.py &"
            fi
            ;;

        6)
            echo "🔧 Complete Setup (All Tiers)"
            echo ""
            echo "This will setup ALL tiers in sequence:"
            echo "   1. Bronze → 2. Silver → 3. Gold → 4. Platinum"
            echo ""
            read -p "Continue? (y/n) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                # Bronze
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "🥉 STEP 1: BRONZE TIER"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                FOLDERS=("Inbox" "Needs_Action" "In_Progress" "Pending_Approval" "Approved" "Rejected" "Done" "Logs" "Briefings")
                for folder in "${FOLDERS[@]}"; do
                    mkdir -p "$folder" 2>/dev/null
                done
                echo "✅ Bronze complete!"

                # Silver
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "🥈 STEP 2: SILVER TIER"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                if [ -f "setup_silver_tier.sh" ]; then
                    bash setup_silver_tier.sh
                fi

                # Gold
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "🥇 STEP 3: GOLD TIER"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                if [ -f "setup_gold_tier.sh" ]; then
                    bash setup_gold_tier.sh
                fi

                # Platinum
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "💎 STEP 4: PLATINUM TIER"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                if [ -f "setup_platinum_tier.sh" ]; then
                    bash setup_platinum_tier.sh
                fi

                echo ""
                echo "🎉 Complete setup finished!"
            fi
            ;;

        7)
            clear
            echo "📊 SYSTEM STATUS CHECK"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""

            echo "🥉 BRONZE TIER:"
            check_status "Folders" "[ -d 'Inbox' ]"
            check_status "Watcher" "[ -f 'watchers/filesystem_watcher.py' ]"

            echo ""
            echo "🥈 SILVER TIER:"
            check_status "Gmail watcher" "[ -f 'watchers/gmail_watcher.py' ]"
            check_status "OAuth configured" "[ -f 'credentials.json' ]"
            check_status "Authenticated" "[ -f 'token.json' ]"

            echo ""
            echo "🥇 GOLD TIER:"
            check_status "WhatsApp watcher" "[ -f 'watchers/whatsapp_watcher.py' ]"
            check_status "Playwright" "pip list 2>/dev/null | grep -q playwright"
            check_status "Logged into WhatsApp" "[ -d '$HOME/.whatsapp_session' ]"

            echo ""
            echo "💎 PLATINUM TIER:"
            check_status "Cloud agent" "[ -f 'cloud-agent/vault_sync.py' ]"
            check_status "Git repo" "[ -d '.git' ]"

            echo ""
            echo "🏃 RUNNING PROCESSES:"
            if ps aux | grep -E "(filesystem_watcher|gmail_watcher|whatsapp_watcher|orchestrator)" | grep -v grep | wc -l | grep -q "^0$"; then
                echo "   ⚠️  No watchers currently running"
            else
                ps aux | grep -E "(filesystem_watcher|gmail_watcher|whatsapp_watcher|orchestrator)" | grep -v grep | awk '{print "   ✅", $11}'
            fi

            echo ""
            echo "📁 TASK COUNTS:"
            echo "   Inbox: $(ls -1 Inbox/ 2>/dev/null | wc -l) files"
            echo "   Needs_Action: $(find Needs_Action/ -name '*.md' 2>/dev/null | wc -l) tasks"
            echo "   Pending: $(find Pending_Approval/ -name '*.md' 2>/dev/null | wc -l) tasks"
            echo "   Done: $(find Done/ -name '*.md' 2>/dev/null | wc -l) tasks"
            ;;

        8)
            echo "📖 DOCUMENTATION FILES:"
            echo ""
            echo "   📋 START_HERE.md - Begin here!"
            echo "   📋 HOW_TO_START_ALL_TIERS.md - Complete commands"
            echo "   📋 MASTER_GUIDE.md - Full reference"
            echo "   📋 TIER_COMPLETION_REPORT.md - Status report"
            echo "   📋 URDU_COMPLETE_GUIDE.md - Urdu/Hindi guide"
            echo ""
            read -p "Open a file? (y/n) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo "Which file?"
                echo "  1. START_HERE.md"
                echo "  2. HOW_TO_START_ALL_TIERS.md"
                echo "  3. TIER_COMPLETION_REPORT.md"
                read -p "Choose (1-3): " -n 1 -r FILE_OPTION
                echo ""
                case $FILE_OPTION in
                    1) cat START_HERE.md | less ;;
                    2) cat HOW_TO_START_ALL_TIERS.md | less ;;
                    3) cat TIER_COMPLETION_REPORT.md | less ;;
                esac
            fi
            ;;

        9)
            echo "👋 Exiting setup"
            echo ""
            echo "📚 Documentation available:"
            echo "   cat START_HERE.md"
            echo "   cat HOW_TO_START_ALL_TIERS.md"
            echo ""
            echo "🚀 Quick start commands:"
            echo "   python3 watchers/filesystem_watcher.py &"
            echo "   python3 watchers/whatsapp_watcher.py &"
            echo ""
            exit 0
            ;;

        *)
            echo "❌ Invalid option. Please choose 1-9."
            ;;
    esac

    echo ""
    read -p "Press Enter to continue..."
done
