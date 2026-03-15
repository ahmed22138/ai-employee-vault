#!/usr/bin/env python3
"""
WhatsApp QR Code - With proper browser settings
"""

import time
from playwright.sync_api import sync_playwright

print("🚀 Starting WhatsApp Web with updated browser...")
print("")

with sync_playwright() as p:
    # Launch with proper user agent (latest Chrome)
    browser = p.chromium.launch(
        headless=True,
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-blink-features=AutomationControlled'
        ]
    )

    # Create context with modern Chrome user agent
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1280, 'height': 720}
    )

    page = context.new_page()

    print("📱 Loading WhatsApp Web...")
    page.goto('https://web.whatsapp.com', wait_until='networkidle')

    print("⏳ Waiting 15 seconds for QR code...")
    time.sleep(15)

    # Take screenshot
    screenshot_path = '/mnt/e/all-d-files/Ai_Employee_Vault/whatsapp_qr_code.png'
    page.screenshot(path=screenshot_path, full_page=False)

    print("")
    print("✅ Screenshot saved!")
    print(f"📂 Location: {screenshot_path}")
    print("")
    print("🖼️  Windows path:")
    print("   E:\\all-d-files\\Ai_Employee_Vault\\whatsapp_qr_code.png")
    print("")

    browser.close()

print("✅ Done! QR code should be visible now!")
