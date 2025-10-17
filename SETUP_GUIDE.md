# 🚀 Setup Guide - Gmail Promo Agent

Complete step-by-step guide to get your Gmail Promo Agent running.

## Prerequisites

- Python 3.8 or higher
- Gmail account
- Google Cloud account (free)
- Basic command line knowledge

## Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd gmail-promo-agent

# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import googleapiclient; print('✓ Google API Client installed')"
python -c "import bs4; print('✓ BeautifulSoup installed')"
python -c "import jinja2; print('✓ Jinja2 installed')"
```

## Step 2: Google Cloud Console Setup

### Create Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Select a Project" → "New Project"
3. Name it "Gmail Promo Agent" (or your choice)
4. Click "Create"

### Enable Gmail API

1. In the Cloud Console, navigate to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click on it, then click "Enable"
4. Wait for activation (usually instant)

### Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure consent screen first:
   - User Type: External
   - App name: "Gmail Promo Agent"
   - User support email: your email
   - Developer contact: your email
   - Scopes: Add `gmail.readonly`
   - Test users: Add your Gmail address
   - Click "Save and Continue"

4. Back to Create OAuth client ID:
   - Application type: "Desktop app"
   - Name: "Gmail Promo Agent Client"
   - Click "Create"

5. Download the JSON file:
   - Click the download icon (⬇️) next to your new credential
   - Save as `credentials.json` in your project root

## Step 3: Project Configuration

### Verify File Structure

```
gmail-promo-agent/
├── credentials.json          ← You just downloaded this
├── gmail_agent.py
├── promo_parser.py
├── demo_simulation.py
├── config.yaml
├── categories.json
├── report_template.md
├── requirements.txt
└── README.md
```

### Configure Settings

Edit `config.yaml`:

```yaml
gmail:
  user: "me"
  query: "category:promotions newer_than:7d"  # Adjust timeframe
  credentials_path: "./credentials.json"

report:
  output_path: "./weekly_promo_report.md"
  template_path: "./report_template.md"
  categories_path: "./categories.json"
```

**Query Options:**
- `newer_than:3d` - Last 3 days
- `newer_than:7d` - Last week (default)
- `newer_than:14d` - Last 2 weeks
- `newer_than:30d` - Last month

**Advanced Queries:**
```yaml
# From specific sender
query: "from:deals@example.com newer_than:7d"

# With specific subjects
query: "subject:(sale OR discount) newer_than:7d"

# Multiple criteria
query: "category:promotions (discount OR coupon OR deal) newer_than:7d"
```

## Step 4: First Run (OAuth Authorization)

### Important: Two Different JSON Files!

⚠️ **Common confusion:** There are TWO different JSON files:

1. **`credentials.json`** (OAuth Client Config)
   - Downloaded from Google Cloud Console
   - Contains `client_id`, `client_secret`, `redirect_uris`
   - Used to START the authentication process
   - You create this in Step 2

2. **`token.json`** (User Authorization Token)
   - Created AUTOMATICALLY after first run
   - Contains `access_token`, `refresh_token`
   - Used for subsequent runs
   - Don't create this manually!

### Run the Agent

```bash
# First time run
python gmail_agent.py
```

**What happens on FIRST run:**

```
============================================================
Gmail Promo Email Agent - Weekly Summary
============================================================

[1/5] Connecting to Gmail...
🔐 First time setup - Opening browser for authentication...
   1. Sign in to your Gmail account
   2. Grant read-only access
   3. Return here after authorization
```

1. Browser opens automatically
2. Sign in to your Gmail account
3. You'll see "Google hasn't verified this app" warning - click "Advanced" → "Go to Gmail Promo Agent (unsafe)"
4. Review permissions (read-only Gmail access)
5. Click "Allow"
6. Browser shows "The authentication flow has completed"
7. Close browser and return to terminal

```
✓ Authentication successful! Token saved to token.json
✓ Connected to Gmail API

[2/5] Fetching promotional emails...
```

8. Agent continues processing your emails

**Generated Files:**
- `token.json` - Saved authentication (auto-created, keep secret!)
- `weekly_promo_report.md` - Your promo report
- `weekly_promo_report.json` - Structured data backup

### Subsequent Runs

After the first run, it's much simpler:

```bash
python gmail_agent.py
```

The agent will use the saved `token.json` and won't open the browser again!

## Step 5: Test with Demo Mode

Before connecting to Gmail, test with sample data:

```bash
python demo_simulation.py
```

**Expected Output:**
```
======================================================================
GMAIL PROMO AGENT - DEMO SIMULATION
======================================================================

📧 Processing 6 sample promotional emails...

[1/6] Processing: Flash Sale: 40% Off All Flights...
[2/6] Processing: Buy One Get One Free - Papa's Pizza...
...

✓ Extracted 8 promotional offers
✓ After deduplication: 7 unique offers

📊 CATEGORY BREAKDOWN:
----------------------------------------------------------------------
✈️ Flights: 2 offer(s)
🍕 Food: 2 offer(s)
...

✅ DEMO COMPLETE!
📄 Markdown report saved: demo_weekly_report.md
📄 JSON data saved: demo_promos.json
```

## Step 6: Verify Output

### Check Markdown Report

```bash
# View report
cat weekly_promo_report.md

# Or open in your editor
code weekly_promo_report.md  # VS Code
nano weekly_promo_report.md  # Terminal editor
```

**Example Report:**

```markdown
# 🎉 Weekly Promo Summary

**Generated:** October 17, 2025 at 2:30 PM  
**Total Offers:** 15  
**Categories:** 5

---

## ✈️ Flights

### FLIGHT40
- **Discount:** 40% off
- **Expires:** October 20, 2025
- **From:** Flash Sale: 40% Off All Flights...
```

### Check JSON Data

```bash
# Pretty print JSON
python -m json.tool weekly_promo_report.json
```

## Troubleshooting

### Issue: "Authorized user info was not in the expected format"

**Error message:**
```
ValueError: Authorized user info was not in the expected format, 
missing fields client_id, refresh_token, client_secret.
```

**Cause:** The code is trying to read `credentials.json` as if it's a `token.json` file (they have different formats).

**Solutions:**
1. Make sure you have `credentials.json` (not `token.json`) in your project folder
2. Delete any existing `token.json`: `rm token.json`
3. Your `credentials.json` should look like this:
   ```json
   {
     "installed": {
       "client_id": "xxxxx.apps.googleusercontent.com",
       "project_id": "your-project",
       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
       "token_uri": "https://oauth2.googleapis.com/token",
       "client_secret": "xxxxx",
       "redirect_uris": ["http://localhost"]
     }
   }
   ```
4. Run the agent again: `python gmail_agent.py`
5. Complete the browser authentication flow
6. This will create the proper `token.json` automatically

### Issue: "credentials.json not found"

**Solution:**
```bash
# Verify file exists
ls -la credentials.json

# If missing, re-download from Google Cloud Console
# Make sure it's named exactly "credentials.json"
```

### Issue: "Invalid credentials"

**Solutions:**
1. Delete `token.json`: `rm token.json`
2. Re-run: `python gmail_agent.py`
3. Complete OAuth flow again

### Issue: "No promos found"

**Solutions:**
1. Check your Gmail promotions tab has emails
2. Expand time range in `config.yaml`:
   ```yaml
   query: "category:promotions newer_than:30d"
   ```
3. Use broader query:
   ```yaml
   query: "is:unread newer_than:7d"
   ```

### Issue: "Permission denied" or "Access blocked"

**Solutions:**
1. Verify OAuth consent screen is configured
2. Add your email as test user
3. Make sure app is in "Testing" mode (not Production)
4. Check that Gmail API is enabled

### Issue: "Rate limit exceeded"

**Solutions:**
1. Reduce `max_results` in code (default 50)
2. Wait a few minutes before retrying
3. Check quota limits in Google Cloud Console

### Issue: HTML emails not parsing correctly

**Solutions:**
```bash
# Install lxml for better HTML parsing
pip install lxml

# Verify installation
python -c "import lxml; print('✓ lxml installed')"
```

## Advanced Configuration

### Custom Categories

Edit `categories.json` to add your own:

```json
{
  "Fitness": ["gym", "workout", "fitness", "yoga"],
  "Streaming": ["netflix", "hulu", "spotify", "subscription"],
  "Your Category": ["keyword1", "keyword2", "keyword3"]
}
```

### Custom Report Template

Edit `report_template.md` with Jinja2 syntax:

```markdown
# My Custom Report

Generated on: {{ generated_date }}

{% for category, promos in categorized_promos.items() %}
## {{ category }} ({{ promos|length }} deals)

{% for promo in promos %}
**{{ promo.code }}** - {{ promo.discount }}
{% if promo.expiration %}*Expires: {{ promo.expiration }}*{% endif %}

{% endfor %}
{% endfor %}
```

### Schedule Automatic Runs

**Mac/Linux (cron):**

```bash
# Edit crontab
crontab -e

# Add line (run every Monday at 9 AM):
0 9 * * 1 cd /path/to/gmail-promo-agent && /usr/bin/python3 gmail_agent.py
```

**Windows (Task Scheduler):**

1. Open Task Scheduler
2. "Create Basic Task"
3. Name: "Gmail Promo Agent"
4. Trigger: Weekly, Monday, 9:00 AM
5. Action: Start a program
   - Program: `C:\Python39\python.exe`
   - Arguments: `gmail_agent.py`
   - Start in: `C:\path\to\gmail-promo-agent`
6. Finish

## Security Best Practices

### Protect Your Credentials

```bash
# Add to .gitignore
echo "credentials.json" >> .gitignore
echo "token.json" >> .gitignore
echo "*.json" >> .gitignore

# Never commit these files!
git status  # Verify they're ignored
```

### Limit Permissions

The agent only uses `gmail.readonly` scope:
- ✅ Can read emails
- ❌ Cannot send emails
- ❌ Cannot delete emails
- ❌ Cannot modify emails

### Regular Security Audits

1. Review connected apps: https://myaccount.google.com/permissions
2. Revoke access if no longer needed
3. Regenerate credentials periodically

## Next Steps

1. ✅ Run demo mode successfully
2. ✅ Connect to Gmail and generate first report
3. ✅ Customize categories for your needs
4. ✅ Schedule weekly automatic runs
5. ✅ Share feedback and improvements!

## Need Help?

- **Documentation:** Check README.md
- **Issues:** Open GitHub issue
- **Gmail API:** https://developers.google.com/gmail/api
- **OAuth Help:** https://developers.google.com/identity/protocols/oauth2

---

**You're all set! Happy deal hunting! 🎉**