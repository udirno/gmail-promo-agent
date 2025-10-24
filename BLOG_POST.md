# Why I Built a Local-First Promo Code Manager

*October 2025*

---

## The Problem

I had 73 unread promotional emails. When I needed a discount code, I spent 10 minutes clicking through my inbox.

Frustrating. There had to be a better way.

---

## Why Not Just Build a Web App?

The obvious solution: build a web app where users click "Sign in with Google" and get a dashboard.

**But would you actually trust a random web service with full Gmail access?**

I wouldn't.

When you give a web app Gmail access:
- Your credentials are stored on their server
- Your emails are processed remotely
- You can't verify what happens to your data
- Every breach is a potential leak

**I wanted something better.**

---

## The Local-First Approach

Instead of "give us your data, we'll process it," I built "run this on your computer, keep your data local."

### What This Means

**Privacy by design:**
- Data never leaves your machine
- No third party access
- No server breaches
- No terms of service changes

**Complete transparency:**
- Open source code you can inspect
- Runs on your machine
- You control everything

**Actually faster:**
- No network latency
- Works offline
- No subscription fees

---

## What The Tool Does

Here's a typical promotional email:

![Promotional Email](screenshots/promo_email.png)

The tool:
1. Scans your Gmail promotional folder
2. Extracts promo codes using pattern matching
3. Identifies merchants from sender domains
4. Tracks expiration dates
5. Generates a searchable interface

After one scan, you get this:

![Extracted Codes](screenshots/found_promos.png)

Clean, organized, searchable. No more hunting through emails.

---

## The Setup (5 Minutes)

Yes, local-first requires setup. But it's straightforward:

1. Install Python (5 minutes, one-time)
2. Clone the repo (1 command)
3. Create Google credentials (2 minutes, one-time)
4. Run the app (1 command)

When you connect, you authorize once:

![OAuth Screen](screenshots/oauth_consent.png)

**Total time: ~5 minutes.**

Compare this to creating accounts, entering payment info, reading terms of service, and wondering what they do with your data.

**I'll take the 5-minute setup.**

---

## Built in a Day with AI

I built this in 8 hours using Claude (Anthropic's AI).

**What AI did:**
- Wrote Gmail API integration
- Implemented OAuth correctly
- Created extraction logic
- Generated the interface
- Helped debug edge cases

**What I decided:**
- Architecture (local-first vs cloud)
- Privacy considerations
- User experience priorities
- What data to store and how

**The AI was a tool. I made the ethical decisions.**

---

## Why This Matters

This isn't just about promo codes. It's about a bigger question:

**As AI tools become more capable, where should we grant them access?**

AI email assistants, shopping helpers, schedulers, document processors - each wants access to sensitive data.

**Do we really want all of that in the cloud?**

Local-first alternatives are viable. They just require us to prioritize privacy over convenience.

---

## The Tradeoffs

**Web apps have:**
- One-click setup
- Access from anywhere
- Automatic updates

**Local-first has:**
- Complete privacy
- No ongoing costs
- You own your data

For a tool accessing my personal emails, privacy wins.

---

## Who This Is For

This tool is for people who:
- Value privacy over convenience
- Are comfortable with basic command line
- Want to understand what software does
- Prefer owning tools rather than renting them

Not for:
- People who want zero setup
- Mobile-first users
- Teams needing centralized data

**Different tools for different needs.**

---

## Try It Yourself

The project is open source: [github.com/udirno/gmail-promo-agent](https://github.com/udirno/gmail-promo-agent)

Setup takes 5 minutes: [QUICKSTART.md](QUICKSTART.md)

**What you get:**
- Your promo codes organized
- Experience with local-first tools
- Code you can inspect and modify
- Privacy-respecting software

**What you don't get:**
- Slick onboarding
- Mobile app
- Cloud sync
- Any data leaving your computer

**For me, that last point makes it worth it.**

---

## Final Thought

I'm not saying everyone should abandon cloud services.

I'm saying **we should have the choice.**

With AI tools becoming more powerful and invasive, we need to be intentional about where we grant access.

**You can build useful AI-powered tools that respect user privacy.**

You just have to make it a priority.

---

**Try it:** [QUICKSTART.md](QUICKSTART.md)

**Questions?** [Open an issue](https://github.com/udirno/gmail-promo-agent/issues)

---

*Built in a day with AI. Kept local by design.*