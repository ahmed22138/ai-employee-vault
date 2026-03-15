# Quick Start Guide - AI Employee Bronze Tier

## Welcome! 🎉
You've successfully set up the Bronze Tier of your Personal AI Employee. This guide will help you get started immediately.

## What You Have Now
✅ Complete folder structure for task management
✅ Dashboard for monitoring your AI Employee
✅ Company Handbook with operational rules
✅ File System Watcher (Python script)
✅ Vault Manager Agent Skill
✅ All Bronze Tier requirements met

## 3-Minute Quick Start

### Step 1: Install Dependencies (1 minute)
```bash
# Make sure you're in the Ai_Employee_Vault directory
pip install -r requirements.txt
```

### Step 2: Start the File Watcher (30 seconds)
Open a new terminal and run:
```bash
cd watchers
python filesystem_watcher.py
```

Keep this terminal open. The watcher is now monitoring your Inbox folder!

### Step 3: Test the System (1 minute)
In another terminal or file explorer:
1. Create a test file (any file - txt, pdf, image, etc.)
2. Drop it into the `Inbox/` folder
3. Watch the watcher terminal - you'll see it detect the file!
4. Check `Needs_Action/` folder - a new action item was created!

### Step 4: Use Claude Code (30 seconds)
In your Claude Code terminal (this one):
```
"Read the file in Needs_Action folder and process it"
```

Claude will read the task and can help you:
- Categorize the file
- Move it to the appropriate location
- Update the Dashboard
- Complete the task

## Daily Workflow

### Morning Routine
1. Check Dashboard.md for overnight activity
2. Review Needs_Action folder for new tasks
3. Process or delegate tasks to Claude
4. Check Pending_Approval for any items needing your review

### During the Day
- Drop files into Inbox as they come in
- Let the watcher detect and create tasks automatically
- Ask Claude to "process pending tasks" periodically
- Review and approve sensitive actions in Pending_Approval

### Evening Routine
```
Ask Claude: "Generate a daily summary of activities"
```

## Useful Claude Prompts

### Task Management
- "Check Needs_Action and summarize pending tasks"
- "Process all pending tasks"
- "Move completed task X to Done folder"
- "Create an approval request for [action]"

### Dashboard & Reports
- "Update the Dashboard with current status"
- "Generate a daily summary"
- "Show me what was completed this week"
- "What needs my attention?"

### Organization
- "Organize files in Needs_Action by priority"
- "Clean up old completed tasks"
- "Check for any urgent items"

## Using the Vault Manager Skill

The Vault Manager skill helps Claude understand how to manage your AI Employee system.

To use it:
```
"Using the vault-manager skill, process all pending tasks"
```

This gives Claude specific context about:
- How to process tasks
- When to request approval
- How to update the Dashboard
- Organizational rules from Company_Handbook

## File Organization Tips

### Inbox/
- Drop ANY file here
- Watcher creates action items automatically
- Files stay here until you process them

### Needs_Action/
- Review these regularly
- Process with Claude's help
- Move to Done when complete

### Pending_Approval/
- IMPORTANT: Review these daily!
- Move to Approved/ to proceed
- Move to Rejected/ to cancel

### Done/
- Archive of completed tasks
- Can be cleaned up monthly
- Useful for generating reports

## Troubleshooting

### Watcher isn't detecting files
- Make sure filesystem_watcher.py is running
- Check you're dropping files in Inbox/ (not subfolders)
- Look at Logs/ folder for error messages

### Claude can't find files
- Ensure you're in the Ai_Employee_Vault directory
- Use absolute paths or relative paths from vault root
- Check file permissions

### Need help?
1. Check README.md for detailed documentation
2. Review Company_Handbook.md for rules
3. Look at the hackathon PDF for architecture details

## Next Steps

### Customize Your Setup
1. Edit Company_Handbook.md with your specific rules
2. Add your own categories and priorities
3. Customize the Dashboard layout
4. Create additional Agent Skills for your workflow

### Upgrade to Silver Tier
When ready, add:
- Gmail Watcher for email automation
- WhatsApp Watcher for message monitoring
- MCP servers for external actions
- Automated LinkedIn posting
- Human-in-the-loop approval workflows

### Monitor & Improve
- Review Dashboard daily
- Check Logs for patterns
- Adjust Company_Handbook rules as needed
- Track time saved vs manual work

## Example: Complete Task Flow

1. **File arrives**: Someone emails you a PDF, you save it to Inbox/
2. **Watcher detects**: Creates action item in Needs_Action/
3. **Claude processes**: You ask "What's new in Needs_Action?"
4. **Claude analyzes**: Reads the PDF, understands content
5. **Action needed**: Claude determines this needs approval to email back
6. **Approval request**: Created in Pending_Approval/
7. **You approve**: Move file to Approved/
8. **Claude executes**: (Would send email in Silver tier with MCP)
9. **Task complete**: Moved to Done/, Dashboard updated
10. **Logged**: Full audit trail in Logs/

## Success Metrics

Track your AI Employee's effectiveness:
- Files processed per day
- Time saved on routine tasks
- Response time to incoming items
- Approval accuracy rate

Check Dashboard weekly to see progress!

## Community & Support

- **Weekly Meetings**: Wednesday 10 PM (Zoom link in hackathon PDF)
- **Documentation**: See README.md and hackathon PDF
- **Share Progress**: Submit your implementation via the form

---

## You're Ready! 🚀

Your Bronze Tier AI Employee is fully operational. Start by:
1. Running the file watcher
2. Dropping a test file in Inbox
3. Asking Claude to process it

Welcome to the future of personal automation!

---
*Last Updated: 2026-02-20*
*Version: Bronze Tier 1.0*
