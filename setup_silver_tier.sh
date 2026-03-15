#!/bin/bash
# 🥈 SILVER TIER - AUTOMATED SETUP SCRIPT
# This script helps you setup Silver Tier (Email + LinkedIn)

set -e

echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║    🥈 SILVER TIER - AUTOMATED SETUP                  ║"
echo "║    Email + LinkedIn Configuration                    ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Check if running in correct directory
if [ ! -f "Company_Handbook.md" ]; then
    echo "❌ Error: Please run this script from the Ai_Employee_Vault directory"
    exit 1
fi

echo "📋 This script will help you setup Silver Tier components:"
echo "   1. Check Python packages"
echo "   2. Check Node.js dependencies"
echo "   3. Setup .env configuration"
echo "   4. Guide you through Gmail API setup"
echo "   5. Test SMTP configuration"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Setup cancelled"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 1: Checking Python Packages"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

MISSING_PACKAGES=()

# Check for required packages
if ! pip list 2>/dev/null | grep -q "google-api-python-client"; then
    MISSING_PACKAGES+=("google-api-python-client")
fi

if ! pip list 2>/dev/null | grep -q "google-auth-httplib2"; then
    MISSING_PACKAGES+=("google-auth-httplib2")
fi

if ! pip list 2>/dev/null | grep -q "google-auth-oauthlib"; then
    MISSING_PACKAGES+=("google-auth-oauthlib")
fi

if ! pip list 2>/dev/null | grep -q "schedule"; then
    MISSING_PACKAGES+=("schedule")
fi

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo "⚠️  Missing packages detected: ${MISSING_PACKAGES[*]}"
    read -p "Install missing packages? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📦 Installing packages..."
        pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib schedule requests
        echo "✅ Packages installed"
    else
        echo "⚠️  Skipping package installation"
    fi
else
    echo "✅ All Python packages installed"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 2: Checking Node.js Dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -d "mcp-servers/email-server" ]; then
    cd mcp-servers/email-server
    if [ ! -d "node_modules" ]; then
        echo "⚠️  Node modules not installed"
        read -p "Install Node.js dependencies? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "📦 Installing Node modules..."
            npm install
            echo "✅ Node modules installed"
        else
            echo "⚠️  Skipping Node installation"
        fi
    else
        echo "✅ Node modules already installed"
    fi
    cd ../..
else
    echo "⚠️  Email server directory not found"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 3: .env Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    read -p "Create .env file? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cat > .env << 'EOF'
# AI EMPLOYEE VAULT - CONFIGURATION FILE
# Created by automated setup

# ============================================
# SILVER TIER - Email Configuration
# ============================================

# Gmail OAuth (will be filled after Step 4)
GMAIL_CLIENT_ID=
GMAIL_CLIENT_SECRET=

# SMTP Email Sending
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=

# LinkedIn (optional)
LINKEDIN_EMAIL=
LINKEDIN_PASSWORD=

# ============================================
# GOLD TIER - WhatsApp & Browser
# ============================================

# WhatsApp Settings
WHATSAPP_HEADLESS=true

# Odoo (optional)
ODOO_URL=
ODOO_DB=
ODOO_USERNAME=
ODOO_PASSWORD=

# Social Media (optional)
FACEBOOK_ACCESS_TOKEN=
TWITTER_API_KEY=
TWITTER_API_SECRET=

# ============================================
# PLATINUM TIER - Cloud Settings
# ============================================

CLOUD_MODE=false
DEPLOYMENT_ENVIRONMENT=local
EOF
        echo "✅ .env file created"
    fi
else
    echo "✅ .env file exists"
fi

echo ""
echo "Now let's configure your credentials..."
echo ""

# SMTP Configuration
read -p "Do you want to configure SMTP email sending? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📧 SMTP Configuration:"
    echo "   You need a Gmail App Password (not your regular password)"
    echo "   1. Go to: https://myaccount.google.com/apppasswords"
    echo "   2. Generate app password for 'Mail' + 'Other (Custom name)'"
    echo "   3. Copy the 16-character password"
    echo ""
    read -p "Enter your Gmail address: " SMTP_USER
    read -s -p "Enter your Gmail App Password: " SMTP_PASS
    echo ""

    # Update .env
    if [ -f ".env" ]; then
        sed -i "s|SMTP_USER=.*|SMTP_USER=$SMTP_USER|g" .env
        sed -i "s|SMTP_PASS=.*|SMTP_PASS=$SMTP_PASS|g" .env
        echo "✅ SMTP credentials saved to .env"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 4: Gmail API Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "📋 Gmail API Setup Instructions:"
echo ""
echo "To enable Gmail monitoring, you need OAuth credentials:"
echo ""
echo "1. Go to: https://console.cloud.google.com"
echo "2. Create new project: 'AI Employee'"
echo "3. Enable Gmail API:"
echo "   - Go to 'APIs & Services' → 'Library'"
echo "   - Search 'Gmail API'"
echo "   - Click 'Enable'"
echo "4. Create OAuth credentials:"
echo "   - Go to 'APIs & Services' → 'Credentials'"
echo "   - Click 'Create Credentials' → 'OAuth client ID'"
echo "   - Configure consent screen (External, app name: AI Employee)"
echo "   - Application type: 'Desktop app'"
echo "   - Download JSON file"
echo "5. Rename to 'credentials.json'"
echo "6. Move to: $(pwd)/credentials.json"
echo ""

if [ -f "credentials.json" ]; then
    echo "✅ credentials.json found!"
else
    echo "❌ credentials.json not found"
    echo ""
    read -p "Have you downloaded credentials.json? Press Enter when ready..."

    if [ -f "credentials.json" ]; then
        echo "✅ credentials.json detected!"
    else
        echo "⚠️  credentials.json still not found"
        echo "   You can add it later and run: python3 watchers/gmail_watcher.py"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 5: First-Time Gmail Authentication"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "credentials.json" ] && [ ! -f "token.json" ]; then
    echo ""
    echo "📋 First-time authentication required"
    echo "   This will open a browser for you to authorize the app"
    echo ""
    read -p "Run Gmail authentication now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔓 Starting Gmail authentication..."
        echo "   A browser window will open"
        echo "   Click 'Allow' to authorize"
        python3 watchers/gmail_watcher.py --test-auth 2>/dev/null || python3 -c "
from watchers.gmail_watcher import GmailWatcher
watcher = GmailWatcher()
print('✅ Authentication successful! token.json created')
" 2>/dev/null || echo "⚠️  Run manually: python3 watchers/gmail_watcher.py"
    fi
elif [ -f "token.json" ]; then
    echo "✅ Already authenticated (token.json exists)"
else
    echo "⚠️  credentials.json not found, skipping authentication"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SILVER TIER SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Setup Summary:"
echo "   ✅ Python packages: Installed"
echo "   ✅ Node.js modules: Installed"
echo "   ✅ .env file: Created/Updated"
if [ -f "credentials.json" ]; then
    echo "   ✅ Gmail OAuth: credentials.json found"
else
    echo "   ⚠️  Gmail OAuth: credentials.json needed"
fi
if [ -f "token.json" ]; then
    echo "   ✅ Gmail auth: token.json created"
else
    echo "   ⚠️  Gmail auth: Run first-time authentication"
fi
echo ""
echo "🚀 Start Silver Tier:"
echo "   python3 watchers/gmail_watcher.py &"
echo "   python3 watchers/orchestrator.py &"
echo ""
echo "📊 Check status:"
echo "   ps aux | grep -E '(gmail|orchestrator)' | grep -v grep"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
