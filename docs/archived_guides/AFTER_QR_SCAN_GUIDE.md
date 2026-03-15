# 📱 WhatsApp Setup Complete! - What's Next

**Status:** ✅ QR Code Scanned Successfully!
**Session:** ✅ Saved to ~/.whatsapp_session

---

## 🎉 Congratulations!

WhatsApp ab connected hai! Ab AI Employee WhatsApp messages monitor kar sakta hai.

---

## 🚀 How to Use WhatsApp Monitoring

### Option 1: Background Monitoring (Recommended)

**Start monitoring in background:**
```bash
python3 watchers/whatsapp_watcher.py &
```

**Check if running:**
```bash
ps aux | grep whatsapp_watcher
```

**Stop monitoring:**
```bash
pkill -f whatsapp_watcher
```

---

### Option 2: PM2 (24/7 Operation)

**Start with PM2:**
```bash
pm2 start watchers/whatsapp_watcher.py --interpreter python3 --name whatsapp
pm2 save
```

**Check status:**
```bash
pm2 status
pm2 logs whatsapp
```

**Stop:**
```bash
pm2 stop whatsapp
pm2 delete whatsapp
```

---

## 📨 How It Works

### 1. Monitoring Keywords

Script detects these urgent keywords:
- urgent
- asap
- emergency
- help
- invoice
- payment
- deadline
- important
- critical
- now

### 2. When Urgent Message Received

**Script automatically:**
1. ✅ Detects message with keyword
2. ✅ Creates action file in `Needs_Action/whatsapp/`
3. ✅ Updates Dashboard.md
4. ✅ Logs the activity

### 3. Action File Example

File: `Needs_Action/whatsapp/WHATSAPP_20260303_123456_John_Doe.md`

Contains:
- Sender name
- Message text
- Timestamp
- Priority level
- Suggested actions
- Notes

---

## 🧪 Testing

### Test 1: Send Urgent Message

**From another phone, send WhatsApp message:**
```
Hey, this is urgent! Please help with invoice.
```

**Check results:**
```bash
# Check action files
ls -lt Needs_Action/whatsapp/

# Check dashboard
cat Dashboard.md | grep WhatsApp

# Check logs
tail -f Logs/whatsapp_watcher_*.log
```

### Test 2: Normal Message (Should Ignore)

**Send message without keywords:**
```
Hello, how are you?
```

**Result:** No action file created (not urgent)

---

## 📊 Monitoring Status

### Check if monitoring is active:

```bash
# Check process
ps aux | grep whatsapp_watcher

# Check logs
tail -20 Logs/whatsapp_watcher_*.log

# Check session
ls -lh ~/.whatsapp_session/
```

---

## 🔄 Daily Usage

### Morning:
```bash
# Start monitoring
pm2 start whatsapp

# Check status
pm2 status
```

### During Day:
```bash
# Check for new action items
ls -lt Needs_Action/whatsapp/

# Check dashboard
cat Dashboard.md
```

### Evening:
```bash
# Review logs
pm2 logs whatsapp --lines 50

# Process action items
# Handle urgent messages
```

---

## 🎯 Expected Behavior

**Every 30 seconds, script:**
1. Checks WhatsApp Web
2. Looks for unread messages
3. Scans for urgent keywords
4. Creates action files for urgent items
5. Updates dashboard
6. Logs activity

**Session:**
- Saved after QR scan
- No need to scan again
- Valid until you logout manually

---

## 💡 Pro Tips

### Tip 1: Customize Keywords

Edit `watchers/whatsapp_watcher.py` line 36:
```python
self.keywords = [
    'urgent', 'asap', 'emergency', 'help', 'invoice',
    'payment', 'deadline', 'important', 'critical', 'now',
    'your-custom-keyword'  # Add your own
]
```

### Tip 2: Change Check Interval

Edit line 29:
```python
super().__init__(vault_path, check_interval=30)  # Change 30 to your value
```

### Tip 3: Auto-Start on Boot

```bash
# Save PM2 config
pm2 startup
pm2 save

# Now WhatsApp watcher starts automatically on reboot
```

---

## 🐛 Troubleshooting

### Problem: Session expired / Logged out

**Solution:**
```bash
# Delete old session
rm -rf ~/.whatsapp_session

# Scan QR code again
bash open_qr_code.sh
python3 watchers/whatsapp_watcher.py
```

### Problem: Not detecting messages

**Check:**
1. Is script running? `ps aux | grep whatsapp`
2. Are messages unread? (Script only checks unread)
3. Do messages contain keywords? (See keyword list above)

### Problem: Too many false positives

**Solution:** Remove common keywords from list
```python
# Remove 'help' if too generic
self.keywords = [
    'urgent', 'asap', 'emergency', 'invoice',
    'payment', 'deadline', 'critical'
]
```

---

## 📋 Quick Commands Reference

**Start monitoring:**
```bash
pm2 start watchers/whatsapp_watcher.py --interpreter python3 --name whatsapp
```

**Check status:**
```bash
pm2 status whatsapp
```

**View logs:**
```bash
pm2 logs whatsapp --lines 50
```

**Stop:**
```bash
pm2 stop whatsapp
```

**Restart:**
```bash
pm2 restart whatsapp
```

**Check action items:**
```bash
ls -lt Needs_Action/whatsapp/
```

**View dashboard:**
```bash
cat Dashboard.md
```

---

## ✅ Summary

**Setup Complete:**
- ✅ QR code scanned
- ✅ Session saved
- ✅ Script ready to monitor
- ✅ Keywords configured
- ✅ Action files will be created automatically

**Next Steps:**
1. Start monitoring: `pm2 start ...`
2. Send test message with "urgent"
3. Check `Needs_Action/whatsapp/` folder
4. Review Dashboard.md
5. Process action items!

---

**WhatsApp AI Employee is now ACTIVE!** 🎉

*Created: 2026-03-03*
*Status: Ready for production use*
