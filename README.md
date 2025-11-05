# Gmail Promo Agent

**A local-first AI tool that transforms your cluttered promotional inbox into an organized, searchable dashboard—while keeping your data on your machine.**

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Privacy First](https://img.shields.io/badge/privacy-local%20first-green.svg)

## Overview

Your Gmail inbox has 50+ promotional emails scattered everywhere. Finding a specific promo code takes 5-10 minutes of frustrated clicking. You know there was a Target discount somewhere, but where?

**Gmail Promo Agent solves this.**

It automatically scans your Gmail promotional folder, extracts promo codes and discount information, identifies which merchants sent them, tracks expiration dates, and generates a clean, searchable dashboard. Finding any code takes 2 seconds instead of 10 minutes.

The entire tool runs locally on your computer. Your email data never touches external servers. No third-party access, no cloud processing, no subscriptions—just a privacy-respecting tool that works.

**Why local-first?** Because you shouldn't have to trust a random web app with full access to your Gmail. This tool runs on your machine, uses your credentials, stores data in your local database, and you can inspect every line of code.

## Quickstart - Get Running in 5 Minutes

**Goal:** From zero to working promo code dashboard in approximately 5 minutes.

**Time breakdown:** Install Python (2 min, one-time) → Download project (30 sec) → Set up Google credentials (2 min, one-time) → Run the app (30 sec)

**Prerequisites:**
- A Gmail account (the one you want to scan for promo codes)
- Administrator access to your computer (to install Python)
- 5 minutes of uninterrupted time

### Step 1: Install Python (2 minutes, ONE-TIME)

**Check if you already have Python:**

Open your terminal:
- **Mac:** Press `Cmd + Space`, type "Terminal", press Enter
- **Windows:** Press `Win + R`, type "cmd", press Enter
- **Linux:** Use your preferred terminal

Type this command:
```bash
python3 --version
```

**If you see** `Python 3.8.10` or higher → **Skip to Step 2**

**If you get an error** → Install Python:

**Mac:**
```bash
# Install Homebrew (if you don't have it)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

**Windows:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download and run the installer
3. **CHECK** "Add Python to PATH"
4. Click "Install Now"

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip
```

**Verify:** Close and reopen terminal, then run `python3 --version`

### Step 2: Download the Project (30 seconds)

**Option A: Using Git (Recommended)**
```bash
cd ~/Desktop
git clone https://github.com/udirno/gmail-promo-agent.git
cd gmail-promo-agent
pip3 install -r requirements.txt
```

**Option B: Download ZIP**
1. Go to [github.com/udirno/gmail-promo-agent](https://github.com/udirno/gmail-promo-agent)
2. Click green "Code" button → "Download ZIP"
3. Extract to your Desktop
4. Open terminal and run:
   ```bash
   cd ~/Desktop/gmail-promo-agent-main
   pip3 install -r requirements.txt
   ```

Wait 30-60 seconds for dependencies to install.

### Step 3: Set Up Google Credentials (2 minutes, ONE-TIME)

**Why?** Google requires ANY app accessing Gmail to have OAuth credentials—even local apps. Think of it as creating an API key.

**Your data stays local.** These credentials just let YOUR app talk to YOUR Gmail.

#### 3.1: Create a Google Cloud Project

1. Open [console.cloud.google.com](https://console.cloud.google.com)
2. Sign in with your Gmail account
3. Click project dropdown → "NEW PROJECT"
4. Name: "Promo Code Manager" → Click "CREATE"
5. Wait 10 seconds, then **make sure your new project is selected**

#### 3.2: Enable Gmail API

1. Left sidebar → "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click "Gmail API" → Click "ENABLE"
4. Wait 5 seconds

#### 3.3: Configure OAuth Consent Screen

1. Left sidebar → "APIs & Services" → "OAuth consent screen"
2. Select "External" → Click "CREATE"
3. Fill in:
   - **App name:** Promo Code Manager
   - **User support email:** (your email)
   - **Developer contact:** (your email)
4. Click "SAVE AND CONTINUE" (3 times)
5. Left sidebar → "Audience"
6. Click "+ ADD USERS"
7. Enter YOUR Gmail address → Click "ADD"

#### 3.4: Create OAuth Credentials

1. Left sidebar → "APIs & Services" → "Credentials"
2. Click "+ CREATE CREDENTIALS" → "OAuth client ID"
3. **Application type:** Desktop app
4. **Name:** Promo Agent Local Client
5. Click "CREATE"
6. Click "DOWNLOAD JSON"
7. **Rename the downloaded file to:** `credentials.json`
8. **Move it to your project folder** (same location as `api_server.py`)

**Verify:**
```bash
cd ~/Desktop/gmail-promo-agent
ls credentials.json  # Should show the file
```

### Step 4: Run the App (30 seconds)

Start the server:
```bash
cd ~/Desktop/gmail-promo-agent
python3 -u api_server.py
```

You should see:
```
Gmail Promo Agent API Starting...
Server running at: http://localhost:8000
```

**Leave this terminal open** (Server needs to keep running)

#### 4.1: Open the Test Page

**Open a NEW terminal window** (keep server running in first one).

```bash
cd ~/Desktop/gmail-promo-agent

# Open test page in browser:
open test_frontend.html        # Mac
start test_frontend.html       # Windows
xdg-open test_frontend.html    # Linux
```

#### 4.2: Connect Your Gmail

1. Click "Create Test User" → Success message appears
2. Click "Connect Gmail" → Google sign-in window opens
3. Sign in with your Gmail account
4. You'll see: "Google hasn't verified this app"
   - Click "Advanced" → "Go to Promo Code Manager (unsafe)"
   - *(It says "unsafe" because it's your local app—this is normal)*
5. Click "Allow"
6. Window says "Gmail connected successfully"
7. Close that window and return to test page

#### 4.3: Scan for Promo Codes

1. Click "Scan for Promos"
2. Wait 10-30 seconds...
3. In your terminal, you'll see:
   ```
   Processing 50 emails...
   Email 1/50: Found 1 promo(s) - Chase Center
     Code: SFHOOPS
   ...
   Total promos: 12
   ```
4. Click "Get Promos" to see your codes

### Step 5: View Your Dashboard

The scan created an interactive HTML dashboard:

```bash
open promo_dashboard.html      # Mac
start promo_dashboard.html     # Windows
xdg-open promo_dashboard.html  # Linux
```

**You're done**

**What you can do now:**
- **Search instantly:** Type any merchant name
- **Filter by category:** Click category pills
- **Copy codes:** One-click copy to clipboard
- **Re-scan anytime:** Just click "Scan for Promos" again

### Troubleshooting

**"credentials.json not found"**
- Make sure you downloaded the JSON from Google Cloud
- Renamed it to exactly `credentials.json`
- Placed it in project root (same folder as `api_server.py`)

**"Port 8000 already in use"**
- Another app is using that port
- Edit `api_server.py`: change `port=8000` to `port=8001`

**"Permission denied during OAuth"**
- Go to console.cloud.google.com
- APIs & Services → Audience
- Add yourself as a test user

**"No promo codes found"**
- Check your Gmail promotions folder for emails in last 7 days
- The tool uses conservative extraction (quality over quantity)
- Adjust time in `config.yaml`: change `newer_than:7d` to `newer_than:30d`

## Why Local-First?

I deliberately chose not to build this as a web app. Here's why:

**Trust & Privacy:** Would you give a random web service access to your Gmail? I wouldn't either. This tool runs entirely on your computer, uses your own Google credentials, stores data in your local SQLite database, never sends data to external servers, and lets you inspect all the code.

**Ethical AI Development:** As AI tools become more powerful, we need to be thoughtful about where we grant them access. A cloud service with Gmail access creates security risks (credentials exposed to servers), privacy risks (emails processed remotely), and trust problems (how do you know data isn't stored?). Local-first is the responsible choice.

## Key Features

**Smart Extraction:**
- Conservative detection—only extracts real promo codes with clear context
- Handles multiple discount formats (%, $, BOGO, free shipping)
- Tracks expiration dates and urgency levels
- Identifies merchant names from sender domains

**Interactive Dashboard:**
- Real-time search across all codes
- Category filtering (Flights, Food, Retail, Entertainment, etc.)
- Urgency indicators (color-coded expiration warnings)
- One-click code copying
- Sortable columns

**Privacy & Security:**
- Read-only Gmail access (cannot send, delete, or modify emails)
- Local OAuth authentication
- Encrypted token storage in local database
- No external API calls after initial setup
- Fully auditable code

## Architecture

The Gmail Promo Agent uses a simple, privacy-first architecture.

**Backend (Python/FastAPI):** An API server handles Gmail authentication and email processing. A SQLite database stores users, OAuth tokens, and extracted promo codes. Conservative extraction logic prevents false positives, and intelligent merchant detection automatically categorizes offers.

**Frontend (HTML/JavaScript):** A self-contained HTML dashboard with no external dependencies provides real-time filtering and search. It works offline once generated and includes no tracking or analytics.

**Data Flow:**
1. You authorize Gmail access (one-time OAuth)
2. App scans your promotional emails locally
3. AI-enhanced parser extracts real promo codes
4. Dashboard generates as a shareable HTML file
5. Your emails never leave your computer

All processing happens on your machine. Your credentials stay in your local database. Your data remains under your control.

## Considerations

**Extraction Accuracy:**
The promo code extraction uses regex patterns that work well for common promotional email formats. However, please be aware:

- **Current coverage:** The regex patterns are tuned for typical promotional emails and work reliably for most major retailers and service providers
- **Iterative improvement:** The patterns will need a few rounds of tuning before they cover a wider variety of email formats
- **No security risk:** Extraction limitations do not pose any security issues. However, you may experience:
  - **False negatives:** Some legitimate promotional emails may be missed 
  - **False positives:** Some emails may be misclassified as promotions even if they are not
  - **Extraction errors:** The parser may occasionally fail to extract the correct code from certain promotions

**Reporting Issues:**
If you encounter any defects or limitations with the extraction logic, please file a GitHub issue describing the problem. This helps improve the tool for everyone, though fixes cannot be guaranteed.

## FAQ

### Do I need Google Cloud credentials?

Yes, but setup takes about 2 minutes. Google requires any app accessing Gmail (even local ones) to have OAuth credentials—think of it like creating an API key. The Quickstart section above walks you through it step-by-step.

### Is my Gmail data safe?

Completely safe. The app runs only on your computer, uses read-only Gmail access (cannot send/delete emails), stores everything in a local SQLite database, uses standard OAuth (same as official Gmail apps), and never transmits data to external servers. You can revoke access anytime at https://myaccount.google.com/permissions

### Can I use this on multiple computers?

Yes. Just clone the repo and set up credentials on each machine. Your data stays local to each computer—no syncing between them.

### Can I share my promo codes with family?

Absolutely. The dashboard is a self-contained HTML file. Just email it or upload to a shared drive. Recipients don't need the app installed to view your codes.

### Does this work with Outlook or Yahoo?

Not yet—currently Gmail only. Support for other providers could be added in the future.

### How long does setup take?

First time: ~5 minutes (includes Google Cloud setup). Subsequent uses: ~30 seconds (just run the app). Google Cloud setup is one-time only.

### Do I need to scan every time I want to see codes?

No. After scanning once, the dashboard HTML file persists. You can open it anytime. Scan again only when you want to fetch new promos.

### Does this cost money?

No. Everything is free—the code is open source, Gmail API is free (up to 250 requests/second), and there are no subscriptions or hidden costs.

## Quick Command Reference

```bash
# Start the server
python3 -u api_server.py

# Run demo (no Gmail needed)
python3 demo_simulation.py

# Check extracted codes
python3 check_merchants.py

# View dashboard
open promo_dashboard.html
```

## Documentation

- **[How We Built This](docs/blog/how-we-built-gmail-promo-agent-with-claude.md)** - Building a local-first AI tool with Claude

## Contributing

This is a personal project demonstrating local-first AI tools. Feedback is welcome via GitHub issues.

## License

MIT License - See [LICENSE](LICENSE) for details.

## Acknowledgments

- Built with assistance from Claude (Anthropic)
- Gmail API documentation by Google
