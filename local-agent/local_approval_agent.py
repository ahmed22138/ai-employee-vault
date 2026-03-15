#!/usr/bin/env python3
"""
Local Approval Agent - Platinum Tier
Watches /Approved folder and executes approved actions
ONLY runs locally with full credentials
"""

import os
import sys
import time
import logging
import smtplib
import shutil
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from config_loader import get

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ApprovalHandler(FileSystemEventHandler):
    """Handles approved actions"""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.approved_folder = vault_path / 'Approved'
        self.done_folder = vault_path / 'Done'
        self.logs_folder = vault_path / 'Logs'

        # Ensure folders exist
        for folder in [self.approved_folder, self.done_folder, self.logs_folder]:
            folder.mkdir(parents=True, exist_ok=True)

        # Load SMTP credentials (LOCAL only!)
        self.smtp_host = get('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(get('SMTP_PORT', '587'))
        self.smtp_user = get('SMTP_USER')
        self.smtp_password = get('SMTP_PASSWORD')

        if not self.smtp_user or not self.smtp_password:
            logger.error("❌ SMTP credentials not configured!")
            raise ValueError("SMTP credentials required for Local agent")

    def on_created(self, event):
        """Handle new files in Approved folder"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Only process .md files
        if file_path.suffix != '.md':
            return

        logger.info(f"📋 New approval detected: {file_path.name}")

        # Determine action type from frontmatter
        try:
            content = file_path.read_text()
            if 'type: draft_email_reply' in content:
                self._handle_email_send(file_path, content)
            elif 'type: social_media_post' in content:
                self._handle_social_post(file_path, content)
            elif 'type: payment' in content:
                self._handle_payment(file_path, content)
            else:
                logger.warning(f"⚠️  Unknown approval type: {file_path.name}")
        except Exception as e:
            logger.error(f"Error processing approval: {e}")

    def _handle_email_send(self, file_path: Path, content: str):
        """Send approved email via SMTP"""
        logger.info("📧 Processing email send approval...")

        try:
            # Parse frontmatter and content
            lines = content.split('---')
            if len(lines) < 3:
                raise ValueError("Invalid markdown format")

            # Extract metadata
            frontmatter = lines[1]
            body_content = lines[2]

            # Extract recipient and subject
            to_email = None
            subject = None
            for line in frontmatter.split('\n'):
                if line.startswith('to:'):
                    to_email = line.split(':', 1)[1].strip()
                elif line.startswith('subject:'):
                    subject = line.split(':', 1)[1].strip()

            if not to_email or not subject:
                raise ValueError("Missing to/subject in email draft")

            # Extract email body (everything after ## Draft Reply)
            body_start = body_content.find('## Draft Reply')
            if body_start == -1:
                raise ValueError("No draft reply found")

            email_body = body_content[body_start:]
            # Remove markdown headers
            email_body = email_body.replace('## Draft Reply\n\n', '')
            email_body = email_body.split('---')[0].strip()  # Remove footer notes

            # Send email via SMTP
            self._send_smtp_email(to_email, subject, email_body)

            # Log the action
            self._log_action('email_sent', {
                'to': to_email,
                'subject': subject,
                'file': file_path.name
            })

            # Move to Done
            done_path = self.done_folder / file_path.name
            shutil.move(str(file_path), str(done_path))

            logger.info(f"✅ Email sent to {to_email}")

        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
            # Move to Rejected
            rejected_folder = self.vault_path / 'Rejected'
            rejected_folder.mkdir(exist_ok=True)
            shutil.move(str(file_path), str(rejected_folder / file_path.name))

    def _send_smtp_email(self, to: str, subject: str, body: str):
        """Actually send email via SMTP"""
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = to
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)

    def _handle_social_post(self, file_path: Path, content: str):
        """Handle social media post approval"""
        logger.info("📱 Processing social media post approval...")
        # TODO: Implement social media posting via MCP
        logger.warning("⚠️  Social media posting not yet implemented")

    def _handle_payment(self, file_path: Path, content: str):
        """Handle payment approval"""
        logger.info("💰 Processing payment approval...")
        # TODO: Implement payment execution
        logger.warning("⚠️  Payment execution not yet implemented")

    def _log_action(self, action_type: str, details: dict):
        """Log approved action"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'actor': 'local_agent',
            'details': details
        }

        log_file = self.logs_folder / f'{datetime.now().strftime("%Y-%m-%d")}.json'

        # Append to log file
        import json
        logs = []
        if log_file.exists():
            logs = json.loads(log_file.read_text())
        logs.append(log_entry)
        log_file.write_text(json.dumps(logs, indent=2))


class LocalApprovalAgent:
    """Main Local Approval Agent"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.approved_folder = self.vault_path / 'Approved'
        self.approved_folder.mkdir(parents=True, exist_ok=True)

        self.observer = Observer()
        self.handler = ApprovalHandler(self.vault_path)

    def start(self):
        """Start watching Approved folder"""
        logger.info("🏠 Starting Local Approval Agent")
        logger.info(f"   Watching: {self.approved_folder}")
        logger.info("   Security: LOCAL ONLY (has full credentials)")

        self.observer.schedule(
            self.handler,
            str(self.approved_folder),
            recursive=True
        )
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            logger.info("Local Approval Agent stopped")

        self.observer.join()


def main():
    """Main entry point"""
    logger.info("🏠 Starting Local Approval Agent (Platinum Tier)")

    # Verify we're LOCAL (not cloud)
    if os.getenv('CLOUD_MODE'):
        logger.error("❌ FATAL: Local agent MUST NOT run in cloud!")
        logger.error("   Remove CLOUD_MODE environment variable")
        sys.exit(1)

    vault_path = os.getenv('VAULT_PATH', '/mnt/e/all-d-files/Ai_Employee_Vault')

    agent = LocalApprovalAgent(vault_path)
    agent.start()


if __name__ == '__main__':
    main()
