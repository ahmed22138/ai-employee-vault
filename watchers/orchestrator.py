#!/usr/bin/env python3
"""
Orchestrator - Silver Tier Component
Manages scheduling, folder watching, and process coordination
"""

import os
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime, time as dt_time
from typing import Dict, List
import json
import schedule

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Orchestrator')


class Orchestrator:
    """
    Main orchestrator for AI Employee system
    Handles scheduling, folder watching, and task coordination
    """

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.rejected = self.vault_path / 'Rejected'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.logs = self.vault_path / 'Logs'
        self.briefings = self.vault_path / 'Briefings'

        # Ensure directories exist
        for folder in [self.needs_action, self.pending_approval, self.approved,
                       self.rejected, self.done, self.plans, self.logs, self.briefings]:
            folder.mkdir(parents=True, exist_ok=True)

        logger.info(f"Orchestrator initialized for vault: {vault_path}")

    def check_needs_action(self):
        """Check Needs_Action folder for new tasks"""
        files = list(self.needs_action.glob('*.md'))

        if files:
            logger.info(f"Found {len(files)} tasks in Needs_Action folder")
            # Trigger Claude Code to process tasks
            self.trigger_claude_processing()
        else:
            logger.debug("No tasks in Needs_Action folder")

    def check_approved_actions(self):
        """Check Approved folder and execute approved actions"""
        files = list(self.approved.glob('*.md'))

        for file in files:
            try:
                content = file.read_text(encoding='utf-8')

                # Parse frontmatter to determine action type
                if '---' in content:
                    frontmatter = content.split('---')[1]

                    # Check if it's an email action
                    if 'action: send_email' in frontmatter or 'type: email' in frontmatter:
                        self.execute_email_action(file)
                    elif 'type: linkedin_post' in frontmatter:
                        self.execute_linkedin_action(file)
                    else:
                        logger.info(f"Unknown action type in {file.name}, moving to Done")
                        self.move_to_done(file)

            except Exception as e:
                logger.error(f"Error processing approved file {file.name}: {e}")

    def execute_email_action(self, file: Path):
        """Execute an approved email action via MCP"""
        try:
            logger.info(f"Executing email action: {file.name}")

            # Parse email details from file
            content = file.read_text(encoding='utf-8')

            # Extract details (basic parsing)
            # In a real implementation, this would be more robust
            lines = content.split('\n')
            to = subject = body = None

            for i, line in enumerate(lines):
                if line.startswith('to:'):
                    to = line.split('to:')[1].strip()
                elif line.startswith('subject:'):
                    subject = line.split('subject:')[1].strip()
                elif '## Email Content' in line or '## Body' in line:
                    # Get content after this header
                    body = '\n'.join(lines[i+1:])
                    break

            if not all([to, subject, body]):
                logger.error(f"Missing email details in {file.name}")
                return

            # Call email MCP server (this is a simplified version)
            # In production, this would use the actual MCP protocol
            logger.info(f"Sending email to {to}: {subject}")

            # Log the action
            self.log_action('email_send', {
                'to': to,
                'subject': subject,
                'file': file.name,
                'timestamp': datetime.now().isoformat()
            })

            # Move to Done
            self.move_to_done(file)

            logger.info(f"Email action completed: {file.name}")

        except Exception as e:
            logger.error(f"Error executing email action {file.name}: {e}")

    def execute_linkedin_action(self, file: Path):
        """Execute an approved LinkedIn post action"""
        try:
            logger.info(f"Executing LinkedIn action: {file.name}")

            # For Silver tier, LinkedIn posting is manual
            # This just logs the action and provides the post content
            content = file.read_text(encoding='utf-8')

            logger.info(f"LinkedIn post ready for manual posting: {file.name}")
            logger.info("Content saved in file - user should manually post to LinkedIn")

            # Log the action
            self.log_action('linkedin_post', {
                'file': file.name,
                'timestamp': datetime.now().isoformat(),
                'status': 'manual_posting_required'
            })

            # Move to Done (user will post manually)
            self.move_to_done(file)

        except Exception as e:
            logger.error(f"Error executing LinkedIn action {file.name}: {e}")

    def move_to_done(self, file: Path):
        """Move a file to the Done folder"""
        try:
            dest = self.done / file.name
            # Handle duplicates
            if dest.exists():
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                dest = self.done / f"{file.stem}_{timestamp}{file.suffix}"

            file.rename(dest)
            logger.info(f"Moved to Done: {file.name}")
        except Exception as e:
            logger.error(f"Error moving {file.name} to Done: {e}")

    def trigger_claude_processing(self):
        """Trigger Claude Code to process tasks"""
        try:
            # This would launch Claude Code with a specific prompt
            # For now, we just log it
            logger.info("Triggering Claude Code to process Needs_Action folder")

            # In production, this might run:
            # subprocess.run(['claude', 'code', '--prompt', 'Process all tasks in Needs_Action folder'])

        except Exception as e:
            logger.error(f"Error triggering Claude: {e}")

    def log_action(self, action_type: str, details: Dict):
        """Log an action to the daily log file"""
        try:
            log_date = datetime.now().strftime('%Y-%m-%d')
            log_file = self.logs / f'{log_date}_actions.json'

            # Load existing log or create new
            if log_file.exists():
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {'date': log_date, 'actions': []}

            # Add new action
            log_data['actions'].append({
                'timestamp': datetime.now().isoformat(),
                'type': action_type,
                'details': details
            })

            # Save log
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)

            logger.debug(f"Logged {action_type} action")

        except Exception as e:
            logger.error(f"Error logging action: {e}")

    def generate_weekly_briefing(self):
        """Generate Monday Morning CEO Briefing"""
        try:
            logger.info("Generating weekly CEO briefing")

            # This would be a comprehensive task that:
            # 1. Reads Business_Goals.md
            # 2. Analyzes Done/ folder for completed tasks
            # 3. Checks logs for metrics
            # 4. Creates a briefing in Briefings/ folder

            # For now, create a placeholder
            briefing_date = datetime.now().strftime('%Y-%m-%d')
            briefing_file = self.briefings / f'{briefing_date}_Monday_Briefing.md'

            if briefing_file.exists():
                logger.info("Briefing already exists for today")
                return

            content = f"""# Monday Morning CEO Briefing

---
generated: {datetime.now().isoformat()}
period: Last 7 days
---

## Executive Summary

Weekly briefing generated automatically by AI Employee system.

## This Week's Activity

(Analysis would be generated here by Claude Code)

## Action Items

- Review pending approvals in /Pending_Approval
- Check completed tasks in /Done
- Update Business_Goals.md if needed

---
*Generated by Orchestrator v1.0*
"""

            briefing_file.write_text(content, encoding='utf-8')
            logger.info(f"Weekly briefing created: {briefing_file.name}")

            # Trigger Claude to fill in the details
            self.trigger_claude_processing()

        except Exception as e:
            logger.error(f"Error generating weekly briefing: {e}")

    def setup_schedules(self):
        """Setup scheduled tasks"""
        logger.info("Setting up scheduled tasks")

        # Check Needs_Action folder every 5 minutes
        schedule.every(5).minutes.do(self.check_needs_action)

        # Check Approved folder every 2 minutes
        schedule.every(2).minutes.do(self.check_approved_actions)

        # Generate weekly briefing every Monday at 7 AM
        schedule.every().monday.at("07:00").do(self.generate_weekly_briefing)

        # Daily health check at 6 AM
        schedule.every().day.at("06:00").do(self.health_check)

        logger.info("Schedules configured:")
        logger.info("  - Check Needs_Action: Every 5 minutes")
        logger.info("  - Check Approved: Every 2 minutes")
        logger.info("  - Weekly briefing: Monday 7:00 AM")
        logger.info("  - Health check: Daily 6:00 AM")

    def health_check(self):
        """Perform system health check"""
        logger.info("Performing health check")

        # Check if all required folders exist
        for folder in [self.needs_action, self.pending_approval, self.approved,
                       self.done, self.logs, self.briefings]:
            if not folder.exists():
                logger.warning(f"Folder missing: {folder}")
                folder.mkdir(parents=True, exist_ok=True)

        # Check for stale tasks (pending approval > 7 days)
        try:
            import time as time_module
            current_time = time_module.time()
            week_ago = current_time - (7 * 24 * 60 * 60)

            stale_files = []
            for file in self.pending_approval.glob('*.md'):
                if file.stat().st_mtime < week_ago:
                    stale_files.append(file.name)

            if stale_files:
                logger.warning(f"Found {len(stale_files)} stale approval requests")
                for file in stale_files:
                    logger.warning(f"  - {file}")

        except Exception as e:
            logger.error(f"Error checking for stale tasks: {e}")

        logger.info("Health check complete")

    def run(self):
        """Main run loop"""
        logger.info("Orchestrator starting...")
        self.setup_schedules()

        logger.info("Orchestrator running. Press Ctrl+C to stop.")

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Orchestrator stopped by user")


def main():
    """Main entry point"""
    vault_path = os.getenv('VAULT_PATH', '/mnt/e/all-d-files/Ai_Employee_Vault')

    orchestrator = Orchestrator(vault_path)
    orchestrator.run()


if __name__ == '__main__':
    main()
