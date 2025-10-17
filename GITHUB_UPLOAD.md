# Upload to GitHub - Step by Step

## CRITICAL: Protect Your Credentials First!

Before uploading anything, we need to make sure your Gmail credentials and tokens are NOT uploaded.

### Step 1: Create .gitignore File

```bash
cd ~/Desktop/gmail_promo_agent

# Create .gitignore
cat > .gitignore << 'EOF'
# Credentials and Tokens - NEVER COMMIT THESE
credentials.json
token.json
*.json

# Except these JSONs which are safe
!categories.json
!package.json

# Generated reports and data
promo_dashboard.html
demo_promo_dashboard.html
weekly_promo_report.md
weekly_promo_report.json
demo_promos.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
EOF
```

### Step 2: Verify Credentials are Ignored

```bash
# IMPORTANT: Check that credentials.json won't be uploaded
git init
git add .
git status

# You should NOT see:
# - credentials.json
# - token.json
# - weekly_promo_report.json

# You SHOULD see:
# - gmail_agent.py
# - promo_parser.py
# - dashboard_generator.py
# - etc.
```

### Step 3: Initial Commit

```bash
git add .
git commit -m "Initial commit: Gmail Promo Agent with dashboard"
```

### Step 4: Create GitHub Repository

1. Go to https://github.com
2. Click the **"+"** icon (top right) → **"New repository"**
3. Fill in:
   - **Repository name:** `gmail-promo-agent`
   - **Description:** `AI agent that extracts promo codes from Gmail and generates an interactive dashboard`
   - **Visibility:** 
     - ✅ **Public** (if you want to share)
     - ⬜ **Private** (if you want to keep it private)
   - ⬜ Do NOT initialize with README (we already have files)
4. Click **"Create repository"**

### Step 5: Connect and Push

GitHub will show you commands. Use these:

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR-USERNAME/gmail-promo-agent.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Replace `YOUR-USERNAME` with your actual GitHub username!**

### Step 6: Verify Upload

1. Refresh your GitHub repository page
2. Check that you see all your Python files
3. **CRITICAL:** Verify that `credentials.json` and `token.json` are NOT visible
4. Check that README.md is displaying properly

---

## Sharing Your Project

Once uploaded, you can share:

**Repository URL:**
```
https://github.com/YOUR-USERNAME/gmail-promo-agent
```

**What Others Will See:**
- ✅ All your Python code
- ✅ README with setup instructions
- ✅ Demo simulation capability
- ✅ Sample dashboard screenshot
- ❌ Your Gmail credentials (safe!)
- ❌ Your generated reports (private)

---

## Future Updates

After making changes:

```bash
# Stage changes
git add .

# Commit with message
git commit -m "Description of what you changed"

# Push to GitHub
git push
```

---

## Add a Screenshot

To make your repo more impressive, add a dashboard screenshot:

```bash
# 1. Take a screenshot of your dashboard and save as dashboard_screenshot.png

# 2. Add to repo
git add dashboard_screenshot.png
git commit -m "Add dashboard screenshot"
git push
```

Then update README.md to include:
```markdown
## Dashboard Preview

![Dashboard Screenshot](dashboard_screenshot.png)
```

---

## Troubleshooting

### "git: command not found"
```bash
# Install git (Mac)
xcode-select --install

# Or install via Homebrew
brew install git
```

### "Permission denied (publickey)"
Use HTTPS instead of SSH:
```bash
git remote set-url origin https://github.com/YOUR-USERNAME/gmail-promo-agent.git
```

### "Accidentally committed credentials.json"

**DO THIS IMMEDIATELY:**

```bash
# Remove from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch credentials.json" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all

# Then regenerate new credentials from Google Cloud Console
```

---

## Security Checklist

Before sharing repository URL, verify:

- [ ] credentials.json is NOT in repository
- [ ] token.json is NOT in repository  
- [ ] .gitignore file is present
- [ ] No API keys or passwords in any files
- [ ] Generated reports are excluded

---

## Making It Look Professional

### Add Topics/Tags

On GitHub repo page:
1. Click ⚙️ next to "About"
2. Add topics: `gmail`, `promo-codes`, `python`, `automation`, `dashboard`, `email-parser`

### Add License

```bash
# Add MIT License
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

git add LICENSE
git commit -m "Add MIT License"
git push
```

---

## Example Repository Description

Use this for your GitHub repo description:

```
🎯 Gmail Promo Agent

An intelligent agent that connects to Gmail, extracts promotional codes 
from your inbox, and generates a clean, shareable dashboard. Features 
smart merchant detection, urgency tracking, and one-click code copying.

Built with Python | Gmail API | Interactive HTML Dashboard
```

---

Your project is now ready to share! 🚀