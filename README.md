# 🎉 Gmail Promo Email AI Agent

An intelligent agent that automatically scans your Gmail inbox, extracts promotional offers, categorizes them, and generates beautiful weekly summary reports.

## ✨ Features

- **Gmail Integration** - Securely connects via Google's official API
- **Smart Extraction** - Detects promo codes, discounts, and expiration dates
- **HTML Support** - Handles both plain text and HTML emails
- **Intelligent Categorization** - Auto-sorts into Flights, Food, Retail, Entertainment, etc.
- **Deduplication** - Removes duplicate codes automatically
- **Beautiful Reports** - Generates formatted Markdown summaries with emojis
- **JSON Export** - Saves structured data for further processing

## 🎯 Enhanced Features (New!)

### Extraction Improvements
- ✅ Multiple discount format detection (%, $, BOGO, free shipping)
- ✅ Expiration date extraction (various formats)
- ✅ HTML email parsing with BeautifulSoup
- ✅ False positive filtering (no more "HTTP" or "EMAIL" as codes)
- ✅ Context-aware categorization using both subject and body

### Report Enhancements
- ✅ Category emojis for visual appeal
- ✅ Statistics dashboard (total offers, category breakdown)
- ✅ Sorted by popularity
- ✅ Jinja2 templating for customization
- ✅ JSON backup for data analysis

### Code Quality
- ✅ Type hints throughout
- ✅ Comprehensive error handling
- ✅ Pagination support for large inboxes
- ✅ Progress indicators
- ✅ Detailed logging

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repo-url>
cd gmail-promo-agent

# Install dependencies
pip install -r requirements.txt
```

### 2. Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (or use existing)
3. Enable the Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials as `credentials.json`
6. Place in project root directory

### 3. Configuration

Edit `config.yaml` to customize:

```yaml
gmail:
  query: "category:promotions newer_than:7d"  # Adjust timeframe
  credentials_path: "./credentials.json"
  
report:
  output_path: "./weekly_promo_report.md"
  template_path: "./report_template.md"
  categories_path: "./categories.json"
```

### 4. Run the Agent

```bash
# First run - will open browser for OAuth
python gmail_agent.py

# Subsequent runs - uses saved token
python gmail_agent.py
```

### 5. Demo Mode (No Gmail Required)

Test the agent with sample data:

```bash
python demo_simulation.py
```

## 📁 Project Structure

```
gmail-promo-agent/
├── gmail_agent.py          # Main agent logic
├── promo_parser.py         # Extraction & categorization
├── demo_simulation.py      # Demo with sample data
├── config.yaml             # Configuration
├── categories.json         # Category keyword mappings
├── report_template.md      # Markdown report template
├── requirements.txt        # Python dependencies
├── credentials.json        # Gmail API credentials (you create)
└── README.md               # This file
```

## 📊 Sample Output

After running, you'll get a report like this:

```markdown
# 🎉 Weekly Promo Summary

**Generated:** October 17, 2025 at 2:30 PM  
**Total Offers:** 15  
**Categories:** 5

---

## 📊 Quick Stats

- **Flights:** 4 offer(s)
- **Food:** 5 offer(s)
- **Retail:** 3 offer(s)
- **Entertainment:** 2 offer(s)
- **Other:** 1 offer(s)

---

## ✈️ Flights

### FLIGHT40
- **Discount:** 40% off
- **Expires:** October 20, 2025
- **From:** Flash Sale: 40% Off All Flights...

### CYBER60
- **Discount:** up to 60% off
- **Expires:** October 30, 2025
- **From:** Cyber Monday Travel Deals...
```

## 🎨 Customization

### Add New Categories

Edit `categories.json`:

```json
{
  "Flights": ["flight", "airline", "fare", "travel"],
  "Food": ["restaurant", "pizza", "meal", "delivery"],
  "Tech": ["laptop", "phone", "gadget", "electronics"],
  "Your Category": ["keyword1", "keyword2"]
}
```

### Customize Report Template

Edit `report_template.md` with Jinja2 syntax:

```markdown
{% for category, promos in categorized_promos.items() %}
## {{ category }}
{% for promo in promos %}
- **{{ promo.code }}** - {{ promo.discount }}
{% endfor %}
{% endfor %}
```

### Adjust Gmail Query

Modify `config.yaml`:

```yaml
gmail:
  # Last 3 days only
  query: "category:promotions newer_than:3d"
  
  # Include specific sender
  query: "category:promotions from:deals@example.com newer_than:7d"
  
  # Specific subject keywords
  query: "category:promotions subject:(sale OR discount) newer_than:7d"
```

## 🔧 Advanced Usage

### Scheduled Weekly Runs

**Using cron (Linux/Mac):**

```bash
# Run every Monday at 9 AM
0 9 * * 1 cd /path/to/project && python gmail_agent.py
```

**Using Task Scheduler (Windows):**

1. Open Task Scheduler
2. Create Basic Task
3. Set weekly trigger (Monday 9 AM)
4. Action: Start Program → `python.exe`
5. Arguments: `gmail_agent.py`
6. Start in: Your project directory

**Using Python schedule library:**

```python
import schedule
import time
from gmail_agent import main

schedule.every().monday.at("09:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Email the Report

Add to `gmail_agent.py`:

```python
import smtplib
from email.mime.text import MIMEText

def email_report(report_path, recipient):
    with open(report_path, 'r') as f:
        content = f.read()
    
    msg = MIMEText(content)
    msg['Subject'] = 'Weekly Promo Summary'
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = recipient
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('your-email@gmail.com', 'app-password')
        smtp.send_message(msg)
```

### Export to CSV

```python
import csv

def export_to_csv(promos, filename='promos.csv'):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['code', 'discount', 'category', 'expiration'])
        writer.writeheader()
        writer.writerows(promos)
```

## 🐛 Troubleshooting

### "Credentials not found"
- Ensure `credentials.json` is in project root
- Verify path in `config.yaml`
- Re-download from Google Cloud Console

### "No promos found"
- Check Gmail query in `config.yaml`
- Verify you have promotional emails in timeframe
- Try broader query: `"newer_than:30d"`

### HTML parsing issues
- Install lxml: `pip install lxml`
- BeautifulSoup will fall back to html.parser

### Rate limiting
- Gmail API has quota limits (check Google Cloud Console)
- Add delays between requests if processing many emails
- Consider caching results

## 🔒 Security Best Practices

1. **Never commit credentials**
   ```bash
   echo "credentials.json" >> .gitignore
   echo "token.json" >> .gitignore
   ```

2. **Use read-only scope**
   - Agent uses `gmail.readonly` scope only
   - Cannot send, delete, or modify emails

3. **Secure token storage**
   - Token is stored locally after first OAuth
   - Keep `token.json` secure

4. **Regular audits**
   - Review connected apps: https://myaccount.google.com/permissions
   - Revoke access if needed

## 📈 Future Enhancements

- [ ] AI-powered deal scoring (best deals first)
- [ ] Price tracking over time
- [ ] Browser extension for one-click code copying
- [ ] Mobile app notifications
- [ ] Multi-language support
- [ ] Calendar integration (add expiration reminders)
- [ ] Deal sharing with friends
- [ ] Cashback/rewards tracking

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Better promo code detection patterns
- Additional category keywords
- New report formats (HTML, PDF)
- Integration with deal-sharing platforms
- Machine learning for categorization

## 📝 License

MIT License - feel free to use and modify!

## 🆘 Support

- **Issues:** Open a GitHub issue
- **Questions:** Check existing issues or create new one
- **Gmail API Docs:** https://developers.google.com/gmail/api

## ⚡ Performance Tips

1. **Limit email fetch count** in config (default 50)
2. **Narrow time range** for faster processing
3. **Use specific queries** to reduce API calls
4. **Enable caching** for repeated runs

## 🎓 Learn More

- [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)
- [OAuth 2.0 Setup Guide](https://developers.google.com/identity/protocols/oauth2)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)

---

**Happy Deal Hunting! 🎉🛍️**