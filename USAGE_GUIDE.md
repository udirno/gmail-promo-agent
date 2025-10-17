# Usage Guide - Gmail Promo Agent

## Overview

This tool transforms your cluttered promotional inbox into a clean, actionable dashboard. Instead of clicking through dozens of emails, you get a single, shareable page showing all your active promo codes sorted by urgency and value.

## Quick Start

```bash
# Run the agent (after initial setup)
python gmail_agent.py

# Open your dashboard
open promo_dashboard.html
```

That's it! Your dashboard is ready to use and share.

---

## The Dashboard

### What You Get

**A professional, interactive web page featuring:**

1. **Quick Stats** - Total offers, expiring soon count, category breakdown
2. **Search Bar** - Find codes instantly by name, discount, or source
3. **Category Filters** - One-click filtering by Flights, Food, Retail, etc.
4. **Sortable Columns** - Click any column header to sort
5. **Urgency Indicators** - Color-coded expiration warnings
6. **One-Click Copy** - Copy any code with a single button click
7. **Mobile Responsive** - Works perfectly on phone, tablet, or desktop

### Dashboard Features

#### Urgency Column
Tells you at a glance which deals need immediate action:

- **Red** = Expires today or tomorrow (ACT NOW)
- **Orange** = Expires in 2-3 days (HIGH PRIORITY)
- **Yellow** = Expires in 4-7 days (MEDIUM)
- **Green** = Expires in 7+ days (LOW)
- **Gray** = Unknown expiration

#### Smart Sorting
By default, shows:
1. Expiring soonest first (so you never miss a deal)
2. Within same urgency, highest value deals first

#### Category Filters
Quick access to specific types of deals:
- **All** - See everything
- **Expiring Soon** - Only show codes expiring this week
- **Flights, Food, Retail, etc.** - Category-specific filtering

#### Search Functionality
Type anything to instantly filter:
- Code names: "SAVE20"
- Discount amounts: "50%"
- Source: "United Airlines"
- Multiple words: "pizza 30%"

---

## Real-World Use Cases

### Use Case 1: Family Shopping Planning

**Scenario:** It's Saturday morning, you're planning the week's shopping.

**How to use:**
1. Open `promo_dashboard.html`
2. Click "Expiring Soon" filter
3. Check "Food" and "Retail" categories
4. Note codes expiring this week
5. Click "Copy" buttons and paste into your shopping notes
6. Share dashboard link with family via email/text

**Time saved:** 15-20 minutes vs reading individual emails

### Use Case 2: Business Travel

**Scenario:** Need to book flights and hotels for upcoming trip.

**How to use:**
1. Open dashboard on your phone
2. Filter by "Flights" and "Hotels"
3. Sort by discount value (click "Discount" column)
4. See best deals first
5. Copy codes directly into booking sites

**Time saved:** 10-15 minutes of email searching

### Use Case 3: Team Expense Management

**Scenario:** You manage a team, want to share available discounts.

**How to use:**
1. Run the agent weekly
2. Email `promo_dashboard.html` to your team
3. They can search/filter for relevant deals
4. Everyone has the same up-to-date information

**Time saved:** Eliminates back-and-forth "do we have a code for X?" emails

### Use Case 4: Urgent Deal Check

**Scenario:** About to checkout online, wondering if you have a code.

**How to use:**
1. Quick open dashboard on phone
2. Search for the store name
3. Copy code if available
4. Complete purchase

**Time saved:** 2-3 minutes vs inbox search

---

## Sharing Your Dashboard

### Option 1: Email/Text
```bash
# The HTML file is self-contained - just attach and send
# Recipients can open directly in any browser
```

### Option 2: Cloud Storage
```bash
# Upload to Dropbox/Google Drive/iCloud
# Share link with family/team
```

### Option 3: Personal Website
```bash
# If you have a website, upload promo_dashboard.html
# Access from anywhere via URL
```

### Option 4: Print to PDF
```bash
# Open dashboard in browser
# File > Print > Save as PDF
# Great for offline reference
```

---

## Customization

### Adjust Time Range

Edit `config.yaml`:

```yaml
gmail:
  # Get last 3 days only (for daily checks)
  query: "category:promotions newer_than:3d"
  
  # Get last month (for comprehensive view)
  query: "category:promotions newer_than:30d"
```

### Add Custom Categories

Edit `categories.json`:

```json
{
  "Grocery": ["grocery", "supermarket", "instacart"],
  "Your Category": ["keyword1", "keyword2"]
}
```

### Change Dashboard Title

Edit `dashboard_generator.py`, line ~160:

```python
<h1>Our Family Promo Codes</h1>
```

---

## Automation Options

### Weekly Email Report

Create `send_report.py`:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def email_dashboard(recipients, dashboard_path='promo_dashboard.html'):
    sender = "your-email@gmail.com"
    password = "your-app-password"  # Use Gmail app password
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = f'Weekly Promo Codes - {datetime.now().strftime("%B %d, %Y")}'
    
    body = "Here are this week's promo codes. Open the attached file in your browser."
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach dashboard
    with open(dashboard_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename=promo_codes.html')
        msg.attach(part)
    
    # Send
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)

# Usage
email_dashboard(['family@example.com', 'friend@example.com'])
```

Run via cron every Monday:
```bash
0 9 * * 1 cd /path/to/project && python gmail_agent.py && python send_report.py
```

---

## Tips for Maximum Efficiency

### 1. Bookmark the Dashboard
Save `file:///path/to/promo_dashboard.html` in your browser for instant access.

### 2. Mobile Home Screen Shortcut
On iPhone/Android, add the dashboard to your home screen for app-like access.

### 3. Use Search Shortcuts
Common searches to save time:
- "50" - Find all 50% off deals
- "free" - Find free shipping or BOGO offers
- "$" - Find dollar-amount discounts
- Store names - "pizza", "airline", "clothing"

### 4. Weekly Routine
Set a reminder to run the agent every Monday morning:
- Fresh codes for the week
- Clear out expired deals
- Share with family during breakfast

### 5. Pre-Shopping Check
Before any online purchase, quick check:
1. Open dashboard
2. Search store name
3. Copy code if available
4. Save money!

---

## Troubleshooting

### Dashboard won't open
- Make sure you're opening `promo_dashboard.html` (not the .json or .md files)
- Try different browser if one doesn't work
- File should work offline, no internet needed to view

### Codes showing as expired
- Run the agent again to refresh: `python gmail_agent.py`
- Expired codes are automatically removed from the dashboard

### Can't find a specific code
- Use the search box - searches all text
- Try searching by store name, not just code
- Check if it's in a different category than expected

### Sharing not working
- Make sure you're sending the .html file, not a screenshot
- Recipients need to "download" or "save" the attachment, then open it
- Works in any modern browser (Chrome, Firefox, Safari, Edge)

---

## Privacy & Security

### What's Shared
- Dashboard contains only promo codes, discounts, and email subjects
- No personal information
- No Gmail credentials
- No authentication required to view

### What's Safe to Share
✅ Promo dashboard (promo_dashboard.html)
✅ JSON data file (if recipient wants structured data)

### What to NEVER Share
❌ credentials.json (OAuth secrets)
❌ token.json (Gmail access token)
❌ Your Gmail password

---

## Performance Notes

**Dashboard loads instantly** - it's a single HTML file with no external dependencies

**Works offline** - once generated, no internet needed to view

**No tracking** - completely private, no analytics or external scripts

**Lightweight** - typical dashboard is <100KB even with 200+ codes

---

## Next Steps

1. ✅ Run agent: `python gmail_agent.py`
2. ✅ Open dashboard: `open promo_dashboard.html`
3. ✅ Bookmark it for quick access
4. ✅ Set up weekly automation (optional)
5. ✅ Share with family/team (optional)

**Questions?** Check README.md or open an issue on GitHub.

---

**Remember:** The goal is to SAVE TIME. If you're spending more than 30 seconds finding a code, the tool is working!