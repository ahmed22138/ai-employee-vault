#!/usr/bin/env python3
"""
Simple script to get WhatsApp QR code screenshot
"""

import time
from playwright.sync_api import sync_playwright

print("🚀 Opening WhatsApp Web...")
print("⏳ Please wait 20 seconds for QR code to load...")
print("")

with sync_playwright() as p:
    # Launch browser
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Go to WhatsApp Web
    print("📱 Loading web.whatsapp.com...")
    page.goto('https://web.whatsapp.com', timeout=60000)

    # Wait for page to fully load
    print("⏳ Waiting 20 seconds for QR code to appear...")
    time.sleep(20)

    # Take screenshot
    screenshot_path = '/mnt/e/all-d-files/Ai_Employee_Vault/whatsapp_qr_code.png'
    page.screenshot(path=screenshot_path)

    print("")
    print("✅ Screenshot saved!")
    print(f"📂 Location: {screenshot_path}")
    print("")
    print("🖼️  Open this file in Windows:")
    print("   E:\\all-d-files\\Ai_Employee_Vault\\whatsapp_qr_code.png")
    print("")

    browser.close()

print("✅ Done! QR code screenshot ready!")
