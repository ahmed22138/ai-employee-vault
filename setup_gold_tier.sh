#!/bin/bash
# 🥇 GOLD TIER - AUTOMATED SETUP SCRIPT
# This script helps you setup Gold Tier (WhatsApp + Browser Automation)

set -e

echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║    🥇 GOLD TIER - AUTOMATED SETUP                    ║"
echo "║    WhatsApp + Browser Automation                     ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Check if running in correct directory
if [ ! -f "Company_Handbook.md" ]; then
    echo "❌ Error: Please run this script from the Ai_Employee_Vault directory"
    exit 1
fi

echo "📋 This script will help you setup Gold Tier components:"
echo "   1. Install Playwright and browsers"
echo "   2. Setup WhatsApp Web login"
echo "   3. Configure optional integrations (Odoo, Social Media)"
echo "   4. Test WhatsApp monitoring"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Setup cancelled"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 1: Installing Playwright & Browsers"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if Playwright is installed
if ! pip list 2>/dev/null | grep -q "playwright"; then
    echo "⚠️  Playwright not installed"
    read -p "Install Playwright? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📦 Installing Playwright..."
        pip install playwright beautifulsoup4 httpx
        echo "✅ Playwright installed"
    fi
else
    echo "✅ Playwright already installed"
fi

# Check if browsers are installed
if [ ! -d "$HOME/.cache/ms-playwright" ]; then
    echo "⚠️  Playwright browsers not installed"
    read -p "Install Chromium browser? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📦 Installing Chromium browser..."
        python3 -m playwright install chromium
        echo "✅ Chromium installed"
    fi
else
    echo "✅ Playwright browsers already installed"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 2: WhatsApp Web Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if already logged in
if [ -d "$HOME/.whatsapp_session" ]; then
    echo "✅ WhatsApp session found (already logged in)"
    echo ""
    read -p "Do you want to re-login? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing old session..."
        rm -rf "$HOME/.whatsapp_session"
        echo "✅ Old session removed"
    else
        echo "✅ Using existing session"
    fi
fi

if [ ! -d "$HOME/.whatsapp_session" ]; then
    echo ""
    echo "📱 WhatsApp Web Login Methods:"
    echo ""
    echo "   1. QR Screenshot (Easiest - Recommended)"
    echo "   2. Browser Window (See QR on screen)"
    echo "   3. X Server (WSL Windows users)"
    echo ""
    read -p "Choose method (1/2/3): " -n 1 -r METHOD
    echo ""

    case $METHOD in
        1)
            echo ""
            echo "📸 QR Screenshot Method:"
            echo "   1. Starting WhatsApp watcher..."
            echo "   2. QR code will be saved as: whatsapp_qr_code.png"
            echo "   3. Scan it with your phone"
            echo ""
            read -p "Start WhatsApp watcher? (y/n) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo "🚀 Starting watcher..."
                timeout 15 python3 watchers/whatsapp_watcher.py 2>/dev/null &
                WATCHER_PID=$!

                echo "⏳ Waiting 10 seconds for QR code..."
                sleep 10

                if [ -f "whatsapp_qr_code.png" ]; then
                    echo "✅ QR code saved: whatsapp_qr_code.png"

                    # Try to open with different viewers
                    if command -v explorer.exe &> /dev/null; then
                        explorer.exe whatsapp_qr_code.png
                    elif command -v xdg-open &> /dev/null; then
                        xdg-open whatsapp_qr_code.png
                    elif command -v open &> /dev/null; then
                        open whatsapp_qr_code.png
                    else
                        echo "📋 Open manually: whatsapp_qr_code.png"
                    fi

                    echo ""
                    echo "📱 Scan the QR code with WhatsApp on your phone:"
                    echo "   WhatsApp → Settings → Linked Devices → Link a Device"
                    echo ""
                    read -p "Press Enter after scanning..."

                    # Kill watcher
                    kill $WATCHER_PID 2>/dev/null || true

                    # Check if session was created
                    if [ -d "$HOME/.whatsapp_session" ]; then
                        echo "✅ WhatsApp login successful!"
                    else
                        echo "⚠️  Session not detected. Try running: python3 watchers/whatsapp_watcher.py"
                    fi
                else
                    echo "⚠️  QR code not found. Try again: python3 watchers/whatsapp_watcher.py"
                fi
            fi
            ;;
        2)
            echo ""
            echo "🖥️  Browser Window Method:"
            echo "   Starting watcher with visible browser..."
            echo "   Scan QR code when browser opens"
            echo ""
            read -p "Start? (y/n) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                WHATSAPP_HEADLESS=false python3 watchers/whatsapp_watcher.py
            fi
            ;;
        3)
            echo ""
            echo "🚀 X Server Method (WSL):"
            echo ""
            echo "Prerequisites:"
            echo "   1. VcXsrv installed on Windows"
            echo "   2. XLaunch running with 'Disable access control' checked"
            echo ""
            read -p "Are prerequisites done? (y/n) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                export DISPLAY=:0
                echo "🔍 Testing X Server connection..."
                if command -v xeyes &> /dev/null; then
                    timeout 3 xeyes &
                    sleep 1
                    pkill xeyes 2>/dev/null || true
                    echo "✅ X Server working"
                else
                    echo "⚠️  xeyes not installed. Trying anyway..."
                fi

                echo "🚀 Starting WhatsApp watcher..."
                WHATSAPP_HEADLESS=false python3 watchers/whatsapp_watcher.py
            fi
            ;;
        *)
            echo "❌ Invalid choice"
            ;;
    esac
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 3: Optional Integrations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "Gold Tier includes optional integrations:"
echo "   • Odoo (Accounting/ERP)"
echo "   • Facebook (Social media posting)"
echo "   • Twitter (Social media posting)"
echo ""

read -p "Configure Odoo integration? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📋 Odoo Configuration:"
    read -p "Odoo URL (e.g., https://your-company.odoo.com): " ODOO_URL
    read -p "Database name: " ODOO_DB
    read -p "Username: " ODOO_USERNAME
    read -s -p "Password: " ODOO_PASSWORD
    echo ""

    # Update .env
    if [ -f ".env" ]; then
        sed -i "s|ODOO_URL=.*|ODOO_URL=$ODOO_URL|g" .env
        sed -i "s|ODOO_DB=.*|ODOO_DB=$ODOO_DB|g" .env
        sed -i "s|ODOO_USERNAME=.*|ODOO_USERNAME=$ODOO_USERNAME|g" .env
        sed -i "s|ODOO_PASSWORD=.*|ODOO_PASSWORD=$ODOO_PASSWORD|g" .env
        echo "✅ Odoo credentials saved to .env"
    fi
fi

echo ""
read -p "Configure Social Media (Facebook/Twitter)? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📋 Social Media Configuration:"
    echo "   You'll need API tokens from Facebook and Twitter"
    echo ""
    read -p "Facebook Access Token: " FB_TOKEN
    read -p "Twitter API Key: " TWITTER_KEY
    read -p "Twitter API Secret: " TWITTER_SECRET

    # Update .env
    if [ -f ".env" ]; then
        sed -i "s|FACEBOOK_ACCESS_TOKEN=.*|FACEBOOK_ACCESS_TOKEN=$FB_TOKEN|g" .env
        sed -i "s|TWITTER_API_KEY=.*|TWITTER_API_KEY=$TWITTER_KEY|g" .env
        sed -i "s|TWITTER_API_SECRET=.*|TWITTER_API_SECRET=$TWITTER_SECRET|g" .env
        echo "✅ Social media credentials saved to .env"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 4: Testing WhatsApp Monitoring"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -d "$HOME/.whatsapp_session" ]; then
    echo ""
    read -p "Test WhatsApp watcher now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🚀 Starting WhatsApp watcher for 30 seconds..."
        echo "   Send yourself a test message!"
        echo ""
        timeout 30 python3 watchers/whatsapp_watcher.py || true
        echo ""
        echo "📊 Checking for new messages..."
        NEW_MESSAGES=$(find Needs_Action/whatsapp/ -name "*.md" 2>/dev/null | wc -l)
        if [ $NEW_MESSAGES -gt 0 ]; then
            echo "✅ Found $NEW_MESSAGES new message(s)!"
            echo "   Files created in: Needs_Action/whatsapp/"
        else
            echo "⚠️  No new messages detected"
            echo "   The watcher is working, just no new messages"
        fi
    fi
else
    echo "⚠️  WhatsApp not logged in. Complete Step 2 first."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ GOLD TIER SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Setup Summary:"
if pip list 2>/dev/null | grep -q "playwright"; then
    echo "   ✅ Playwright: Installed"
else
    echo "   ⚠️  Playwright: Not installed"
fi
if [ -d "$HOME/.cache/ms-playwright" ]; then
    echo "   ✅ Browsers: Installed"
else
    echo "   ⚠️  Browsers: Not installed"
fi
if [ -d "$HOME/.whatsapp_session" ]; then
    echo "   ✅ WhatsApp: Logged in"
else
    echo "   ⚠️  WhatsApp: Not logged in"
fi
echo ""
echo "🚀 Start Gold Tier:"
echo "   python3 watchers/whatsapp_watcher.py &"
echo "   python3 watchers/error_recovery.py &"
echo "   python3 watchers/ralph_wiggum.py &"
echo ""
echo "📊 Check status:"
echo "   ps aux | grep -E '(whatsapp|error_recovery|ralph)' | grep -v grep"
echo ""
echo "📁 Check messages:"
echo "   ls -la Needs_Action/whatsapp/"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
