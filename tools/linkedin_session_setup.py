#!/usr/bin/env python3
"""
LinkedIn Session Setup - Complete verification once
This will save authenticated session for future use
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import json
import time

# Load environment
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

def setup_linkedin_session():
    """Setup LinkedIn session with manual verification"""

    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')

    if not email or not password:
        print("❌ LinkedIn credentials not found in .env")
        return False

    print("╔════════════════════════════════════════════════════════╗")
    print("║     LinkedIn Session Setup - One-Time Verification    ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    print("This will:")
    print("  1. Open visible browser")
    print("  2. Login to LinkedIn")
    print("  3. Let you complete any verification")
    print("  4. Save session for future automation")
    print()
    print(f"📧 Email: {email}")
    print()

    input("Press ENTER to continue...")
    print()

    session_file = Path(__file__).parent.parent / 'linkedin_session.json'

    with sync_playwright() as p:
        print("🌐 Launching browser...")
        browser = p.chromium.launch(headless=False)  # Visible browser
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720}
        )
        page = context.new_page()

        try:
            # Navigate to LinkedIn
            print("📍 Navigating to LinkedIn...")
            page.goto('https://www.linkedin.com/login')
            time.sleep(2)

            # Login
            print("🔐 Entering credentials...")
            page.fill('#username', email)
            page.fill('#password', password)
            page.click('button[type="submit"]')

            print()
            print("⏳ Waiting for login...")
            print()
            print("📱 If security verification appears:")
            print("   → Complete it in the browser window")
            print("   → This script will wait for you")
            print("   → Take your time!")
            print()

            # Wait for feed or checkpoint
            try:
                page.wait_for_url('**/feed/**', timeout=120000)  # 2 minutes
                print("✅ Login successful!")
            except:
                # Might be on checkpoint/challenge page
                current_url = page.url
                if 'checkpoint' in current_url or 'challenge' in current_url:
                    print("⚠️ Security challenge detected!")
                    print("📱 Please complete verification in browser...")
                    print("⏳ Waiting up to 5 minutes...")

                    # Wait for user to complete challenge
                    page.wait_for_url('**/feed/**', timeout=300000)  # 5 minutes
                    print("✅ Verification complete!")
                else:
                    print(f"⚠️ Unexpected page: {current_url}")
                    print("Trying to continue...")

            # Save session
            print()
            print("💾 Saving session...")
            cookies = context.cookies()
            storage = context.storage_state()

            session_data = {
                'cookies': cookies,
                'storage': storage
            }

            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)

            print(f"✅ Session saved to: {session_file}")
            print()
            print("🎉 Setup complete!")
            print()
            print("Now you can use automation without verification:")
            print("  python3 tools/linkedin_poster.py")
            print()

            # Keep browser open to see success
            time.sleep(5)

            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        finally:
            browser.close()

if __name__ == '__main__':
    success = setup_linkedin_session()
    sys.exit(0 if success else 1)
