#!/bin/bash

# AI Employee - Cloud Agent Deployment Script
# Deploy to Oracle Cloud Free Tier / AWS / Any Linux VM

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     AI EMPLOYEE - PLATINUM TIER CLOUD DEPLOYMENT          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
VAULT_REPO="${VAULT_REPO:-https://github.com/yourusername/ai-employee-vault.git}"
VAULT_PATH="/opt/ai-employee-vault"
CLOUD_AGENT_PATH="/opt/ai-employee-cloud"
USER="ai-employee"

echo -e "${BLUE}[1/8] System Update${NC}"
sudo apt update && sudo apt upgrade -y

echo -e "${BLUE}[2/8] Installing Dependencies${NC}"
sudo apt install -y python3.13 python3-pip nodejs npm git

echo -e "${BLUE}[3/8] Creating AI Employee User${NC}"
if ! id "$USER" &>/dev/null; then
    sudo useradd -m -s /bin/bash $USER
    echo -e "${GREEN}✅ User created${NC}"
else
    echo -e "${YELLOW}⚠️  User already exists${NC}"
fi

echo -e "${BLUE}[4/8] Cloning Vault (Markdown only, no secrets)${NC}"
cd /opt
if [ ! -d "$VAULT_PATH" ]; then
    sudo git clone $VAULT_REPO $VAULT_PATH
    sudo chown -R $USER:$USER $VAULT_PATH
    echo -e "${GREEN}✅ Vault cloned${NC}"
else
    cd $VAULT_PATH
    sudo -u $USER git pull
    echo -e "${GREEN}✅ Vault updated${NC}"
fi

echo -e "${BLUE}[5/8] Setting up Cloud Agent${NC}"
sudo mkdir -p $CLOUD_AGENT_PATH
sudo cp -r $VAULT_PATH/cloud-agent/* $CLOUD_AGENT_PATH/
sudo chown -R $USER:$USER $CLOUD_AGENT_PATH

echo -e "${BLUE}[6/8] Installing Python Dependencies${NC}"
cd $CLOUD_AGENT_PATH
sudo -u $USER pip3 install -r requirements.txt

echo -e "${BLUE}[7/8] Installing PM2 (Process Manager)${NC}"
sudo npm install -g pm2

echo -e "${BLUE}[8/8] Setting up Systemd Service${NC}"
sudo tee /etc/systemd/system/ai-employee-cloud.service > /dev/null <<EOF
[Unit]
Description=AI Employee Cloud Agent
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$CLOUD_AGENT_PATH
ExecStart=/usr/bin/pm2 start ecosystem.config.js --no-daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ai-employee-cloud
sudo systemctl start ai-employee-cloud

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     CLOUD AGENT DEPLOYED SUCCESSFULLY! 🚀                  ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Next Steps:"
echo "  1. Configure environment variables: sudo nano $CLOUD_AGENT_PATH/.env"
echo "  2. Check status: sudo systemctl status ai-employee-cloud"
echo "  3. View logs: sudo journalctl -u ai-employee-cloud -f"
echo "  4. Setup Git sync from Local machine"
echo ""
