# How We Built Gmail Promo Agent with Claude

I was constantly drowning in promotional emails—airlines offering 40% off, restaurants with BOGO deals, retailers running flash sales. But whenever I actually needed a promo code, I'd waste 10 minutes clicking through my inbox, trying to remember which store sent what offer.

I wanted something simple: a searchable tool that could find all my Gmail promotions in seconds. But I wasn't willing to trust some random web app with full access to my Gmail account. I needed a solution that ran locally on my machine, kept my data private, and didn't require handing over credentials to a third party. No cloud processing, no external servers—just a clean local tool that respected my privacy.

Using Claude's AI assistance, I built the Gmail Promo Agent from scratch. We started with the core problem: connecting to Gmail's API securely using OAuth so only I have access to my emails. Then we built intelligent extraction logic that could parse promotional emails and identify real promo codes without generating false positives. Claude helped me implement conservative pattern matching—the system only extracts codes when there's clear context like "Use code SAVE20" or "Enter FLIGHT40 at checkout"—so I wouldn't end up with a dashboard full of random capitalized words.

Next, we built a categorization system that automatically sorts offers into Flights, Food, Retail, Entertainment, and other categories. The tool extracts merchant names from sender domains, identifies discount amounts, tracks expiration dates, and calculates urgency levels so codes expiring soon appear at the top. Finally, we generated an interactive HTML dashboard with real-time search, category filters, sortable columns, and one-click code copying. The entire dashboard works offline once generated—no external dependencies, no tracking scripts, completely self-contained.

The result? A FastAPI backend with SQLite storage, a clean OAuth flow for Gmail connection, and a dashboard that turns email chaos into organized, actionable information. All running 100% locally on my machine.

This project demonstrates how AI can help you build practical, privacy-respecting tools quickly and effectively. The entire application—from Gmail API integration to the interactive dashboard—was built in a single day. No prior experience with Gmail's API was needed. Claude handled the technical implementation while I made the important decisions about architecture, privacy, and user experience.

What used to take me 10 minutes of inbox searching now takes 2 seconds. I open my dashboard, search for "Target," and instantly see all available codes. The tool has saved me dozens of hours and helped me catch deals I would have missed otherwise.

More importantly, it proves that you don't need to sacrifice privacy for convenience. Local-first AI tools are viable, powerful, and can be built in a single day with the right assistance.

**Try it yourself:** [github.com/udirno/gmail-promo-agent](https://github.com/udirno/gmail-promo-agent)

The repository includes everything you need: setup instructions, code you can audit and modify, and a quickstart guide. Build your own privacy-respecting tools and take back control of your data.
