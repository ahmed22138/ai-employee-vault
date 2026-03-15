#!/bin/bash

# AI Employee Configuration Setup Script
# This script helps you create and configure .env file

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Vault path
VAULT_PATH="/mnt/e/all-d-files/Ai_Employee_Vault"
cd "$VAULT_PATH"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     AI EMPLOYEE - CONFIGURATION SETUP                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env already exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file already exists!${NC}"
    echo ""
    read -p "Do you want to backup and create new? (y/N): " response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        backup_file=".env.backup.$(date +%Y%m%d_%H%M%S)"
        mv .env "$backup_file"
        echo -e "${GREEN}✅ Backed up to $backup_file${NC}"
    else
        echo "Exiting without changes."
        exit 0
    fi
fi

# Check if .env.example exists
if [ ! -f ".env.example" ]; then
    echo -e "${RED}❌ .env.example not found!${NC}"
    echo "Please ensure you're in the correct directory."
    exit 1
fi

echo -e "${BLUE}Creating .env from .env.example...${NC}"
cp .env.example .env
chmod 600 .env  # Secure permissions
echo -e "${GREEN}✅ .env file created${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Configuration Options:"
echo ""
echo "1. Quick Setup (Essential only - Gmail)"
echo "2. Full Setup (Interactive - all services)"
echo "3. Manual Edit (Open .env in editor)"
echo "4. Skip (Configure later)"
echo ""
read -p "Select option (1-4): " option

case $option in
    1)
        echo ""
        echo "🚀 Quick Setup - Essential Configuration"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""

        # SMTP Configuration
        echo "📧 Gmail SMTP Setup (for sending emails):"
        read -p "Enter your Gmail address: " smtp_user
        read -s -p "Enter your Gmail App Password (16 digits): " smtp_pass
        echo ""

        if [ -n "$smtp_user" ] && [ -n "$smtp_pass" ]; then
            sed -i "s/SMTP_USER=.*/SMTP_USER=$smtp_user/" .env
            sed -i "s/SMTP_PASSWORD=.*/SMTP_PASSWORD=$smtp_pass/" .env
            echo -e "${GREEN}✅ SMTP configured${NC}"
        else
            echo -e "${YELLOW}⚠️  SMTP not configured - skipped${NC}"
        fi

        echo ""
        echo -e "${GREEN}✅ Quick setup complete!${NC}"
        echo ""
        echo "📋 Next steps:"
        echo "   1. Get credentials.json from Google Cloud Console"
        echo "   2. Place it in: $VAULT_PATH/credentials.json"
        echo "   3. Run: python config_loader.py (to verify)"
        ;;

    2)
        echo ""
        echo "🎯 Full Setup - Interactive Configuration"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""

        # SMTP
        echo "📧 Gmail SMTP Setup:"
        read -p "Gmail address: " smtp_user
        read -s -p "Gmail App Password: " smtp_pass
        echo ""
        sed -i "s/SMTP_USER=.*/SMTP_USER=$smtp_user/" .env
        sed -i "s/SMTP_PASSWORD=.*/SMTP_PASSWORD=$smtp_pass/" .env

        # Odoo (optional)
        echo ""
        echo "💰 Odoo Setup (Optional - press Enter to skip):"
        read -p "Odoo URL: " odoo_url
        if [ -n "$odoo_url" ]; then
            read -p "Odoo Database: " odoo_db
            read -p "Odoo Username: " odoo_user
            read -s -p "Odoo Password: " odoo_pass
            echo ""
            sed -i "s|ODOO_URL=.*|ODOO_URL=$odoo_url|" .env
            sed -i "s/ODOO_DB=.*/ODOO_DB=$odoo_db/" .env
            sed -i "s/ODOO_USERNAME=.*/ODOO_USERNAME=$odoo_user/" .env
            sed -i "s/ODOO_PASSWORD=.*/ODOO_PASSWORD=$odoo_pass/" .env
            echo -e "${GREEN}✅ Odoo configured${NC}"
        fi

        # Facebook (optional)
        echo ""
        echo "📱 Facebook Setup (Optional - press Enter to skip):"
        read -p "Facebook Page Access Token: " fb_token
        if [ -n "$fb_token" ]; then
            read -p "Facebook Page ID: " fb_page_id
            sed -i "s/FACEBOOK_PAGE_ACCESS_TOKEN=.*/FACEBOOK_PAGE_ACCESS_TOKEN=$fb_token/" .env
            sed -i "s/FACEBOOK_PAGE_ID=.*/FACEBOOK_PAGE_ID=$fb_page_id/" .env
            echo -e "${GREEN}✅ Facebook configured${NC}"
        fi

        # Instagram (optional)
        echo ""
        echo "📸 Instagram Setup (Optional - press Enter to skip):"
        read -p "Instagram Business Account ID: " ig_id
        if [ -n "$ig_id" ]; then
            sed -i "s/INSTAGRAM_ACCOUNT_ID=.*/INSTAGRAM_ACCOUNT_ID=$ig_id/" .env
            echo -e "${GREEN}✅ Instagram configured${NC}"
        fi

        # Twitter (optional)
        echo ""
        echo "🐦 Twitter Setup (Optional - press Enter to skip):"
        read -p "Twitter API Key: " tw_key
        if [ -n "$tw_key" ]; then
            read -p "Twitter API Secret: " tw_secret
            read -p "Twitter Access Token: " tw_token
            read -p "Twitter Access Secret: " tw_access_secret
            sed -i "s/TWITTER_API_KEY=.*/TWITTER_API_KEY=$tw_key/" .env
            sed -i "s/TWITTER_API_SECRET=.*/TWITTER_API_SECRET=$tw_secret/" .env
            sed -i "s/TWITTER_ACCESS_TOKEN=.*/TWITTER_ACCESS_TOKEN=$tw_token/" .env
            sed -i "s/TWITTER_ACCESS_SECRET=.*/TWITTER_ACCESS_SECRET=$tw_access_secret/" .env
            echo -e "${GREEN}✅ Twitter configured${NC}"
        fi

        echo ""
        echo -e "${GREEN}✅ Full setup complete!${NC}"
        ;;

    3)
        echo ""
        echo "📝 Opening .env in editor..."

        # Try different editors
        if command -v nano &> /dev/null; then
            nano .env
        elif command -v vim &> /dev/null; then
            vim .env
        elif command -v vi &> /dev/null; then
            vi .env
        else
            echo -e "${YELLOW}⚠️  No editor found${NC}"
            echo "Edit manually: nano .env"
        fi
        ;;

    4)
        echo ""
        echo "Skipping configuration."
        echo "Edit manually: nano .env"
        ;;

    *)
        echo "Invalid option. Exiting."
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Important Files:"
echo "   • Configuration: .env (NEVER commit to git!)"
echo "   • Template: .env.example (safe to commit)"
echo "   • Git ignore: .gitignore (already configured)"
echo ""
echo "🔐 Security:"
echo "   • .env has secure permissions (600)"
echo "   • .env is in .gitignore"
echo "   • Never share .env file!"
echo ""
echo "✅ Next Steps:"
echo "   1. Verify config: python config_loader.py"
echo "   2. Get credentials.json (Gmail API)"
echo "   3. Install dependencies: pip install -r requirements.txt"
echo "   4. Start watchers: pm2 start watchers/*.py"
echo ""
echo "📖 Full guide: COMPLETE_GUIDE_URDU.md"
echo ""
