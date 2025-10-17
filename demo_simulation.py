"""
Demo simulation of the Gmail Promo Agent with sample email data.
Run this to see the agent in action without needing Gmail API credentials.
Now generates the interactive HTML dashboard!
"""

from promo_parser import extract_promos, categorize_promo, deduplicate_promos
from dashboard_generator import generate_html_dashboard
from datetime import datetime
import json

# Sample promotional email texts
SAMPLE_EMAILS = [
    {
        "subject": "Southwest Airlines - Flash Sale: 40% Off All Flights This Weekend!",
        "sender": "deals@southwest.com",
        "body": """
        Don't miss out! Book your dream vacation now.
        
        Use promo code FLIGHT40 at checkout to save 40% off on all domestic 
        and international flights. This incredible offer expires October 20, 2025.
        
        Valid for travel through December 2025.
        """
    },
    {
        "subject": "Papa John's - Buy One Get One Free",
        "sender": "promotions@papajohns.com",
        "body": """
        Hi there!
        
        We're celebrating our anniversary with an amazing deal:
        Buy 1 large pizza, get 1 FREE!
        
        Order online with code BOGO2024 
        Offer valid until October 25, 2025
        
        Free delivery on orders over $20
        """
    },
    {
        "subject": "Nordstrom - Your exclusive 25% discount awaits",
        "sender": "offers@nordstrom.com",
        "body": """
        Dear Valued Customer,
        
        As a thank you for being part of our community, here's an exclusive 
        discount just for you: Save 25% on your entire purchase at our store.
        
        Use code: SAVE25NOW
        Shop clothing, accessories, home goods and more.
        
        Ends: November 1, 2025
        """
    },
    {
        "subject": "Ticketmaster - Last Chance: Concert Tickets $50 Off",
        "sender": "events@ticketmaster.com",
        "body": """
        The show is almost here! 
        
        Get $50 off tickets to the Summer Music Festival using code MUSIC50
        
        Limited time offer - valid through October 18, 2025
        All genres, all venues. Don't miss this amazing event!
        """
    },
    {
        "subject": "Target - Free Shipping + 15% Off Your Order",
        "sender": "promotions@target.com",
        "body": """
        Hey Friend!
        
        This week only: Enjoy FREE SHIPPING on all orders plus an extra 15% off
        when you spend $75 or more.
        
        Code: SHIP15FREE
        
        Expiration: October 22, 2025
        
        Happy shopping!
        """
    },
    {
        "subject": "Expedia - Cyber Monday Travel Deals - Up to 60% Savings",
        "sender": "deals@expedia.com",
        "body": """
        HUGE SAVINGS ALERT!
        
        We've slashed prices on thousands of flights and hotel packages.
        Save up to 60% off regular prices on select routes.
        
        Use promo code CYBER60 for maximum savings
        Book by October 30, 2025
        Travel dates: Now through March 2026
        
        Book your airline tickets now!
        """
    },
    {
        "subject": "DoorDash - 50% Off All Menu Items - Limited Time!",
        "sender": "offers@doordash.com",
        "body": """
        You're going to love this...
        
        For the next 48 hours, get 50% OFF everything on our menu!
        Use the code at checkout: FEAST50
        
        Valid on all restaurant delivery orders
        Hurry - expires October 19, 2025
        """
    },
    {
        "subject": "Best Buy - Special Offer Inside - No Code Needed!",
        "sender": "deals@bestbuy.com",
        "body": """
        Surprise! We're giving you 20% off automatically.
        
        No coupon code needed - discount applied at checkout
        Shop now and save on our entire collection
        
        This offer ends October 24, 2025
        """
    }
]

def simulate_agent():
    """Simulate the promo agent processing sample emails."""
    
    print("=" * 70)
    print("GMAIL PROMO AGENT - DEMO SIMULATION")
    print("=" * 70)
    print()
    
    print(f"Processing {len(SAMPLE_EMAILS)} sample promotional emails...")
    print()
    
    all_promos = []
    
    # Process each sample email
    for i, email in enumerate(SAMPLE_EMAILS, 1):
        print(f"[{i}/{len(SAMPLE_EMAILS)}] Processing: {email['subject'][:50]}...")
        
        # Extract promos
        promos = extract_promos(email['body'], email['subject'], email.get('sender', ''))
        
        # Categorize
        categorized = [categorize_promo(p) for p in promos]
        all_promos.extend(categorized)
    
    print()
    print(f"✓ Extracted {len(all_promos)} promotional offers")
    
    # Deduplicate
    unique_promos = deduplicate_promos(all_promos)
    print(f"✓ After deduplication: {len(unique_promos)} unique offers")
    print()
    
    # Group by category for display
    categorized = {}
    for promo in unique_promos:
        cat = promo.get("category", "Other")
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append(promo)
    
    # Sort by number of promos
    categorized = dict(sorted(categorized.items(), key=lambda x: len(x[1]), reverse=True))
    
    # Show breakdown
    print("CATEGORY BREAKDOWN:")
    print("-" * 70)
    for category, promos in categorized.items():
        print(f"  {category}: {len(promos)} offer(s)")
    print()
    
    # Generate HTML dashboard
    print("Generating interactive dashboard...")
    dashboard_path = generate_html_dashboard(unique_promos, "demo_promo_dashboard.html")
    
    # Save JSON backup
    with open("demo_promos.json", "w") as f:
        json.dump(unique_promos, f, indent=2)
    
    print()
    print("=" * 70)
    print("DEMO COMPLETE!")
    print("=" * 70)
    print(f"✓ Interactive Dashboard: {dashboard_path}")
    print(f"✓ JSON Data: demo_promos.json")
    print()
    print("Next steps:")
    print(f"  1. Open dashboard: open {dashboard_path}")
    print("  2. Try the search bar")
    print("  3. Click category filters")
    print("  4. Click 'Copy' buttons to copy codes")
    print("  5. Sort by clicking column headers")
    print("=" * 70)
    
    return unique_promos


if __name__ == "__main__":
    promos = simulate_agent()