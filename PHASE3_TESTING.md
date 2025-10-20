# Phase 3 Testing Guide: Real Gmail Integration

## 🎯 What We're Testing

Phase 3 connects to YOUR real Gmail account and extracts REAL promo codes from your inbox.

---

## ⚠️ IMPORTANT: You Need credentials.json

For testing, you still need to use YOUR Google Cloud credentials. Here's why:

**Why?**
- We're testing with YOUR Gmail account
- In production, the end user won't need this (you'll manage credentials centrally)
- For now, each developer needs their own credentials for testing

**Already have credentials.json from earlier?**
✅ Great! It should still be in your project folder.

**Don't have it or need a new one?**
Follow the Quick Setup below.

---

## 🚀 Quick Setup (If You Don't Have credentials.json)

### 1. Go to Google Cloud Console
https://console.cloud.google.com

### 2. Select Your Project
(Or create new one: "Gmail Promo Agent Test")

### 3. Enable Gmail API
- APIs & Services → Library
- Search "Gmail API"
- Click "Enable"

### 4. Create OAuth Credentials
- APIs & Services → Credentials
- Click "Create Credentials" → "OAuth client ID"
- Application type: **"Web application"** (important!)
- Name: "Gmail Promo Agent Local"
- Authorized redirect URIs: **Add this exactly:**
  ```
  http://localhost:8000/api/auth/callback
  ```
- Click "Create"

### 5. Download Credentials
- Click the download icon (⬇️) next to your new credential
- Save as `credentials.json`
- **Place in your project root directory:**
  ```
  ~/Desktop/gmail_promo_agent/credentials.json
  ```

### 6. Add Yourself as Test User
- OAuth consent screen
- Scroll to "Test users"
- Click "+ ADD USERS"
- Add your Gmail address
- Click "Save"

---

## ✅ Phase 3 Testing Steps

### Step 1: Update Dependencies

```bash
cd ~/Desktop/gmail_promo_agent

# Install new packages
pip install -r requirements.txt
```

### Step 2: Verify Files

```bash
# Check you have these files:
ls -la credentials.json      # OAuth config
ls -la gmail_service.py      # New file
ls -la api_server.py         # Updated
ls -la promo_agent.db        # Database
```

### Step 3: Restart API Server

```bash
# Stop old server (Ctrl+C)

# Start new server
python api_server.py
```

**Expected output:**
```
🚀 Gmail Promo Agent API Starting...
✓ Database already exists
📍 Server running at: http://localhost:8000
📚 API docs available at: http://localhost:8000/docs
```

### Step 4: Open Test Page

```bash
open test_frontend.html
```

### Step 5: Test OAuth Flow

Click buttons in this order:

#### A. Create Test User
1. Click **"Create Test User"**
2. Should show success

#### B. Check Gmail Status (Before Connecting)
1. Click **"Check Gmail Status"**
2. Should show: `"connected": false`

#### C. Connect Gmail
1. Click **"Connect Gmail"**
2. A new browser window should open
3. **Sign in to your Gmail account**
4. You'll see: "Google hasn't verified this app" 
   - Click **"Advanced"**
   - Click **"Go to Gmail Promo Agent Local (unsafe)"**
5. Click **"Allow"**
6. Window should show: "Gmail connected successfully! You can close this window."
7. Close that window

#### D. Check Gmail Status (After Connecting)
1. Back in test page, click **"Check Gmail Status"**
2. Should show:
   ```json
   {
     "connected": true,
     "email": "your@gmail.com"
   }
   ```

#### E. Scan for REAL Promos
1. Click **"Scan for Promos"**
2. Wait 5-10 seconds (it's scanning your actual Gmail!)
3. Should show:
   ```json
   {
     "success": true,
     "total_promos": 6,  // Your actual count
     "emails_scanned": 50,
     "message": "Successfully scanned..."
   }
   ```

#### F. View Your Promos
1. Click **"Get Promos"**
2. You should see YOUR REAL promo codes from Gmail!
3. They should have real merchant names
4. Real expiration dates
5. Real categories

#### G. Check Stats
1. Click **"Get Stats"**
2. Should show statistics about YOUR codes

---

## 🎉 SUCCESS CRITERIA

Phase 3 is working if:

✅ OAuth flow completes without errors  
✅ "Check Gmail Status" shows `connected: true`  
✅ Scan returns YOUR real promo codes  
✅ Codes show real merchant names (not "Explore Fall")  
✅ Expiration dates are real  
✅ Categorization makes sense  
✅ Stats match the number of codes found  

---

## 🔍 What Should You See?

### Before Phase 3:
- Sample data only (FALL40, PRESALE, etc.)
- Same 3 codes every time
- Not from your inbox

### After Phase 3:
- YOUR actual promo codes
- From YOUR Gmail promotional folder
- Real merchants you recognize
- Real expiration dates
- Matches what's in your inbox

---

## 🐛 Troubleshooting

### "credentials.json not configured"
**Fix:** Make sure `credentials.json` is in project root directory

### "Invalid redirect URI"
**Fix:** In Google Cloud Console, make sure redirect URI is EXACTLY:
```
http://localhost:8000/api/auth/callback
```

### "Access blocked" during OAuth
**Fix:** Add yourself as a test user in OAuth consent screen

### "Gmail not connected" after authorizing
**Fix:**
1. Click "Connect Gmail" again
2. Make sure you clicked "Allow" in the OAuth window
3. Check browser console for errors

### No promo codes found
**Possible reasons:**
1. You actually don't have promo emails in last 7 days (check Gmail)
2. They're not in "Promotions" category
3. No codes with clear context (conservative extraction)

**Try:**
```bash
# Check your Gmail promotions folder manually
# Do you have promotional emails in the last 7 days?
# Do any have promo codes like "SAVE20" or "Use code XXXXX"?
```

### Scan takes a long time
**Normal!** Scanning 50 emails from Gmail API takes 10-30 seconds depending on:
- Email size
- Number of emails
- Internet speed
- Gmail API rate limits

---

## 📊 Expected Results

### Typical Scan Results:
- **Emails scanned:** 20-50 (depending on how many promos you get)
- **Codes found:** 3-15 (only real codes with context)
- **Categories:** 2-6 (based on your emails)

**Remember:** We use conservative extraction, so:
- Fewer codes = Higher quality
- No false positives like "LIVE" or "CREDIT"
- Only codes with clear context

---

## 🔐 Security Note

**Your OAuth token is:**
- ✅ Stored encrypted in database
- ✅ Only accessible to your user account
- ✅ Can be revoked anytime
- ✅ Read-only access (cannot send/delete emails)

**To revoke access:**
1. Click "Disconnect Gmail" in test page
2. Or visit: https://myaccount.google.com/permissions
3. Remove "Gmail Promo Agent"

---

## 🎯 Next Steps After Phase 3

Once Phase 3 is confirmed working:

**Phase 4: React Frontend**
- Build professional web interface
- Replace test page with real UI
- Add refresh button, filters, search
- Mobile-responsive design

**Phase 5: Production Deploy**
- Deploy to Railway/Vercel
- Use environment variables for credentials
- Add rate limiting
- Set up monitoring

---

## ✋ STOP HERE

Test Phase 3 completely before moving forward.

**Confirm these work:**
1. OAuth connection
2. Real Gmail scanning
3. Your actual promo codes appear
4. Data persists in database
5. All test buttons work

**Then report back:**
- How many promo codes were found?
- Do they look accurate?
- Any errors in the console?
- Screenshots welcome!

---

Ready to test? Let's do this! 🚀