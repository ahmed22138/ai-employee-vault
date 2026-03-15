#!/usr/bin/env python3
"""
Gmail Watcher - Silver Tier Component
Monitors Gmail for important emails and creates action items
"""

import os
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from base_watcher import BaseWatcher

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    import pickle
except ImportError:
    print("Gmail API dependencies not installed. Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    exit(1)

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailWatcher(BaseWatcher):
    """Watches Gmail for new important emails and creates action items"""

    def __init__(self, vault_path: str, credentials_path: str = None):
        super().__init__(vault_path, check_interval=120)  # Check every 2 minutes

        # Credentials handling
        self.credentials_path = credentials_path or os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
        self.token_path = Path(vault_path) / '.gmail_token.pickle'

        # Track processed messages
        self.processed_ids_file = Path(vault_path) / '.gmail_processed_ids.txt'
        self.processed_ids = self._load_processed_ids()

        # Initialize Gmail service
        self.service = self._get_gmail_service()

        self.logger.info("Gmail Watcher initialized successfully")

    def _load_processed_ids(self) -> set:
        """Load previously processed message IDs"""
        if self.processed_ids_file.exists():
            with open(self.processed_ids_file, 'r') as f:
                return set(line.strip() for line in f)
        return set()

    def _save_processed_id(self, message_id: str):
        """Save a processed message ID"""
        self.processed_ids.add(message_id)
        with open(self.processed_ids_file, 'a') as f:
            f.write(f"{message_id}\n")

    def _get_gmail_service(self):
        """Authenticate and return Gmail API service"""
        creds = None

        # Load token if exists
        if self.token_path.exists():
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not Path(self.credentials_path).exists():
                    self.logger.error(f"Gmail credentials file not found at {self.credentials_path}")
                    self.logger.error("Please download credentials.json from Google Cloud Console")
                    self.logger.error("See: https://developers.google.com/gmail/api/quickstart/python")
                    raise FileNotFoundError(f"Gmail credentials not found: {self.credentials_path}")

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def check_for_updates(self) -> List[Dict]:
        """Check Gmail for new important emails"""
        try:
            # Search for unread important emails
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:important',
                maxResults=10
            ).execute()

            messages = results.get('messages', [])

            # Filter out already processed messages
            new_messages = [
                m for m in messages
                if m['id'] not in self.processed_ids
            ]

            self.logger.info(f"Found {len(new_messages)} new important emails")
            return new_messages

        except Exception as e:
            self.logger.error(f"Error checking Gmail: {e}")
            return []

    def create_action_file(self, message: Dict) -> Path:
        """Create action file for an email"""
        try:
            # Get full message details
            msg = self.service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()

            # Extract headers
            headers = {h['name']: h['value'] for h in msg['payload']['headers']}

            from_email = headers.get('From', 'Unknown')
            subject = headers.get('Subject', 'No Subject')
            date_received = headers.get('Date', datetime.now().isoformat())

            # Extract snippet (preview)
            snippet = msg.get('snippet', '')

            # Determine priority based on keywords
            priority = self._determine_priority(subject, snippet)

            # Create action file content
            content = f"""---
type: email
from: {from_email}
subject: {subject}
received: {date_received}
processed: {datetime.now().isoformat()}
priority: {priority}
status: pending
gmail_id: {message['id']}
---

## Email Content

**Subject:** {subject}
**From:** {from_email}
**Date:** {date_received}

**Preview:**
{snippet}

## Suggested Actions

- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Add to task list
- [ ] Archive after processing

## Notes

This email was flagged as important by Gmail. Please review and take appropriate action.

---
*Created by Gmail Watcher - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

            # Create file with safe filename
            safe_subject = "".join(c for c in subject[:50] if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = f"EMAIL_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_subject}.md"
            filepath = self.needs_action / filename

            filepath.write_text(content, encoding='utf-8')

            # Mark as processed
            self._save_processed_id(message['id'])

            self.logger.info(f"Created action file: {filename}")
            self.update_dashboard(f"📧 New email: {subject[:50]}")

            return filepath

        except Exception as e:
            self.logger.error(f"Error creating action file for email {message['id']}: {e}")
            return None

    def _determine_priority(self, subject: str, snippet: str) -> str:
        """Determine email priority based on content"""
        text = (subject + ' ' + snippet).lower()

        # High priority keywords
        high_priority_keywords = ['urgent', 'asap', 'important', 'critical', 'invoice', 'payment', 'deadline']
        if any(keyword in text for keyword in high_priority_keywords):
            return 'high'

        # Medium priority keywords
        medium_priority_keywords = ['meeting', 'call', 'review', 'feedback', 'question']
        if any(keyword in text for keyword in medium_priority_keywords):
            return 'medium'

        return 'low'

    def update_dashboard(self, activity: str):
        """Update Dashboard.md with new activity"""
        try:
            dashboard = self.vault_path / 'Dashboard.md'
            if not dashboard.exists():
                return

            content = dashboard.read_text(encoding='utf-8')

            # Add to recent activity
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            new_activity = f"- [{timestamp}] {activity}"

            # Insert after "## Recent Activity"
            if "## Recent Activity" in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip() == "## Recent Activity":
                        lines.insert(i + 1, new_activity)
                        break
                content = '\n'.join(lines)
                dashboard.write_text(content, encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Error updating dashboard: {e}")


def main():
    """Main entry point for Gmail Watcher"""
    # Get vault path from environment or use default
    vault_path = os.getenv('VAULT_PATH', '/mnt/e/all-d-files/Ai_Employee_Vault')

    # Get credentials path from environment
    credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH')

    # Create and run watcher
    watcher = GmailWatcher(vault_path, credentials_path)

    print(f"Gmail Watcher started - monitoring for important emails")
    print(f"Vault: {vault_path}")
    print(f"Check interval: {watcher.check_interval} seconds")
    print("Press Ctrl+C to stop")

    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\nGmail Watcher stopped by user")
    except Exception as e:
        print(f"\nError: {e}")
        raise


if __name__ == '__main__':
    main()
