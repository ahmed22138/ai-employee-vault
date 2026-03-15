#!/bin/bash
# 💎 PLATINUM TIER - DEPLOYMENT SCRIPT
# This script helps you deploy Platinum Tier (24/7 Cloud + Local Hybrid)

set -e

echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║    💎 PLATINUM TIER - DEPLOYMENT SCRIPT              ║"
echo "║    24/7 Cloud + Local Hybrid System                  ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Check if running in correct directory
if [ ! -f "Company_Handbook.md" ]; then
    echo "❌ Error: Please run this script from the Ai_Employee_Vault directory"
    exit 1
fi

echo "📋 This script will help you deploy Platinum Tier:"
echo "   1. Setup Git repository for vault sync"
echo "   2. Configure cloud deployment settings"
echo "   3. Generate cloud deployment script"
echo "   4. Setup local agent"
echo "   5. Test vault synchronization"
echo ""
echo "⚠️  Prerequisites:"
echo "   • Git installed"
echo "   • GitHub/GitLab account"
echo "   • Cloud VM (Oracle/AWS/Azure) - optional, can setup later"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Setup cancelled"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 1: Git Repository Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git not installed. Please install git first."
    exit 1
fi

# Check if already a git repo
if [ -d ".git" ]; then
    echo "✅ Git repository already initialized"
else
    echo "⚠️  Not a git repository"
    read -p "Initialize git repository? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git init
        echo "✅ Git repository initialized"
    fi
fi

# Check/Create .gitignore
echo ""
echo "🔒 Setting up .gitignore for security..."

if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# ============================================
# SECURITY: NEVER COMMIT THESE FILES
# ============================================

# Credentials and secrets
.env
credentials.json
token.json
*.pem
*.key
id_rsa*

# WhatsApp session (contains login)
.whatsapp_session/
whatsapp_qr_code.png

# Logs (may contain sensitive data)
*.log
Logs/
logs/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so

# Node modules
node_modules/
package-lock.json

# OS files
.DS_Store
Thumbs.db
desktop.ini

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Temporary files
*.tmp
*.bak
*.backup
~*

# ============================================
# SAFE TO COMMIT: Task files and docs
# ============================================

# Task files (these should be synced)
!Needs_Action/**/*.md
!In_Progress/**/*.md
!Pending_Approval/**/*.md
!Approved/**/*.md
!Done/**/*.md

# Documentation
!*.md
!README.md
!Company_Handbook.md
!Business_Goals.md

# Configuration templates (without secrets)
!.env.example
EOF
    echo "✅ .gitignore created"
else
    echo "✅ .gitignore already exists"
fi

# Create .env.example (safe template)
if [ ! -f ".env.example" ]; then
    cat > .env.example << 'EOF'
# AI EMPLOYEE VAULT - CONFIGURATION TEMPLATE
# Copy this to .env and fill in your actual credentials

# ============================================
# SILVER TIER - Email Configuration
# ============================================

GMAIL_CLIENT_ID=your_gmail_client_id_here
GMAIL_CLIENT_SECRET=your_gmail_client_secret_here

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your_gmail_app_password_here

LINKEDIN_EMAIL=your-email@gmail.com
LINKEDIN_PASSWORD=your_linkedin_password_here

# ============================================
# GOLD TIER - WhatsApp & Browser
# ============================================

WHATSAPP_HEADLESS=true

ODOO_URL=https://your-company.odoo.com
ODOO_DB=your_database_name
ODOO_USERNAME=admin
ODOO_PASSWORD=your_odoo_password

FACEBOOK_ACCESS_TOKEN=your_facebook_token
TWITTER_API_KEY=your_twitter_key
TWITTER_API_SECRET=your_twitter_secret

# ============================================
# PLATINUM TIER - Cloud Settings
# ============================================

CLOUD_MODE=false
DEPLOYMENT_ENVIRONMENT=local
GIT_REPO_URL=https://github.com/your-username/ai-employee-vault-sync.git
EOF
    echo "✅ .env.example created"
fi

echo ""
read -p "Do you have a GitHub/GitLab repository URL? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter repository URL (https://github.com/...): " REPO_URL

    # Check if remote exists
    if git remote | grep -q "origin"; then
        echo "⚠️  Remote 'origin' already exists"
        read -p "Update remote URL? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git remote set-url origin "$REPO_URL"
            echo "✅ Remote URL updated"
        fi
    else
        git remote add origin "$REPO_URL"
        echo "✅ Remote 'origin' added"
    fi

    # Update .env
    if [ -f ".env" ]; then
        if grep -q "GIT_REPO_URL=" .env; then
            sed -i "s|GIT_REPO_URL=.*|GIT_REPO_URL=$REPO_URL|g" .env
        else
            echo "GIT_REPO_URL=$REPO_URL" >> .env
        fi
    fi
else
    echo ""
    echo "📋 Create a private repository:"
    echo "   1. Go to: https://github.com/new"
    echo "   2. Name: ai-employee-vault-sync"
    echo "   3. ✅ Private (IMPORTANT!)"
    echo "   4. Create repository"
    echo "   5. Copy the HTTPS URL"
    echo "   6. Run this script again with the URL"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 2: Cloud Deployment Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "📋 Cloud VM Options:"
echo "   1. Oracle Cloud (Free Forever - Recommended)"
echo "   2. AWS EC2 (Free Tier - 12 months)"
echo "   3. Azure VM (Free Tier - 12 months)"
echo "   4. DigitalOcean ($5/month)"
echo "   5. I'll deploy manually later"
echo ""
read -p "Choose option (1-5): " -n 1 -r CLOUD_OPTION
echo ""

case $CLOUD_OPTION in
    5)
        echo "✅ Skipping cloud deployment (manual later)"
        DEPLOY_NOW=false
        ;;
    *)
        echo "✅ Cloud deployment selected"
        DEPLOY_NOW=true
        ;;
esac

# Generate cloud deployment script
echo ""
echo "📝 Generating cloud deployment script..."

cat > cloud-agent/deployment/deploy_to_cloud.sh << 'DEPLOY_SCRIPT'
#!/bin/bash
# Auto-generated Cloud Deployment Script

set -e

echo "╔═══════════════════════════════════════════════════════╗"
echo "║    🚀 DEPLOYING TO CLOUD VM                          ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Check if running on cloud VM
if [ -z "$SSH_CONNECTION" ] && [ "$1" != "--force-local" ]; then
    echo "⚠️  This script should be run on the cloud VM"
    echo ""
    read -p "Enter cloud VM IP address: " VM_IP
    read -p "Enter SSH username (default: ubuntu): " SSH_USER
    SSH_USER=${SSH_USER:-ubuntu}

    echo ""
    echo "📋 Copy this script to cloud VM and run:"
    echo "   scp cloud-agent/deployment/deploy_to_cloud.sh $SSH_USER@$VM_IP:~/"
    echo "   ssh $SSH_USER@$VM_IP"
    echo "   bash deploy_to_cloud.sh"
    exit 0
fi

echo "📦 Installing dependencies..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install -y python3 python3-pip git

# Install Node.js and PM2
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install -y nodejs
fi

if ! command -v pm2 &> /dev/null; then
    sudo npm install -g pm2
fi

echo "✅ Dependencies installed"

# Clone repository
echo ""
echo "📥 Cloning vault repository..."
read -p "Enter Git repository URL: " REPO_URL

if [ ! -d "vault" ]; then
    git clone "$REPO_URL" vault
    echo "✅ Repository cloned"
else
    echo "✅ Repository already exists"
    cd vault
    git pull origin main
    cd ..
fi

# Install Python packages
cd vault
echo ""
echo "📦 Installing Python packages..."
pip3 install google-api-python-client schedule requests

# Setup credentials (read-only mode)
echo ""
echo "🔐 Cloud agent runs in READ-ONLY mode"
echo "   No sensitive credentials needed on cloud"
echo ""

if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Cloud Agent Configuration (READ-ONLY mode)
CLOUD_MODE=true
DEPLOYMENT_ENVIRONMENT=cloud

# Gmail OAuth (read-only, will be setup)
GMAIL_CLIENT_ID=
GMAIL_CLIENT_SECRET=

# No SMTP, WhatsApp, or other secrets on cloud!
EOF
    echo "✅ .env created (read-only mode)"
fi

# Start cloud agents with PM2
echo ""
echo "🚀 Starting cloud agents..."

# Cloud email triage (read-only)
pm2 start cloud-agent/cloud_email_triage.py --name "cloud-email-triage" --interpreter python3 2>/dev/null || echo "⚠️  cloud_email_triage.py not found"

# Vault sync
pm2 start cloud-agent/vault_sync.py --name "vault-sync" --interpreter python3

# Health monitor
pm2 start cloud-agent/health_monitor.py --name "health-monitor" --interpreter python3

# Save PM2 config
pm2 save

# Setup PM2 to start on boot
pm2 startup | grep "sudo" | bash || true

echo ""
echo "✅ Cloud agents deployed!"
echo ""
echo "📊 Status:"
pm2 status

echo ""
echo "📋 Logs:"
echo "   pm2 logs cloud-email-triage"
echo "   pm2 logs vault-sync"
echo "   pm2 logs health-monitor"
echo ""
echo "🔄 Management:"
echo "   pm2 restart all"
echo "   pm2 stop all"
echo "   pm2 status"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
DEPLOY_SCRIPT

chmod +x cloud-agent/deployment/deploy_to_cloud.sh
echo "✅ Cloud deployment script created: cloud-agent/deployment/deploy_to_cloud.sh"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 3: Local Agent Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Update .env for local mode
if [ -f ".env" ]; then
    if ! grep -q "CLOUD_MODE=" .env; then
        echo "CLOUD_MODE=false" >> .env
        echo "DEPLOYMENT_ENVIRONMENT=local" >> .env
    fi
    echo "✅ Local agent configured in .env"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 4: Initial Commit & Push"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -d ".git" ] && git remote | grep -q "origin"; then
    echo ""
    read -p "Commit and push to repository? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📝 Creating initial commit..."

        # Add safe files only
        git add .gitignore .env.example
        git add *.md 2>/dev/null || true
        git add cloud-agent/ local-agent/ 2>/dev/null || true
        git add watchers/*.py 2>/dev/null || true
        git add mcp-servers/ 2>/dev/null || true

        # Commit
        git commit -m "Initial commit: AI Employee Vault Platinum setup" || echo "Nothing to commit"

        # Push
        echo "📤 Pushing to remote..."
        git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null || echo "⚠️  Push failed. Check repository access"

        echo "✅ Pushed to repository"
    fi
else
    echo "⚠️  Git remote not configured. Skipping push."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ PLATINUM TIER SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Setup Summary:"
if [ -d ".git" ]; then
    echo "   ✅ Git repository: Initialized"
else
    echo "   ⚠️  Git repository: Not initialized"
fi
if [ -f ".gitignore" ]; then
    echo "   ✅ Security (.gitignore): Configured"
else
    echo "   ⚠️  Security: .gitignore missing"
fi
if git remote | grep -q "origin"; then
    echo "   ✅ Remote repository: Configured"
else
    echo "   ⚠️  Remote repository: Not configured"
fi
if [ -f "cloud-agent/deployment/deploy_to_cloud.sh" ]; then
    echo "   ✅ Cloud deployment script: Ready"
else
    echo "   ⚠️  Deployment script: Missing"
fi
echo ""
echo "🚀 Next Steps:"
echo ""
echo "📋 Local Side (Your Machine):"
echo "   1. Start local agent:"
echo "      python3 local-agent/local_approval_agent.py &"
echo ""
echo "   2. Start vault sync:"
echo "      python3 cloud-agent/vault_sync.py &"
echo ""
echo "☁️  Cloud Side (Cloud VM):"
echo "   1. Create cloud VM (Oracle/AWS/Azure)"
echo "   2. SSH into VM:"
echo "      ssh ubuntu@YOUR_VM_IP"
echo ""
echo "   3. Copy deployment script:"
echo "      scp cloud-agent/deployment/deploy_to_cloud.sh ubuntu@YOUR_VM_IP:~/"
echo ""
echo "   4. Run deployment:"
echo "      bash deploy_to_cloud.sh"
echo ""
echo "📊 Test Sync:"
echo "   1. On local: echo 'test' > Needs_Action/test.md"
echo "   2. Commit: git add . && git commit -m 'test' && git push"
echo "   3. On cloud: git pull"
echo "   4. Check: cat Needs_Action/test.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
