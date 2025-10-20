# Gmail Promo Agent 🎯

An intelligent agent that automatically extracts promotional codes from your Gmail inbox and generates a clean, interactive dashboard for easy access and sharing.

## Features

✨ **Smart Extraction**
- Conservative promo code detection (no false positives)
- Intelligent merchant name extraction
- Automatic discount and expiration date parsing
- HTML email support

📊 **Interactive Dashboard**
- Clean, professional interface
- Real-time search and filtering
- Sort by merchant, code, expiration, or urgency
- One-click code copying
- Mobile responsive design
- Category-based organization

🎯 **Intelligent Features**
- Removes expired codes automatically
- Urgency indicators (expiring soon highlighted)
- Merchant name extraction from sender
- Deduplication of repeated codes
- "NO CODE NEEDED" tracking for automatic discounts

## Quick Start

### Prerequisites

- Python 3.8+
- Gmail account
- Google Cloud project with Gmail API enabled

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/gmail-promo-agent.git
cd gmail-promo-agent

# Install dependencies
pip install -r requirements.txt
```

### Setup

1. **Enable Gmail API**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download as `credentials.json`

2. **Configure**
   ```bash
   # Place credentials.json in project root
   # Edit config.yaml if needed (optional)
   ```

3. **Run**
   ```bash
   # First run - will open browser for authentication
   python gmail_agent.py
   
   # Open dashboard
   open promo_dashboard.html
   ```

## Usage

### Basic Run

```bash
python gmail_agent.py
```

This will:
1. Connect to Gmail
2. Fetch promotional emails (last 7 days by default)
3. Extract promo codes and merchant info
4. Generate interactive dashboard
5. Save JSON backup

### Demo Mode

Test without Gmail credentials:

```bash
python demo_simulation.py
open demo_promo_dashboard.html
```

### Check Extraction Quality

```bash
python check_merchants.py
```

Shows:
- First 20 extracted promos
- Merchant name extraction details
- Top merchants by frequency

## Configuration

Edit `config.yaml`:

```yaml
gmail:
  query: "category:promotions newer_than:7d"  # Adjust timeframe
  credentials_path: "./credentials.json"

report:
  dashboard_path: "./promo_dashboard.html"
  categories_path: "./categories.json"
  
  # Feature flags
  remove_expired: true
  sort_by_urgency: true
```

### Customize Categories

Edit `categories.json`:

```json
{
  "Flights": ["flight", "airline", "travel"],
  "Food": ["restaurant", "delivery", "meal"],
  "Your Category": ["keyword1", "keyword2"]
}
```

## Dashboard Features

### Main View
- **Search**: Type to filter by merchant, code, or discount
- **Category Filters**: Quick filter buttons (All, Flights, Food, etc.)
- **Sort**: Click any column header to sort
- **Copy**: One-click copy button for each code

### Columns
1. **Merchant** - Company offering the deal
2. **Promo Code** - The actual code + copy button
3. **Discount** - Amount you save
4. **Expires** - Expiration date
5. **Category** - Type of offer
6. **Urgency** - Color-coded time remaining

### Urgency Indicators
- 🔴 **Red** - Expires today/tomorrow
- 🟠 **Orange** - Expires in 2-3 days
- 🟡 **Yellow** - Expires in 4-7 days
- 🟢 **Green** - Expires in 7+ days

## Project Structure

```
gmail-promo-agent/
├── gmail_agent.py              # Main agent
├── promo_parser.py             # Code extraction logic
├── dashboard_generator.py      # HTML dashboard generator
├── demo_simulation.py          # Demo with sample data
├── check_merchants.py          # Diagnostic tool
├── config.yaml                 # Configuration
├── categories.json             # Category definitions
├── requirements.txt            # Python dependencies
├── credentials.json            # OAuth credentials (you create)
├── SETUP_GUIDE.md             # Detailed setup
├── USAGE_GUIDE.md             # Usage instructions
└── README.md                  # This file
```

## How It Works

### 1. Email Fetching
- Connects via Gmail API (read-only)
- Fetches promotional emails based on query
- Supports pagination for large inboxes

### 2. Code Extraction
**Conservative approach** - only extracts codes with clear context:
- Near keywords: "code", "promo", "coupon", "checkout"
- Format: Code + number (SAVE20, FLIGHT40)
- Context: "Use XXXXX at checkout"

**Filters out:**
- Random capitalized words
- Generic business terms
- All-letter words without promo context

### 3. Merchant Detection
**Priority order:**
1. Sender email domain (most reliable)
2. Explicit brand mentions ("From Southwest")
3. Subject line pattern ("Brand Name - Subject")
4. Smart extraction with marketing phrase removal

### 4. Dashboard Generation
- HTML + CSS + JavaScript
- No external dependencies
- Works offline once generated
- Self-contained single file

## Examples

### Input: Gmail Promotional Email
```
From: deals@southwest.com
Subject: Southwest Airlines - Flash Sale: 40% Off

Use promo code FLIGHT40 at checkout to save 40% off.
Expires October 20, 2025.
```

### Output: Dashboard Entry
| Merchant | Code | Discount | Expires | Category | Urgency |
|----------|------|----------|---------|----------|---------|
| Southwest Airlines | FLIGHT40 [Copy] | 40% off | Oct 20, 2025 | Flights | 3 days |

## Automation

### Weekly Cron Job

```bash
# Run every Monday at 9 AM
0 9 * * 1 cd /path/to/gmail-promo-agent && python gmail_agent.py
```

### Email Report

See `USAGE_GUIDE.md` for instructions on automatically emailing the dashboard to yourself or others.

## Performance

- **Processes 50 emails** in ~10 seconds
- **Dashboard loads** instantly (<100KB)
- **Works offline** once generated
- **No external API calls** after generation

## Security

✅ **Read-only Gmail access** - cannot send, delete, or modify emails  
✅ **Local processing** - no data sent to external servers  
✅ **Credentials stay local** - never committed to git  
✅ **OAuth 2.0** - secure authentication  

**Important:** Never commit `credentials.json` or `token.json` to version control!

## Troubleshooting

### "No promos found"
- Check Gmail query in `config.yaml`
- Verify you have promotional emails in timeframe
- Try broader query: `"newer_than:30d"`

### "Too few codes extracted"
- This is intentional! Conservative extraction prevents false positives
- Run `check_merchants.py` to verify quality
- Real promo rate: typically 10-20% of promotional emails

### "Merchant names unclear"
- Agent prioritizes sender domain (most reliable)
- Some marketing emails have poor sender info
- Extraction should improve over time with more patterns

## Results

### Before
- 117 "codes" extracted
- 90% false positives (LIVE, READY, CREDIT, etc.)
- Unusable dashboard

### After
- 6 real codes extracted
- 0% false positives
- Clean, actionable dashboard

**Quality over quantity!**s

## Contributing

Contributions welcome! Areas for improvement:

- Additional promo code patterns
- Better discount extraction
- More category keywords
- UI enhancements
- Additional export formats

## License

MIT License - see LICENSE file

## Acknowledgments

Built with:
- Google Gmail API
- Python 3
- BeautifulSoup4 (HTML parsing)
- Jinja2 (templating)

## Support

For setup help, see:
- `SETUP_GUIDE.md` - Detailed setup instructions
- `USAGE_GUIDE.md` - Usage examples and tips
- `IMPROVEMENTS.md` - Technical details on improvements

## Author

Created as an AI-assisted project to solve the problem of cluttered promotional inboxes.

---

**Star this repo if you find it useful! ⭐**