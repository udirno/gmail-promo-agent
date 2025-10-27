"""
Generate an interactive HTML dashboard for promo codes.
Professional, shareable, and action-oriented.
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict
import re

def parse_discount_value(discount_str: str) -> float:
    """Extract numeric value from discount string for sorting."""
    if not discount_str or discount_str == "Check email for details":
        return 0.0
    
    # Extract percentage
    pct_match = re.search(r'(\d+)%', discount_str)
    if pct_match:
        return float(pct_match.group(1))
    
    # Extract dollar amount
    dollar_match = re.search(r'\$(\d+)', discount_str)
    if dollar_match:
        return float(dollar_match.group(1)) * 2  # Weight dollars higher
    
    # BOGO or free shipping
    if 'free' in discount_str.lower() or 'bogo' in discount_str.lower():
        return 50.0
    
    return 0.0


def parse_expiration(exp_str: str) -> datetime:
    """Parse expiration string to datetime object."""
    if not exp_str:
        return datetime.max
    
    try:
        # Try common formats
        for fmt in ["%B %d, %Y", "%b %d, %Y", "%m/%d/%Y", "%m/%d/%y"]:
            try:
                return datetime.strptime(exp_str, fmt)
            except ValueError:
                continue
        
        # If all else fails, return far future
        return datetime.max
    except:
        return datetime.max


def get_urgency_level(expiration_date: datetime) -> tuple:
    """
    Determine urgency level based on expiration.
    Returns (urgency_text, urgency_class, days_left)
    """
    if expiration_date == datetime.max:
        return ("Unknown", "urgency-unknown", None)
    
    days_left = (expiration_date - datetime.now()).days
    
    if days_left < 0:
        return ("Expired", "urgency-expired", days_left)
    elif days_left == 0:
        return ("Today", "urgency-critical", 0)
    elif days_left == 1:
        return ("Tomorrow", "urgency-critical", 1)
    elif days_left <= 3:
        return (f"{days_left} days", "urgency-high", days_left)
    elif days_left <= 7:
        return (f"{days_left} days", "urgency-medium", days_left)
    else:
        return (f"{days_left} days", "urgency-low", days_left)


def enrich_promo_data(promos: List[Dict]) -> List[Dict]:
    """Add computed fields for sorting and display."""
    enriched = []
    
    for promo in promos:
        # Parse expiration
        exp_date = parse_expiration(promo.get('expiration'))
        urgency_text, urgency_class, days_left = get_urgency_level(exp_date)
        
        # Skip expired promos
        if days_left is not None and days_left < 0:
            continue
        
        # Calculate discount value for sorting
        discount_value = parse_discount_value(promo.get('discount', ''))
        
        # Get clean merchant name
        merchant = promo.get('merchant', 'Unknown Merchant')
        if not merchant or merchant == '':
            # Fallback to subject extraction
            subject = promo.get('subject', '')
            merchant = subject[:40] + '...' if len(subject) > 40 else subject
        
        enriched_promo = {
            **promo,
            'expiration_date': exp_date,
            'urgency_text': urgency_text,
            'urgency_class': urgency_class,
            'days_left': days_left if days_left is not None else 999,
            'discount_value': discount_value,
            'display_expiration': promo.get('expiration', 'No expiration'),
            'display_discount': promo.get('discount', 'See email for details'),
            'display_merchant': merchant
        }
        
        enriched.append(enriched_promo)
    
    # Sort by urgency (expiring soon first), then by discount value
    enriched.sort(key=lambda x: (x['days_left'], -x['discount_value']))
    
    return enriched


def generate_html_dashboard(promos: List[Dict], output_path: str = "promo_dashboard.html"):
    """Generate interactive HTML dashboard."""
    
    # Enrich data
    enriched_promos = enrich_promo_data(promos)
    
    # Get statistics
    total_promos = len(enriched_promos)
    expiring_soon = sum(1 for p in enriched_promos if p['days_left'] <= 7)
    categories = sorted(set(p['category'] for p in enriched_promos))
    
    # Generate timestamp
    generated_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Promo Codes Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f7fa;
            color: #2d3748;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 40px;
        }}
        
        .header h1 {{
            font-size: 32px;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        
        .header .subtitle {{
            opacity: 0.9;
            font-size: 14px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px 40px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .stat-card {{
            text-align: center;
            padding: 20px;
            background: #f7fafc;
            border-radius: 8px;
        }}
        
        .stat-number {{
            font-size: 36px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 14px;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .controls {{
            padding: 30px 40px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .search-box {{
            flex: 1;
            min-width: 250px;
        }}
        
        .search-box input {{
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }}
        
        .search-box input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .filter-group {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .filter-btn {{
            padding: 8px 16px;
            border: 2px solid #e2e8f0;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s;
        }}
        
        .filter-btn:hover {{
            border-color: #667eea;
            background: #f7fafc;
        }}
        
        .filter-btn.active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}
        
        .table-container {{
            padding: 0 40px 40px;
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }}
        
        thead {{
            background: #f7fafc;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        th {{
            padding: 16px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
            color: #4a5568;
            border-bottom: 2px solid #e2e8f0;
            cursor: pointer;
            user-select: none;
        }}
        
        th:hover {{
            background: #edf2f7;
        }}
        
        td {{
            padding: 16px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        tbody tr {{
            transition: background-color 0.2s;
        }}
        
        tbody tr:hover {{
            background: #f7fafc;
        }}
        
        .merchant-cell {{
            font-weight: 600;
            color: #2d3748;
        }}
        
        .code-cell {{
            font-family: 'Monaco', 'Courier New', monospace;
            background: #f7fafc;
            padding: 8px 12px;
            border-radius: 4px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        
        .copy-btn {{
            padding: 4px 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: background 0.3s;
        }}
        
        .copy-btn:hover {{
            background: #5a67d8;
        }}
        
        .copy-btn.copied {{
            background: #48bb78;
        }}
        
        .discount-cell {{
            color: #38a169;
            font-weight: 600;
        }}
        
        .urgency-critical {{
            color: #e53e3e;
            font-weight: 600;
        }}
        
        .urgency-high {{
            color: #ed8936;
            font-weight: 600;
        }}
        
        .urgency-medium {{
            color: #ecc94b;
            font-weight: 500;
        }}
        
        .urgency-low {{
            color: #718096;
        }}
        
        .urgency-unknown {{
            color: #a0aec0;
        }}
        
        .category-badge {{
            display: inline-block;
            padding: 4px 12px;
            background: #edf2f7;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }}
        
        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: #718096;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #718096;
            font-size: 13px;
            border-top: 1px solid #e2e8f0;
        }}
        
        @media (max-width: 768px) {{
            .header {{
                padding: 20px;
            }}
            
            .controls {{
                padding: 20px;
            }}
            
            .table-container {{
                padding: 0 20px 20px;
            }}
            
            .stats {{
                padding: 20px;
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Promo Codes Dashboard</h1>
            <div class="subtitle">Generated {generated_time}</div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{total_promos}</div>
                <div class="stat-label">Active Offers</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{expiring_soon}</div>
                <div class="stat-label">Expiring This Week</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(categories)}</div>
                <div class="stat-label">Categories</div>
            </div>
        </div>
        
        <div class="controls">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search codes, discounts, or sources...">
            </div>
            <div class="filter-group">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="expiring">Expiring Soon</button>
                {' '.join(f'<button class="filter-btn" data-filter="{cat}">{cat}</button>' for cat in categories)}
            </div>
        </div>
        
        <div class="table-container">
            <table id="promoTable">
                <thead>
                    <tr>
                        <th data-sort="merchant">Merchant</th>
                        <th data-sort="code">Promo Code</th>
                        <th data-sort="discount">Discount</th>
                        <th data-sort="expiration">Expires</th>
                        <th data-sort="category">Category</th>
                        <th data-sort="urgency">Urgency</th>
                    </tr>
                </thead>
                <tbody id="promoTableBody">
"""
    
    # Add table rows
    for promo in enriched_promos:
        merchant_display = promo['display_merchant']
        
        html_content += f"""
                    <tr data-category="{promo['category']}" data-days="{promo['days_left']}">
                        <td class="merchant-cell">{merchant_display}</td>
                        <td class="code-cell">
                            {promo['code']}
                            <button class="copy-btn" onclick="copyCode(this, '{promo['code']}')">Copy</button>
                        </td>
                        <td class="discount-cell">{promo['display_discount']}</td>
                        <td>{promo['display_expiration']}</td>
                        <td><span class="category-badge">{promo['category']}</span></td>
                        <td class="{promo['urgency_class']}">{promo['urgency_text']}</td>
                    </tr>
"""
    
    html_content += """
                </tbody>
            </table>
            <div id="noResults" class="no-results" style="display: none;">
                <p>No promo codes match your search or filter.</p>
            </div>
        </div>
        
        <div class="footer">
            Generated by Gmail Promo Agent | Last updated: """ + generated_time + """
        </div>
    </div>
    
    <script>
        // Copy code functionality
        function copyCode(button, code) {
            navigator.clipboard.writeText(code).then(() => {
                const originalText = button.textContent;
                button.textContent = 'Copied!';
                button.classList.add('copied');
                setTimeout(() => {
                    button.textContent = originalText;
                    button.classList.remove('copied');
                }, 2000);
            });
        }
        
        // Filter functionality
        const filterBtns = document.querySelectorAll('.filter-btn');
        const searchInput = document.getElementById('searchInput');
        const tableBody = document.getElementById('promoTableBody');
        const noResults = document.getElementById('noResults');
        
        let currentFilter = 'all';
        let currentSearch = '';
        
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                applyFilters();
            });
        });
        
        searchInput.addEventListener('input', (e) => {
            currentSearch = e.target.value.toLowerCase();
            applyFilters();
        });
        
        function applyFilters() {
            const rows = tableBody.querySelectorAll('tr');
            let visibleCount = 0;
            
            rows.forEach(row => {
                const category = row.dataset.category;
                const days = parseInt(row.dataset.days);
                const text = row.textContent.toLowerCase();
                
                let matchesFilter = false;
                if (currentFilter === 'all') {
                    matchesFilter = true;
                } else if (currentFilter === 'expiring') {
                    matchesFilter = days <= 7;
                } else {
                    matchesFilter = category === currentFilter;
                }
                
                const matchesSearch = !currentSearch || text.includes(currentSearch);
                
                if (matchesFilter && matchesSearch) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            noResults.style.display = visibleCount === 0 ? 'block' : 'none';
        }
        
        // Table sorting
        const headers = document.querySelectorAll('th[data-sort]');
        let sortDirection = {};
        
        headers.forEach(header => {
            sortDirection[header.dataset.sort] = 1;
            
            header.addEventListener('click', () => {
                const sortKey = header.dataset.sort;
                const rows = Array.from(tableBody.querySelectorAll('tr'));
                const columnIndex = Array.from(header.parentNode.children).indexOf(header);
                
                rows.sort((a, b) => {
                    let aVal, bVal;
                    
                    if (sortKey === 'urgency') {
                        aVal = parseInt(a.dataset.days);
                        bVal = parseInt(b.dataset.days);
                    } else {
                        const aCell = a.querySelector(`td:nth-child($${columnIndex + 1})`);
                        const bCell = b.querySelector(`td:nth-child($${columnIndex + 1})`);
                        aVal = aCell.textContent.trim().toLowerCase();
                        bVal = bCell.textContent.trim().toLowerCase();
                    }
                    
                    if (aVal < bVal) return -sortDirection[sortKey];
                    if (aVal > bVal) return sortDirection[sortKey];
                    return 0;
                });
                
                sortDirection[sortKey] *= -1;
                
                rows.forEach(row => tableBody.appendChild(row));
            });
        });
    </script>
</body>
</html>
"""
    
    # Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Interactive dashboard generated: {output_path}")
    print(f"  Active offers: {total_promos}")
    print(f"  Expiring this week: {expiring_soon}")
    print(f"\n  Open in browser: open {output_path}")
    
    return output_path


# ============================================================================
# MAIN EXECUTION BLOCK - THIS WAS MISSING IN YOUR ORIGINAL FILE!
# ============================================================================
if __name__ == "__main__":
    import sys
    import os
    
    # Default input/output paths
    input_file = "weekly_promo_report.json"
    output_file = "promo_dashboard.html"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found!")
        print(f"   Looking in: {os.getcwd()}")
        print(f"\n💡 Make sure you run gmail_agent_improved.py first to generate the JSON file.")
        sys.exit(1)
    
    # Load promo data
    try:
        print(f"📂 Loading promo data from {input_file}...")
        with open(input_file, 'r', encoding='utf-8') as f:
            promo_data = json.load(f)
        
        print(f"✓ Loaded {len(promo_data)} promo codes")
        
        # Generate dashboard
        print(f"🎨 Generating dashboard...")
        generate_html_dashboard(promo_data, output_file)
        
        print(f"\n🎉 Success! Dashboard created at: {output_file}")
        print(f"   Open it with: open {output_file}")
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {input_file}")
        print(f"   {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating dashboard: {str(e)}")
        sys.exit(1)