# Gmail Promo Agent

**An AI-powered local tool that turns your cluttered promotional inbox into an organized, searchable dashboard — all while keeping your data on YOUR machine.**

Built in a single day to demonstrate how AI can help create practical tools that respect your privacy.

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Privacy First](https://img.shields.io/badge/privacy-local%20first-green.svg)

---

## What This Does

Your inbox has 50+ promotional emails with discount codes scattered everywhere. Finding a specific code takes 5-10 minutes of clicking through emails.

**This tool:**
- Scans your Gmail promotional folder automatically
- Extracts promo codes, discounts, and expiration dates
- Generates a searchable, sortable dashboard
- Makes finding codes take 2 seconds instead of 10 minutes
- **Runs 100% locally** - your data never touches our servers

### Before:
Spend 10 minutes reading emails to find "Was there a code for Target?"

### After:
Open dashboard, search "Target", copy code. Done in 5 seconds.

---

## Why Local-First?

**I deliberately chose NOT to build this as a web app.** Here's why:

### Trust & Privacy Matter
Would you give a random web app access to your Gmail? Probably not. Neither would I.

This tool:
- Runs on YOUR computer
- Uses YOUR Google credentials
- Stores data in YOUR local database
- Never sends data to external servers
- You can inspect every line of code

### Ethical AI Development
With AI tools becoming more powerful, **we need to be thoughtful about where we grant access.** A hosted web service with Gmail access is:
- A security risk (credentials exposed to server)
- A privacy risk (your emails processed remotely)  
- A trust problem (how do you know data isn't stored?)

**Local-first is the responsible choice.**

[Read the full blog post on why local-first matters](BLOG_POST.md)

---

## Features

### Smart Extraction
- Conservative detection - Only extracts real promo codes (no false positives)
- Multiple discount formats - Handles %, $, BOGO, free shipping
- Expiration tracking - Knows when codes expire
- Merchant detection - Identifies which company sent the offer

### Interactive Dashboard  
- Real-time search - Find any code in milliseconds
- Category filtering - Flights, Food, Retail, Entertainment, etc.
- Urgency indicators - See which codes expire soon
- One-click copying - Copy any code to clipboard instantly
- Mobile responsive - Works on phone, tablet, or desktop

### Privacy & Security
- Read-only Gmail access - Cannot send, delete, or modify emails
- Local OAuth - Authentication happens on your machine
- Encrypted storage - Tokens stored securely in local database
- No external calls - Dashboard works completely offline

---

## Quick Start

**Time to working app: ~5 minutes**

### Prerequisites
- Python 3.8+ installed ([Download here](https://www.python.org/downloads/))
- Gmail account
- 5 minutes

### Setup in 3 Steps

```bash
# 1. Clone and install
git clone https://github.com/udirno/gmail-promo-agent.git
cd gmail-promo-agent
pip install -r requirements.txt

# 2. Set up Google credentials (one-time, ~2 minutes)
# Follow the guide: QUICKSTART.md

# 3. Run the app
python api_server.py
# Then open: http://localhost:8000
```

**Full setup guide:** [QUICKSTART.md](QUICKSTART.md) - Start here if you're new!

---

## Screenshots

### Promotional Email Example
![Promotional Email](screenshots/promo_email.png)
*Typical promotional email with embedded discount code*

### OAuth Authorization
![OAuth Screen](screenshots/oauth_consent.png)
*One-time Gmail authorization (your data stays local)*

### Extracted Codes
![Extracted Promo Codes](screenshots/found_promos.png)
*Clean, organized codes with merchant names and expiration dates*

---

## How It Works

### Architecture
```
Your Computer (Everything runs here)
│
├─ Python Backend (FastAPI)
│  ├─ Gmail API Integration (your credentials)
│  ├─ AI-Enhanced Parser (extracts codes)
│  └─ SQLite Database (local storage)
│
└─ HTML Dashboard
   ├─ Search & Filter UI
   └─ Works offline after generation
```

### Data Flow
1. **You authorize** - One-time OAuth with Google (you control access)
2. **App scans Gmail** - Reads promotional emails using Gmail API
3. **AI extracts codes** - Smart parsing finds real promo codes
4. **Dashboard generates** - Beautiful, searchable HTML file
5. **You use codes** - Search, filter, copy codes instantly

**Your emails never leave your computer.**

---

## Tech Stack

**Backend:**
- Python 3.8+ (main logic)
- FastAPI (API server)
- SQLAlchemy (database ORM)
- Gmail API (email access)

**Frontend:**
- Vanilla JavaScript (no framework needed)
- HTML/CSS (responsive design)
- Local storage (works offline)

**Why these choices?**
- No external dependencies once set up
- Easy to audit - readable Python code
- Fast setup - standard libraries
- Privacy preserved - no cloud services

---

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes (START HERE!)
- **[BLOG_POST.md](BLOG_POST.md)** - Why I built this local-first
- **[SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** - Detailed setup instructions
- **[USAGE_GUIDE.md](docs/USAGE_GUIDE.md)** - How to use the dashboard

---

## FAQ

### Do I need to set up Google Cloud credentials?
**Yes, but it takes ~2 minutes** following [QUICKSTART.md](QUICKSTART.md).

**Why?** Google requires this for any app accessing Gmail (even local ones). Think of it like creating an API key.

### Is my Gmail data safe?
**Completely safe.** The app:
- Runs only on your computer
- Uses read-only access (cannot send/delete emails)
- Stores data in local SQLite database
- Uses standard OAuth (same as mobile Gmail apps)

You can revoke access anytime at https://myaccount.google.com/permissions

### Can I use this on multiple computers?
**Yes!** Just clone the repo and set up credentials on each machine. Data stays local to each computer.

### Does this work with Outlook/Yahoo?
**Not yet.** Currently Gmail only. Email provider integration could be added in the future.

### Can I share my promo codes with family?
**Yes!** The dashboard is a self-contained HTML file. Just email it or upload to shared drive. Recipients don't need the app installed to view codes.

---

## Why I Built This

### The Problem
I was drowning in promotional emails. Whenever I needed a code, I'd spend 10 minutes clicking through my inbox. Frustrating and time-wasting.

### The Solution
I wanted a tool that:
- Automatically extracts all my promo codes
- Makes them searchable and organized  
- **Doesn't require trusting a third party with Gmail access**

### The Result
Built in a single day using AI assistance (Claude) to:
- Write the core extraction logic
- Implement Gmail API integration
- Create the dashboard interface
- Handle edge cases and testing

**Total development time: ~8 hours** (including learning Gmail API, OAuth setup, and documentation)

### The Takeaway
This demonstrates how AI can help you build practical tools quickly — tools you actually want to use, that respect your privacy, and that you can understand and modify.

---

## Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python database.py

# Run API server (with auto-reload)
python api_server.py

# Run tests
python check_merchants.py
```

### Project Structure
```
gmail-promo-agent/
├── api_server.py              # FastAPI backend
├── gmail_service.py           # Gmail API integration
├── database.py                # SQLite models
├── promo_parser.py            # Code extraction logic
├── dashboard_generator.py     # HTML dashboard builder
├── categories.json            # Category definitions
├── config.yaml                # Configuration
└── docs/                      # Documentation
```

---

## Contributing

This is a personal project demonstrating local-first AI tools. Not actively seeking contributions, but feedback is welcome!

**Ideas for future versions:**
- Support for other email providers (Outlook, Yahoo)
- Browser extension for auto-applying codes
- Calendar integration for expiration reminders
- Better ML-based merchant detection
- Mobile app version

---

## License

MIT License - Do whatever you want with this code.

See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- Built with assistance from Claude (Anthropic)
- Gmail API documentation by Google
- Inspired by the need for privacy-respecting tools

---

## Support

- **Issues:** [GitHub Issues](https://github.com/udirno/gmail-promo-agent/issues)
- **Questions:** Check [QUICKSTART.md](QUICKSTART.md) or open an issue
- **Security concerns:** Please open a private security advisory

---

## Try It Now

Ready to organize your promo codes?

**[Start with QUICKSTART.md](QUICKSTART.md)** - 5 minute setup!

Or **[read why local-first matters](BLOG_POST.md)** first.

---

**Built with AI in a single day | Privacy-first | Local-always**