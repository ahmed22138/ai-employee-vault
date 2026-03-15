#!/bin/bash

# WhatsApp Monitoring Starter

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     📱 Starting WhatsApp Monitoring...                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

cd /mnt/e/all-d-files/Ai_Employee_Vault

# Check if already running
if pgrep -f "whatsapp_watcher.py" > /dev/null; then
    echo "⚠️  WhatsApp watcher already running!"
    echo ""
    echo "Process ID: $(pgrep -f whatsapp_watcher.py)"
    echo ""
    echo "To stop: pkill -f whatsapp_watcher"
    echo "To restart: pkill -f whatsapp_watcher && bash start_whatsapp_monitoring.sh"
    exit 1
fi

# Start in background
echo "🚀 Starting WhatsApp monitoring in background..."
nohup python3 watchers/whatsapp_watcher.py > Logs/whatsapp_monitor.log 2>&1 &

# Get process ID
WPID=$!

sleep 2

# Check if started successfully
if ps -p $WPID > /dev/null; then
    echo "✅ WhatsApp monitoring started successfully!"
    echo ""
    echo "Process ID: $WPID"
    echo "Log file: Logs/whatsapp_monitor.log"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 Useful Commands:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Check status:"
    echo "  ps aux | grep whatsapp_watcher"
    echo ""
    echo "View logs (live):"
    echo "  tail -f Logs/whatsapp_monitor.log"
    echo ""
    echo "Stop monitoring:"
    echo "  pkill -f whatsapp_watcher"
    echo ""
    echo "Check action items:"
    echo "  ls -lt Needs_Action/whatsapp/"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "✅ Monitoring active! Messages will be checked every 30 seconds."
    echo ""
else
    echo "❌ Failed to start monitoring!"
    echo "Check: Logs/whatsapp_monitor.log"
fi
