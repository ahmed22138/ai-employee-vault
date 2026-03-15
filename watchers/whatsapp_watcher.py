#!/usr/bin/env python3
"""
WhatsApp Watcher - Gold Tier Component
Monitors WhatsApp Web for urgent messages using Playwright
"""

import os
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from base_watcher import BaseWatcher

try:
    from playwright.sync_api import sync_playwright, Browser, Page
except ImportError:
    print("Playwright not installed. Run: pip install playwright && playwright install chromium")
    exit(1)


class WhatsAppWatcher(BaseWatcher):
    """
    Watches WhatsApp Web for urgent messages and creates action items
    Uses Playwright for browser automation
    """

    def __init__(self, vault_path: str, session_path: str = None):
        super().__init__(vault_path, check_interval=30)  # Check every 30 seconds

        # Session persistence (for staying logged in)
        self.session_path = Path(session_path) if session_path else Path.home() / '.whatsapp_session'
        self.session_path.mkdir(parents=True, exist_ok=True)

        # Urgent keywords to monitor
        self.keywords = [
            'urgent', 'asap', 'emergency', 'help', 'invoice',
            'payment', 'deadline', 'important', 'critical', 'now'
        ]

        # Track processed messages
        self.processed_messages_file = Path(vault_path) / '.whatsapp_processed_messages.txt'
        self.processed_messages = self._load_processed_messages()

        self.browser = None
        self.page = None
        self.is_on_whatsapp = False  # Track if we're already on WhatsApp Web

        self.logger.info("WhatsApp Watcher initialized")

    def _load_processed_messages(self) -> set:
        """Load previously processed message identifiers"""
        if self.processed_messages_file.exists():
            with open(self.processed_messages_file, 'r') as f:
                return set(line.strip() for line in f)
        return set()

    def _save_processed_message(self, message_id: str):
        """Save a processed message ID"""
        self.processed_messages.add(message_id)
        with open(self.processed_messages_file, 'a') as f:
            f.write(f"{message_id}\n")

    def _init_browser(self):
        """Initialize Playwright browser with persistent session"""
        try:
            playwright = sync_playwright().start()

            # Check if headless mode is disabled (for QR code scanning)
            headless_mode = os.getenv('WHATSAPP_HEADLESS', 'true').lower() == 'true'

            # Use persistent context to maintain WhatsApp login
            self.browser = playwright.chromium.launch_persistent_context(
                str(self.session_path),
                headless=headless_mode,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )

            self.page = self.browser.pages[0] if self.browser.pages else self.browser.new_page()

            self.logger.info("Browser initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize browser: {e}")
            return False

    def _ensure_logged_in(self) -> bool:
        """Ensure WhatsApp Web is logged in"""
        try:
            # Only navigate to WhatsApp Web if not already there
            if not self.is_on_whatsapp:
                self.logger.info("Navigating to WhatsApp Web for the first time...")
                self.page.goto('https://web.whatsapp.com', timeout=60000)
                self.is_on_whatsapp = True

            # Wait for either QR code or chat list (without reloading)
            # Try multiple selectors as WhatsApp Web changes their HTML structure
            try:
                # Try different selectors for logged-in state
                selectors_to_try = [
                    '[data-testid="chat-list"]',  # Old selector
                    '#pane-side',  # Sidebar with chats
                    '[aria-label="Chat list"]',  # Accessibility label
                    'div[role="grid"]',  # Chat grid
                ]

                for selector in selectors_to_try:
                    try:
                        self.page.wait_for_selector(selector, timeout=2000)
                        self.logger.info(f"WhatsApp Web logged in successfully (detected via: {selector})")
                        return True
                    except:
                        continue

                # If none worked, assume not logged in
                raise Exception("No login selectors found")
            except:
                # QR code present (not logged in)
                self.logger.warning("WhatsApp Web not logged in - QR code scan required")

                # Take screenshot of QR code for user to see (only once per minute to avoid spam)
                try:
                    screenshot_path = Path(self.vault_path) / "whatsapp_qr_code.png"
                    self.page.screenshot(path=str(screenshot_path))
                    self.logger.info(f"QR code screenshot saved to: {screenshot_path}")
                    print(f"\n📸 QR CODE SAVED: {screenshot_path}")
                    print(f"   Open this image file and scan with your phone!")
                    print(f"   File location: {screenshot_path}\n")
                except Exception as e:
                    self.logger.error(f"Failed to save QR code screenshot: {e}")

                self.logger.warning("Please run in non-headless mode first to scan QR code")
                self.logger.warning("Set WHATSAPP_HEADLESS=false in environment")
                return False

        except Exception as e:
            self.logger.error(f"Failed to check WhatsApp login status: {e}")
            return False

    def check_for_updates(self) -> List[Dict]:
        """Check WhatsApp for new urgent messages"""
        if not self.browser:
            if not self._init_browser():
                return []

        if not self._ensure_logged_in():
            return []

        try:
            urgent_messages = []

            # Get all chats (try multiple selectors as WhatsApp changes structure)
            all_chats = []
            chat_selectors = [
                '[data-testid="cell-frame-container"]',  # Old selector
                'div[role="listitem"]',  # Generic list item
                '#pane-side div[role="row"]',  # Rows in side pane
                'div._ak72._ak73',  # WhatsApp chat container class (may change)
            ]

            for selector in chat_selectors:
                all_chats = self.page.query_selector_all(selector)
                if len(all_chats) > 0:
                    self.logger.info(f"Found {len(all_chats)} chats using selector: {selector}")
                    break

            if len(all_chats) == 0:
                self.logger.warning("No chats found with any selector!")
                return []

            self.logger.info(f"Scanning {len(all_chats)} chats for urgent messages...")

            for idx, chat in enumerate(all_chats[:10]):  # Limit to first 10 to avoid long processing
                try:
                    # Get chat name (try multiple selectors)
                    chat_name = "Unknown"
                    name_selectors = [
                        '[data-testid="cell-frame-title"]',
                        'span[title]',  # Span with title attribute
                        'span[dir="auto"]',  # WhatsApp uses dir="auto" for names
                    ]
                    for name_sel in name_selectors:
                        chat_name_elem = chat.query_selector(name_sel)
                        if chat_name_elem:
                            chat_name = chat_name_elem.inner_text() or chat_name_elem.get_attribute('title') or "Unknown"
                            if chat_name != "Unknown":
                                break

                    # Check if chat has unread indicator (optional - just for logging)
                    has_unread = False
                    unread_selectors = [
                        '[data-testid="icon-unread-count"]',
                        '[aria-label*="unread"]',
                        '.tvf2evcx.m0h2a7mj'  # WhatsApp unread badge class
                    ]
                    for selector in unread_selectors:
                        if chat.query_selector(selector):
                            has_unread = True
                            break

                    self.logger.info(f"Chat {idx+1}: {chat_name} | Unread: {has_unread}")

                    # Click chat to open
                    chat.click()
                    time.sleep(2)  # Wait for messages to load

                    # Get last message text - try multiple selectors
                    messages = []
                    message_selectors = [
                        '[data-testid="msg-container"]',
                        'div.message-in, div.message-out',  # WhatsApp message divs
                        'div[role="row"]',  # Message rows
                        'div.copyable-text',  # WhatsApp copyable text container
                    ]

                    for msg_sel in message_selectors:
                        messages = self.page.query_selector_all(msg_sel)
                        if len(messages) > 0:
                            self.logger.info(f"  Found {len(messages)} messages using: {msg_sel}")
                            break

                    if not messages:
                        self.logger.info(f"  No messages found in {chat_name} with any selector")
                        continue

                    # Get last message and try multiple text selectors
                    last_message = messages[-1]
                    message_text = None
                    text_selectors = [
                        '[data-testid="conversation-text"]',
                        'span.selectable-text',
                        'span[dir="ltr"]',
                        'div._akbu',  # WhatsApp text class
                    ]

                    for text_sel in text_selectors:
                        message_text_elem = last_message.query_selector(text_sel)
                        if message_text_elem:
                            message_text = message_text_elem.inner_text()
                            if message_text:
                                break

                    if not message_text:
                        # Try getting all text from the message
                        message_text = last_message.inner_text()

                    if not message_text or len(message_text.strip()) == 0:
                        self.logger.info(f"  Could not read message text in {chat_name}")
                        continue
                    self.logger.info(f"  Last message: {message_text[:50]}...")

                    # Check for urgent keywords
                    matched_keywords = [kw for kw in self.keywords if kw in message_text.lower()]
                    if matched_keywords:
                        # Create unique message ID
                        message_id = f"{chat_name}_{message_text[:20]}_{datetime.now().strftime('%Y%m%d%H%M')}"

                        if message_id not in self.processed_messages:
                            self.logger.info(f"  ✅ URGENT MESSAGE FOUND! Keywords: {matched_keywords}")
                            urgent_messages.append({
                                'chat_name': chat_name,
                                'message_text': message_text,
                                'message_id': message_id,
                                'timestamp': datetime.now().isoformat()
                            })
                        else:
                            self.logger.info(f"  Message already processed")

                except Exception as e:
                    self.logger.error(f"Error processing chat {idx+1}: {e}")
                    continue

            self.logger.info(f"Found {len(urgent_messages)} new urgent WhatsApp messages")
            return urgent_messages

        except Exception as e:
            self.logger.error(f"Error checking WhatsApp messages: {e}")
            return []

    def create_action_file(self, message: Dict) -> Path:
        """Create action file for urgent WhatsApp message"""
        try:
            chat_name = message['chat_name']
            message_text = message['message_text']
            message_id = message['message_id']
            timestamp = message['timestamp']

            # Determine priority
            priority = 'high' if any(kw in message_text.lower() for kw in ['urgent', 'asap', 'emergency']) else 'medium'

            # Create action file content
            content = f"""---
type: whatsapp_message
from: {chat_name}
received: {timestamp}
processed: {datetime.now().isoformat()}
priority: {priority}
status: pending
whatsapp_id: {message_id}
---

## WhatsApp Message from {chat_name}

**Received:** {timestamp}
**Priority:** {priority.upper()}

**Message:**
{message_text}

## Suggested Actions

- [ ] Reply to sender on WhatsApp
- [ ] Create task if action required
- [ ] Forward to relevant team member
- [ ] Schedule follow-up if needed
- [ ] Archive after processing

## Notes

This message was flagged as urgent based on keyword detection.
Keywords matched: {', '.join([kw for kw in self.keywords if kw in message_text.lower()])}

**IMPORTANT:** Response required via WhatsApp Web (not automated)

---
*Created by WhatsApp Watcher - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

            # Create safe filename
            safe_chat_name = "".join(c for c in chat_name[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = f"WHATSAPP_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_chat_name}.md"
            filepath = self.needs_action / filename

            filepath.write_text(content, encoding='utf-8')

            # Mark as processed
            self._save_processed_message(message_id)

            self.logger.info(f"Created action file: {filename}")
            self.update_dashboard(f"📱 WhatsApp from {chat_name}: {message_text[:50]}...")

            return filepath

        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")
            return None

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

    def cleanup(self):
        """Clean up browser resources"""
        try:
            if self.browser:
                self.browser.close()
                self.logger.info("Browser closed")
        except Exception as e:
            self.logger.error(f"Error closing browser: {e}")


def main():
    """Main entry point for WhatsApp Watcher"""
    vault_path = os.getenv('VAULT_PATH', '/mnt/e/all-d-files/Ai_Employee_Vault')
    session_path = os.getenv('WHATSAPP_SESSION_PATH', None)

    watcher = WhatsAppWatcher(vault_path, session_path)

    print("WhatsApp Watcher started - monitoring for urgent messages")
    print(f"Vault: {vault_path}")
    print(f"Check interval: {watcher.check_interval} seconds")
    print(f"Session path: {watcher.session_path}")
    print("\nIMPORTANT: First run requires QR code scan")
    print("Run with WHATSAPP_HEADLESS=false for first-time setup\n")
    print("Press Ctrl+C to stop")

    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\nWhatsApp Watcher stopped by user")
        watcher.cleanup()
    except Exception as e:
        print(f"\nError: {e}")
        watcher.cleanup()
        raise


if __name__ == '__main__':
    main()
