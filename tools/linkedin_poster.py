#!/usr/bin/env python3
"""
LinkedIn Automated Poster - Gold Tier
Uses Playwright browser automation to post to LinkedIn
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

class LinkedInPoster:
    """Automated LinkedIn poster using browser automation"""

    def __init__(self):
        self.email = os.getenv('LINKEDIN_EMAIL')
        self.password = os.getenv('LINKEDIN_PASSWORD')
        self.headless = os.getenv('BROWSER_HEADLESS', 'false').lower() == 'true'

        if not self.email or not self.password:
            raise ValueError("LinkedIn credentials not found in .env file")

        print(f"✅ Loaded credentials for: {self.email}")

    def post_to_linkedin(self, content: str, dry_run: bool = False) -> bool:
        """
        Post content to LinkedIn

        Args:
            content: The post content to publish
            dry_run: If True, only test login without posting

        Returns:
            True if successful, False otherwise
        """
        if dry_run:
            print("🧪 DRY RUN MODE - Will test login only, no posting")

        print("🚀 Starting LinkedIn browser automation...")

        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()

            try:
                # Step 1: Navigate to LinkedIn login
                print("📍 Navigating to LinkedIn...")
                page.goto('https://www.linkedin.com/login', wait_until='networkidle')
                time.sleep(2)

                # Step 2: Login
                print("🔐 Logging in...")
                page.fill('#username', self.email)
                page.fill('#password', self.password)
                page.click('button[type="submit"]')

                # Wait for login to complete
                print("⏳ Waiting for login...")
                try:
                    page.wait_for_url('https://www.linkedin.com/feed/', timeout=15000)
                    print("✅ Login successful!")
                except PlaywrightTimeout:
                    # Check if we're on security challenge page
                    if 'checkpoint' in page.url or 'challenge' in page.url:
                        print("⚠️ LinkedIn security challenge detected!")
                        print("📱 Please complete the security verification in the browser...")
                        print("⏳ Waiting 60 seconds for manual verification...")
                        time.sleep(60)

                        # Check if we made it to feed
                        if 'feed' not in page.url:
                            print("❌ Login failed - security challenge not completed")
                            return False
                    else:
                        print("❌ Login failed - timeout waiting for feed")
                        return False

                if dry_run:
                    print("✅ DRY RUN: Login successful - skipping post")
                    time.sleep(3)
                    return True

                # Step 3: Click "Start a post" button
                print("✍️ Starting new post...")
                try:
                    # Try multiple selectors for "Start a post" button
                    selectors = [
                        'button[aria-label*="Start a post"]',
                        'button.share-box-feed-entry__trigger',
                        '.share-box-feed-entry__trigger'
                    ]

                    clicked = False
                    for selector in selectors:
                        try:
                            page.click(selector, timeout=5000)
                            clicked = True
                            break
                        except:
                            continue

                    if not clicked:
                        print("❌ Could not find 'Start a post' button")
                        return False

                    time.sleep(2)

                except Exception as e:
                    print(f"❌ Error clicking 'Start a post': {e}")
                    return False

                # Step 4: Fill in post content
                print("📝 Writing post content...")
                try:
                    # Wait for editor to appear
                    page.wait_for_selector('.ql-editor', timeout=10000)

                    # Type content
                    editor = page.locator('.ql-editor').first
                    editor.click()
                    editor.fill(content)
                    time.sleep(2)

                    print("✅ Content written")

                except Exception as e:
                    print(f"❌ Error writing content: {e}")
                    return False

                # Step 5: Post
                print("📤 Publishing post...")
                try:
                    # Find and click Post button
                    post_button_selectors = [
                        'button[aria-label*="Post"]',
                        'button.share-actions__primary-action',
                        'button:has-text("Post")'
                    ]

                    posted = False
                    for selector in post_button_selectors:
                        try:
                            page.click(selector, timeout=5000)
                            posted = True
                            break
                        except:
                            continue

                    if not posted:
                        print("❌ Could not find 'Post' button")
                        return False

                    # Wait for post to complete
                    time.sleep(5)
                    print("✅ Post published successfully!")
                    return True

                except Exception as e:
                    print(f"❌ Error publishing post: {e}")
                    return False

            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                return False

            finally:
                # Keep browser open for a moment to see result
                time.sleep(3)
                browser.close()

def main():
    """Main function"""
    print("=" * 60)
    print("LinkedIn Automated Poster - Gold Tier")
    print("=" * 60)
    print()

    # Check for dry run mode
    dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true' or '--dry-run' in sys.argv

    # Get content from command line or use test content
    if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        content = sys.argv[1]
    else:
        content = """🎉 Exciting milestone achieved!

Just completed the implementation of my Personal AI Employee system - a fully autonomous agent that handles emails, social media, and business tasks 24/7.

Key features:
→ Intelligent email triage and response drafting
→ Automated LinkedIn posting (like this one!)
→ WhatsApp message monitoring
→ Human-in-the-loop approvals for critical decisions

Built with Claude Code, Playwright automation, and lots of coffee ☕

What automation are you working on?

#AI #Automation #Productivity #TechInnovation"""

    print(f"📝 Content to post ({len(content)} characters):")
    print("-" * 60)
    print(content)
    print("-" * 60)
    print()

    try:
        poster = LinkedInPoster()
        success = poster.post_to_linkedin(content, dry_run=dry_run)

        if success:
            print()
            print("=" * 60)
            print("✅ SUCCESS!")
            print("=" * 60)
            return 0
        else:
            print()
            print("=" * 60)
            print("❌ FAILED")
            print("=" * 60)
            return 1

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
