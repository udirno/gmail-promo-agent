"""
Diagnostic tool to check what merchant names are being extracted.
Shows you the first 20 promos with their extraction details.
"""

import json
from promo_parser import extract_merchant_name

def check_merchants():
    """Load your promo data and show merchant extraction details."""
    
    try:
        with open('weekly_promo_report.json', 'r') as f:
            promos = json.load(f)
    except FileNotFoundError:
        print("❌ weekly_promo_report.json not found!")
        print("   Run 'python gmail_agent.py' first to generate data.")
        return
    
    print("=" * 80)
    print("MERCHANT NAME EXTRACTION DIAGNOSTIC")
    print("=" * 80)
    print()
    print(f"Analyzing {len(promos)} promotional offers...")
    print()
    print("Showing first 20 examples:")
    print("=" * 80)
    
    for i, promo in enumerate(promos[:20], 1):
        subject = promo.get('subject', 'No subject')
        merchant = promo.get('merchant', 'Unknown')
        code = promo.get('code', 'NO CODE')
        category = promo.get('category', 'Other')
        
        print(f"\n{i}. CODE: {code}")
        print(f"   Category: {category}")
        print(f"   Subject: {subject[:70]}{'...' if len(subject) > 70 else ''}")
        print(f"   👉 EXTRACTED MERCHANT: {merchant}")
        print(f"   -" * 40)
    
    print("\n" + "=" * 80)
    print("MERCHANT FREQUENCY")
    print("=" * 80)
    
    # Count merchant frequency
    merchant_counts = {}
    for promo in promos:
        merchant = promo.get('merchant', 'Unknown')
        merchant_counts[merchant] = merchant_counts.get(merchant, 0) + 1
    
    # Sort by frequency
    sorted_merchants = sorted(merchant_counts.items(), key=lambda x: -x[1])
    
    print("\nTop 15 merchants by number of offers:")
    for merchant, count in sorted_merchants[:15]:
        print(f"  {count:3d} offers - {merchant}")
    
    print("\n" + "=" * 80)
    print("REVIEW")
    print("=" * 80)
    print()
    print("Look at the extracted merchants above.")
    print("Are they actual company names (good) or marketing phrases (bad)?")
    print()
    print("Examples of GOOD extraction:")
    print("  ✓ Southwest Airlines")
    print("  ✓ Target")
    print("  ✓ Uber Eats")
    print()
    print("Examples of BAD extraction:")
    print("  ✗ Explore Fall Favorites")
    print("  ✗ Psst... $60")
    print("  ✗ Don't Miss Out")
    print()
    print("If you see bad extractions, share a few examples and I'll improve the logic!")
    print("=" * 80)


if __name__ == "__main__":
    check_merchants()