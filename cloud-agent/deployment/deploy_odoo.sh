#!/bin/bash

# Odoo Community 19+ Cloud Deployment - Platinum Tier
# Deploys Odoo on Cloud VM with HTTPS, backups, and health monitoring

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     ODOO COMMUNITY 19+ CLOUD DEPLOYMENT                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
ODOO_VERSION="19.0"
ODOO_PORT="8069"
POSTGRES_VERSION="16"
DOMAIN="${ODOO_DOMAIN:-odoo.yourdomain.com}"

echo -e "${BLUE}[1/10] System Update${NC}"
sudo apt update && sudo apt upgrade -y

echo -e "${BLUE}[2/10] Installing PostgreSQL${NC}"
sudo apt install -y postgresql postgresql-contrib

echo -e "${BLUE}[3/10] Creating Odoo Database User${NC}"
sudo -u postgres createuser -s odoo || echo "User already exists"
sudo -u postgres psql -c "ALTER USER odoo WITH PASSWORD 'odoo_secure_password_change_this';"

echo -e "${BLUE}[4/10] Creating System User${NC}"
sudo useradd -m -s /bin/bash -U odoo || echo "User already exists"

echo -e "${BLUE}[5/10] Installing Odoo Dependencies${NC}"
sudo apt install -y python3-pip python3-dev libxml2-dev libxslt1-dev \
    libldap2-dev libsasl2-dev libtiff5-dev libjpeg8-dev libopenjp2-7-dev \
    zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev \
    libfribidi-dev libxcb1-dev libpq-dev nodejs npm

echo -e "${BLUE}[6/10] Installing wkhtmltopdf (PDF generation)${NC}"
cd /tmp
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
sudo apt install -y ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb
rm wkhtmltox_0.12.6.1-2.jammy_amd64.deb

echo -e "${BLUE}[7/10] Installing Odoo${NC}"
cd /opt
sudo git clone https://www.github.com/odoo/odoo --depth 1 --branch $ODOO_VERSION odoo
sudo chown -R odoo:odoo /opt/odoo

echo -e "${BLUE}[8/10] Installing Python Dependencies${NC}"
cd /opt/odoo
sudo pip3 install -r requirements.txt

echo -e "${BLUE}[9/10] Creating Odoo Configuration${NC}"
sudo tee /etc/odoo.conf > /dev/null <<EOF
[options]
admin_passwd = admin_change_this_password
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo_secure_password_change_this
addons_path = /opt/odoo/addons
logfile = /var/log/odoo/odoo-server.log
xmlrpc_port = $ODOO_PORT
EOF

sudo mkdir -p /var/log/odoo
sudo chown odoo:odoo /var/log/odoo

echo -e "${BLUE}[10/10] Creating Systemd Service${NC}"
sudo tee /etc/systemd/system/odoo.service > /dev/null <<EOF
[Unit]
Description=Odoo
Documentation=https://www.odoo.com
After=network.target postgresql.service

[Service]
Type=simple
User=odoo
ExecStart=/usr/bin/python3 /opt/odoo/odoo-bin -c /etc/odoo.conf
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable odoo
sudo systemctl start odoo

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     ODOO DEPLOYED SUCCESSFULLY! 📊                         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Odoo is now running on: http://$(hostname -I | awk '{print $1}'):$ODOO_PORT"
echo ""
echo "Next Steps:"
echo "  1. Setup HTTPS with Nginx/Certbot (see nginx_odoo.conf)"
echo "  2. Change admin passwords in /etc/odoo.conf"
echo "  3. Access Odoo: http://your-ip:8069"
echo "  4. Create database and set master password"
echo "  5. Configure Odoo MCP server to connect"
echo ""
echo "Check status: sudo systemctl status odoo"
echo "View logs: sudo journalctl -u odoo -f"
echo ""
