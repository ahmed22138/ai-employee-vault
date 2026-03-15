#!/usr/bin/env python3
"""
Cloud Email Triage Watcher - Platinum Tier
Monitors Gmail 24/7, creates draft replies (NEVER sends)
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from watchers.base_watcher import BaseWatcher

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CloudEmailTriageWatcher(BaseWatcher):
    """
    Cloud-based email triage watcher.

    **SECURITY**: This runs on CLOUD, so:
    - NEVER sends emails directly
    - Only creates draft replies
    - Writes approval requests for Local agent
    """

    def __init__(self, vault_path: str, credentials_path: str):
        super().__init__(vault_path, check_interval=120)  # Check every 2 minutes

        self.credentials_path = credentials_path
        self.service = None
        self.processed_ids = set()

        # Cloud-specific paths
        self.updates_folder = self.vault_path / 'Updates'
        self.updates_folder.mkdir(exist_ok=True)

        # Domain-specific folders
        self.email_needs_action = self.vault_path / 'Needs_Action' / 'email'
        self.email_plans = self.vault_path / 'Plans' / 'email'
        self.email_pending = self.vault_path / 'Pending_Approval' / 'email'

        for folder in [self.email_needs_action, self.email_plans, self.email_pending]:
            folder.mkdir(parents=True, exist_ok=True)

        self._init_gmail_service()

    def _init_gmail_service(self):
        """Initialize Gmail API service"""
        try:
            creds = Credentials.from_authorized_user_file(self.credentials_path)
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gmail service: {e}")
            raise

    def check_for_updates(self) -> list:
        """Check for new important emails"""
        try:
            # Query for unread important emails
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread (is:important OR label:important)'
            ).execute()

            messages = results.get('messages', [])
            new_messages = [m for m in messages if m['id'] not in self.processed_ids]

            return new_messages
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return []

    def create_action_file(self, message) -> Path:
        """Create draft reply and approval request (NEVER sends)"""
        try:
            # Get full message details
            msg = self.service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()

            # Extract headers
            headers = {h['name']: h['value'] for h in msg['payload']['headers']}
            sender = headers.get('From', 'Unknown')
            subject = headers.get('Subject', 'No Subject')

            # Get message body
            snippet = msg.get('snippet', '')

            # Create triage file in Updates/ for Cloud agent
            triage_file = self.updates_folder / f'EMAIL_TRIAGE_{message["id"]}.md'
            triage_content = f"""---
type: email_triage
agent: cloud
message_id: {message['id']}
from: {sender}
subject: {subject}
received: {datetime.now().isoformat()}
priority: high
status: triaged
---

## Email Content
{snippet}

## Cloud Agent Analysis
This email requires attention.

### Suggested Response
Based on the content, I suggest:
- Priority level: HIGH
- Response needed: YES
- Estimated urgency: Within 24 hours

### Draft Reply (Requires Local Approval)
A draft response has been prepared and saved to:
`/Pending_Approval/email/DRAFT_REPLY_{message["id"]}.md`

**SECURITY NOTE**: Cloud agent CANNOT send emails.
Local agent must review and approve before sending.
"""
            triage_file.write_text(triage_content)

            # Create draft reply in Pending_Approval for Local agent
            draft_file = self.email_pending / f'DRAFT_REPLY_{message["id"]}.md'
            draft_content = f"""---
type: draft_email_reply
created_by: cloud_agent
requires_local_approval: true
original_message_id: {message['id']}
to: {sender}
subject: Re: {subject}
status: awaiting_approval
---

## Draft Reply

Dear {sender.split('<')[0].strip()},

Thank you for your email regarding "{subject}".

[CLOUD AGENT NOTE: This is a draft. Local agent should review and customize before sending]

I have reviewed your message and will respond shortly.

Best regards,
[Your Name]

---

## To Approve and Send:
1. Review and edit the draft above
2. Move this file to /Approved/email/
3. Local agent will send via SMTP

## To Reject:
Move this file to /Rejected/email/
"""
            draft_file.write_text(draft_content)

            # Mark as processed
            self.processed_ids.add(message['id'])

            logger.info(f"✅ Triaged email from {sender}: {subject}")
            logger.info(f"   Draft created at: {draft_file}")

            return triage_file

        except Exception as e:
            logger.error(f"Error creating action file: {e}")
            return None


def main():
    """Main entry point"""
    logger.info("🌩️  Starting Cloud Email Triage Watcher (Platinum Tier)")

    # Get configuration from environment
    vault_path = os.getenv('VAULT_PATH', '/opt/ai-employee-vault')
    credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')

    # Verify we're in cloud mode
    if not os.getenv('CLOUD_MODE'):
        logger.warning("⚠️  CLOUD_MODE not set! Set export CLOUD_MODE=true")

    # Create watcher
    watcher = CloudEmailTriageWatcher(vault_path, credentials_path)

    # Run continuously
    watcher.run()


if __name__ == '__main__':
    main()
