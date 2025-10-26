# Gmail Promo Agent

**A local-first AI tool that transforms your cluttered promotional inbox into an organized, searchable dashboard—while keeping your data on your machine.**

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Privacy First](https://img.shields.io/badge/privacy-local%20first-green.svg)

---

## Overview

Your Gmail inbox has 50+ promotional emails scattered everywhere. Finding a specific promo code takes 5-10 minutes of frustrated clicking. You know there was a Target discount somewhere, but where?

**Gmail Promo Agent solves this.**

It automatically scans your Gmail promotional folder, extracts promo codes and discount information, identifies which merchants sent them, tracks expiration dates, and generates a clean, searchable dashboard. Finding any code takes 2 seconds instead of 10 minutes.

The entire tool runs locally on your computer. Your email data never touches external servers. No third-party access, no cloud processing, no subscriptions—just a privacy-respecting tool that works.

**Why local-first?** Because you shouldn't have to trust a random web app with full access to your Gmail. This tool runs on your machine, uses your credentials, stores data in your local database, and you can inspect every line of code.

---

## Quickstart

**For Mac users:**

```bash
# Clone and install
git clone https://github.com/udirno/gmail-promo-agent.git
cd gmail-promo-agent
pip3 install -r requirements.txt

# Set up Google credentials (one-time)
# Follow the guide in docs/setup/quickstart.md

# Run the app
python3 api_server.py
# Then open: http://localhost:8000
```

**Need detailed setup instructions?** See [quickstart.md](docs/setup/quickstart.md) for a complete step-by-step guide with screenshots.

**Having issues?** Check the Troubleshooting section below or open a GitHub issue.

---

## Design

### Why Local-First?

I deliberately chose not to build this as a web app. Here's why:

**Trust & Privacy:** Would you give a random web service access to your Gmail? I wouldn't either. This tool runs entirely on your computer, uses your own Google credentials, stores data in your local SQLite database, never sends data to external servers, and lets you inspect all the code.

**Ethical AI Development:** As AI tools become more powerful, we need to be thoughtful about where we grant them access. A cloud service with Gmail access creates security risks (credentials exposed to servers), privacy risks (emails processed remotely), and trust problems (how do you know data isn't stored?). Local-first is the responsible choice.

### Key Features

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
- Mobile responsive
- Works completely offline

**Privacy & Security:**
- Read-only Gmail access (cannot send, delete, or modify emails)
- Local OAuth authentication
- Encrypted token storage in local database
- No external API calls after initial setup
- Fully auditable code

---

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

---

## FAQ

### Do I need Google Cloud credentials?

Yes, but setup takes about 2 minutes. Google requires any app accessing Gmail (even local ones) to have OAuth credentials—think of it like creating an API key. [quickstart.md](docs/setup/quickstart.md) walks you through it step-by-step.

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

---

## Troubleshooting

**Common issues and quick fixes:**

**"credentials.json not found"**  
Make sure you've downloaded your OAuth credentials from Google Cloud Console and placed them in the project root directory. See [quickstart.md](docs/setup/quickstart.md) for detailed instructions.

**"Port 8000 already in use"**  
Another app is using that port. Either stop that app or edit `api_server.py` to use a different port (change `port=8000` to `port=8001`).

**"Permission denied during OAuth"**  
Add yourself as a test user in Google Cloud Console: APIs & Services → OAuth consent screen → Test users → Add your Gmail address.

**"No promo codes found"**  
Check your Gmail promotions folder has emails from the last 7 days. The tool uses conservative extraction (quality over quantity). Try adjusting the time range in `config.yaml`: change `newer_than:7d` to `newer_than:30d`.

**More help:** Check [quickstart.md](docs/setup/quickstart.md) for detailed troubleshooting or open a GitHub issue.

---

## Documentation

- **[quickstart.md](docs/setup/quickstart.md)** - Get running in 5 minutes (START HERE!)
- **[How We Built This](docs/blog/how-we-built-gmail-promo-agent-with-claude.md)** - Building a local-first AI tool

---

## Contributing

This is a personal project demonstrating local-first AI tools. Feedback is welcome via GitHub issues.

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- Built with assistance from Claude (Anthropic)
- Gmail API documentation by Google
- Inspired by the need for privacy-respecting tools

---

## Try It Now

Ready to organize your promo codes?

👉 **[Start with quickstart.md](docs/setup/quickstart.md)**

Or **[read why local-first matters](docs/blog/how-we-built-gmail-promo-agent-with-claude.md)** first.

---

**Built with AI in a single day | Privacy-first | Local-always**
