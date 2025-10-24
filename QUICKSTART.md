# Quickstart Guide - Get Running in 5 Minutes

**Goal:** From zero to working promo code dashboard in approximately 5 minutes.

---

## Time Breakdown

- Step 1: Install Python (2 min, one-time)
- Step 2: Download the project (30 sec)
- Step 3: Set up Google credentials (2 min, one-time)
- Step 4: Run the app (30 sec)

**Total: ~5 minutes** (Steps 1 & 3 are one-time only!)

---

## Prerequisites

- A Gmail account (the one you want to scan for promo codes)
- 5 minutes of uninterrupted time
- Administrator access to your computer (to install Python)

---

## Step 1: Install Python (2 minutes, ONE-TIME)

### Check if You Already Have Python

Open your terminal/command prompt:
- **Mac:** Press `Cmd + Space`, type "Terminal", press Enter
- **Windows:** Press `Win + R`, type "cmd", press Enter

Type this command and press Enter:
```bash
python3 --version
```

**If you see something like** `Python 3.8.10` or higher - **Skip to Step 2!**

**If you get an error** - Continue below to install Python.

---

### Installing Python

#### On Mac:
```bash
# Install Homebrew (if you don't have it)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

#### On Windows:
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow "Download Python 3.x.x" button
3. Run the installer
4. **CHECK THE BOX** that says "Add Python to PATH" 
5. Click "Install Now"
6. Wait for installation to complete

#### On Linux:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip
```

### Verify Installation

Close and reopen your terminal, then run:
```bash
python3 --version
```

You should see: `Python 3.8.x` or higher.

---

## Step 2: Download the Project (30 seconds)

### Option A: Using Git (Recommended)

```bash
# Navigate to where you want the project
cd ~/Desktop

# Clone the repository
git clone https://github.com/udirno/gmail-promo-agent.git

# Enter the project folder
cd gmail-promo-agent

# Install dependencies
pip3 install -r requirements.txt
```

### Option B: Download ZIP

If you don't have Git:
1. Go to [github.com/udirno/gmail-promo-agent](https://github.com/udirno/gmail-promo-agent)
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to your Desktop
5. Open terminal and navigate to the folder:
   ```bash
   cd ~/Desktop/gmail-promo-agent-main
   pip3 install -r requirements.txt
   ```

**Wait for dependencies to install** (30 seconds - 1 minute)

---

## Step 3: Set Up Google Credentials (2 minutes, ONE-TIME)

### Why Do I Need This?

Google requires ANY app that accesses Gmail (even yours running locally) to have OAuth credentials. Think of it like creating an API key.

**Your data stays on your computer.** These credentials just let YOUR app talk to YOUR Gmail.

---

### 3.1: Go to Google Cloud Console

1. Open [console.cloud.google.com](https://console.cloud.google.com)
2. Sign in with your Gmail account

---

### 3.2: Create a New Project

1. Click the project dropdown at the top (says "Select a project")
2. Click "NEW PROJECT" in the top right
3. **Project name:** Type "Promo Code Manager" (or anything you like)
4. Click "CREATE"
5. Wait 10 seconds for it to create

**Make sure your new project is selected** (check the dropdown at top)

---

### 3.3: Enable Gmail API

1. In the left sidebar, click **"APIs & Services"** then **"Library"**
2. In the search box, type **"Gmail API"**
3. Click on **"Gmail API"** from the results
4. Click the blue "ENABLE" button
5. Wait for it to enable (5 seconds)

---

### 3.4: Configure OAuth Consent Screen

1. In the left sidebar, click **"APIs & Services"** then **"OAuth consent screen"**
2. Select **"External"** (unless you have a workspace account, then choose Internal)
3. Click "CREATE"

Fill in the form:
- **App name:** Promo Code Manager
- **User support email:** (your email - it auto-fills)
- **Developer contact:** (your email again)
- Leave everything else blank

4. Click "SAVE AND CONTINUE"
5. On the "Scopes" page, click "SAVE AND CONTINUE" (don't add anything)
6. On the "Summary" page, click "BACK TO DASHBOARD"

Now add yourself as a test user:
7. In the left sidebar, click **"Audience"**
8. Under the "Test users" section, click **"+ ADD USERS"**
9. Enter YOUR Gmail address (the one you want to scan)
10. Click "ADD"
11. Click "SAVE"

---

### 3.5: Create OAuth Credentials

1. In the left sidebar, click **"APIs & Services"** then **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"OAuth client ID"**
4. **Application type:** Choose **"Desktop app"**
5. **Name:** Type "Promo Agent Local Client"
6. Click "CREATE"

A popup appears with your credentials:
7. Click the "DOWNLOAD JSON" button
8. Save the file

---

### 3.6: Move Credentials File

You just downloaded a file called something like `client_secret_xxxxx.json`

**Rename it to:** `credentials.json`

**Move it to your project folder:**

```bash
# Mac/Linux - if the file is in Downloads:
mv ~/Downloads/client_secret_*.json ~/Desktop/gmail-promo-agent/credentials.json

# Windows (in Command Prompt):
move C:\Users\YourName\Downloads\client_secret_*.json C:\Users\YourName\Desktop\gmail-promo-agent\credentials.json
```

Or just drag and drop the file into your project folder and rename it!

**Verify it's there:**
```bash
# Should show "credentials.json"
ls credentials.json
```

---

## Step 4: Run the App! (30 seconds)

You're ready! Let's start the app:

```bash
# Make sure you're in the project folder
cd ~/Desktop/gmail-promo-agent

# Start the API server (use -u for unbuffered output)
python3 -u api_server.py
```

You should see:
```
Gmail Promo Agent API Starting...
Database already exists
Server running at: http://localhost:8000
API docs available at: http://localhost:8000/docs
```

**Leave this terminal window open!** (The server needs to keep running)

---

### 4.1: Open the Test Page

**Open a NEW terminal window** (keep the server running in the first one).

Navigate to your project directory and open the test page:
```bash
# Navigate to project folder
cd ~/Desktop/gmail-promo-agent

# Open test_frontend.html in your browser
open test_frontend.html   # Mac
start test_frontend.html  # Windows
```

You should see the API Test Page:

![API Test Page](screenshots/test_page.png)

---

### 4.2: Connect Your Gmail

1. Click **"Create Test User"** - You should see success message

2. Click **"Connect Gmail"**

3. A Google sign-in window will open:

![OAuth Consent Screen](screenshots/oauth_consent.png)

4. Sign in with your Gmail account
5. You'll see a warning: "Google hasn't verified this app"
   - Click "Advanced" then "Go to Promo Code Manager (unsafe)"
   - (It's "unsafe" because it's YOUR app, not verified by Google - this is normal!)
6. Click "Allow"
7. The window should say "Gmail connected successfully"
8. Close that window and return to the test page

---

### 4.3: Scan for Promo Codes

1. Click **"Scan for Promos"**

2. Wait 10-30 seconds while it scans your Gmail...

3. In your terminal, you should see:
```
Processing 50 emails...
Email 1/50: Found 1 promo(s) - Chase Center
  Code: SFHOOPS
Email 2/50: Found 1 promo(s) - CheapOair
  Code: FALL40
...
Total promos before deduplication: 15
Unique promos after deduplication: 12
```

4. Click **"Get Promos"** to see your promo codes!

![Extracted Promo Codes](screenshots/found_promos.png)

---

## You're Done!

You should now see a list of your promo codes extracted from your Gmail promotional folder.

Here's what a typical promotional email looks like before extraction:

![Promotional Email Example](screenshots/promo_email.png)

And here's what you get after extraction - clean, organized, searchable codes:

![Dashboard with Codes](screenshots/found_promos.png)

### What You Can Do Now:

**View Your Dashboard:**
```bash
# The scan created an HTML dashboard
open promo_dashboard.html   # Mac
start promo_dashboard.html  # Windows
xdg-open promo_dashboard.html  # Linux
```

**Re-scan for New Codes:**
- Just click "Scan for Promos" again on the test page
- Or restart the server and re-scan

**Share the Dashboard:**
- The `promo_dashboard.html` file is self-contained
- Email it to family or upload to Google Drive
- They can open it in any browser - no setup needed!

---

## Troubleshooting

### "credentials.json not found"

**Solution:** Make sure you:
1. Downloaded the JSON file from Google Cloud
2. Renamed it to exactly `credentials.json`
3. Placed it in the project root folder (same folder as `api_server.py`)

Run this to check:
```bash
ls credentials.json
```

---

### "Port 8000 already in use"

**Solution:** Another app is using port 8000.

Either:
- **Option A:** Find and stop that app
- **Option B:** Use a different port:
  ```bash
  # Edit api_server.py, change this line at the bottom:
  # port=8000  →  port=8001
  ```

---

### "Permission denied" during OAuth

**Solution:** Make sure you:
1. Added yourself as a test user in the Audience section
2. Are signing in with the same Gmail account

To fix:
1. Go back to [console.cloud.google.com](https://console.cloud.google.com)
2. APIs & Services → Audience
3. Under "Test users", click "+ ADD USERS" and add your Gmail address

---

### "No promo codes found"

**Possible reasons:**

1. **No promotional emails in last 7 days**
   - Check your Gmail promotional tab
   - Adjust time range in `config.yaml`: `query: "category:promotions newer_than:30d"`

2. **Promo codes don't have clear context**
   - The app uses conservative extraction (avoids false positives)
   - It only extracts codes near words like "Use code", "promo", etc.
   - This is intentional! Quality over quantity

3. **Emails aren't in "Promotions" category**
   - Gmail's automatic categorization might be off
   - Try a broader query in `config.yaml`: `query: "newer_than:7d"`

---

### "Module not found" errors

**Solution:** Install dependencies again:
```bash
pip3 install -r requirements.txt
```

If that doesn't work, try:
```bash
pip3 install --upgrade -r requirements.txt
```

---

### Still Stuck?

1. **Check the server logs** - Look at the terminal where `api_server.py` is running for error messages

2. **Try the demo mode** first to verify everything else works:
   ```bash
   python3 demo_simulation.py
   open demo_promo_dashboard.html
   ```

3. **Open a GitHub issue:**
   - Go to [github.com/udirno/gmail-promo-agent/issues](https://github.com/udirno/gmail-promo-agent/issues)
   - Click "New Issue"
   - Describe what step you're stuck on
   - Include any error messages

---

## Next Steps

Now that you have it working:

- **Read USAGE_GUIDE.md** - Learn all dashboard features
- **Read BLOG_POST.md** - Understand why local-first matters
- **Customize categories** - Edit `categories.json` to match your shopping habits
- **Schedule weekly scans** - Set up automation (instructions in USAGE_GUIDE.md)

---

## Quick Command Reference

```bash
# Start the server
python3 -u api_server.py

# Run demo (no Gmail needed)
python3 demo_simulation.py

# Check what codes were extracted
python3 check_merchants.py

# Re-initialize database if needed
python3 database.py

# View dashboard
open promo_dashboard.html
```

---

## Common Questions

### Do I need to do the Google Cloud setup every time?
**No!** Only once per computer. After the first time, just run `python3 api_server.py`.

### Can I use this on multiple computers?
**Yes!** Just clone the repo, copy your `credentials.json` file over, and run the OAuth setup once per computer.

### How often should I scan?
**Whenever you want!** Suggestions:
- Before shopping trips
- Weekly on Monday morning
- Before big sale events (Black Friday, etc.)

### Can others use my dashboard?
**Yes!** The `promo_dashboard.html` file is shareable via email, Google Drive, or text message. They can open it in any browser - no setup needed!

### Does this cost money?
**No!** Everything is free:
- The code is open source
- Gmail API is free (up to 250 requests/second)
- No subscriptions or hidden costs

---

**Congrats! You're all set up!**

Enjoy your organized promo codes and never waste time hunting through emails again.

**Questions?** [Open an issue on GitHub](https://github.com/udirno/gmail-promo-agent/issues)