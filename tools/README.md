# Tools Directory

Standalone automation scripts for the AI Employee system.

## Available Tools

### 1. LinkedIn Poster (`linkedin_poster.py`)

**Purpose:** Automated LinkedIn posting using browser automation

**Features:**
- ✅ Automated login to LinkedIn
- ✅ Post content programmatically
- ✅ Handles security challenges
- ✅ Dry-run mode for testing
- ✅ Uses credentials from .env

**Installation:**

```bash
# Install Playwright (if not already installed)
pip install playwright

# Install browser binaries
playwright install chromium

# Or install all browsers
playwright install
```

**Usage:**

```bash
# Test login only (dry run)
python3 tools/linkedin_poster.py --dry-run

# Post with default test content
python3 tools/linkedin_poster.py

# Post custom content
python3 tools/linkedin_poster.py "Your custom LinkedIn post content here"

# Post in visible browser mode (not headless)
BROWSER_HEADLESS=false python3 tools/linkedin_poster.py
```

**Configuration:**

Add to `.env`:
```bash
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password
BROWSER_HEADLESS=true  # Set to false to see browser
```

**Security Notes:**
- ⚠️ LinkedIn credentials are sensitive - keep .env secure
- ⚠️ LinkedIn may present security challenges (manual verification needed)
- ⚠️ Use responsibly - respect LinkedIn's terms of service
- ⚠️ Don't spam - post valuable content only

**Troubleshooting:**

1. **"ModuleNotFoundError: No module named 'playwright'"**
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. **Login fails with security challenge**
   - Script will pause for 60 seconds
   - Complete the challenge in the browser window
   - Script will continue automatically

3. **Can't see what's happening**
   ```bash
   BROWSER_HEADLESS=false python3 tools/linkedin_poster.py
   ```

4. **Post button not found**
   - LinkedIn UI changes frequently
   - Try updating the script selectors
   - Report issue for script update

## Future Tools

More automation tools will be added here:
- Email sender
- WhatsApp poster
- Social media scheduler
- Report generator

## Development

To add new tools:
1. Create Python script in this directory
2. Use .env for credentials
3. Add documentation to this README
4. Make executable: `chmod +x tools/your_tool.py`
