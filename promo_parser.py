import re
import json
from datetime import datetime
from typing import List, Dict, Optional


def extract_merchant_name(subject: str, sender: str = "") -> str:
    """
    Extract merchant/brand name from email subject or sender.
    Returns a clean, recognizable merchant name.
    Prioritizes sender domain over subject marketing copy.
    """
    
    # PRIORITY 1: Extract from sender email (most reliable)
    if sender and '@' in sender:
        # Check for name before @ (e.g., "Southwest Airlines <deals@southwest.com>")
        name_match = re.search(r'^([^<]+?)\s*<', sender)
        if name_match:
            name = name_match.group(1).strip().strip('"')
            if len(name) >= 3 and not name.lower().startswith(('no-reply', 'noreply', 'do-not-reply')):
                return name
        
        # Extract domain name
        domain_match = re.search(r'@([^.]+)\.', sender)
        if domain_match:
            domain = domain_match.group(1)
            # Skip generic domains
            generic_domains = ['gmail', 'yahoo', 'outlook', 'hotmail', 'mail', 'email', 
                             'info', 'notification', 'alerts', 'news', 'promo', 'promotions',
                             'marketing', 'offers', 'deals', 'hello', 'hi']
            
            if domain.lower() not in generic_domains:
                # Clean up common subdomains
                domain = re.sub(r'^(www|mail|email|info|promo|deals|offers)\.', '', domain, flags=re.IGNORECASE)
                # Format nicely
                return domain.replace('-', ' ').replace('_', ' ').title()
    
    # PRIORITY 2: Look for explicit brand mentions in subject
    # Pattern: "From Brand Name" or "Brand Name presents" etc.
    from_pattern = re.search(r'(?:from|by)\s+([A-Z][A-Za-z\s&\'.]{2,30})', subject)
    if from_pattern:
        brand = from_pattern.group(1).strip()
        return brand
    
    # PRIORITY 3: Pattern "Brand Name - Subject" or "Brand Name | Subject"
    separator_pattern = re.match(r'^([A-Z][A-Za-z\s&\'.]{2,30}?)\s*[-–—|:]\s*', subject)
    if separator_pattern:
        brand = separator_pattern.group(1).strip()
        # Verify it's not a marketing phrase
        marketing_starts = ['explore', 'discover', 'get', 'save', 'shop', 'buy', 'don\'t miss', 
                          'last chance', 'hurry', 'limited', 'exclusive', 'special', 'new',
                          'flash', 'deal', 'sale', 'offer', 'free', 'psst', 'hey', 'hi']
        
        if not any(brand.lower().startswith(phrase) for phrase in marketing_starts):
            return brand
    
    # PRIORITY 4: Clean subject and extract likely brand name
    # Remove common marketing noise
    noise_patterns = [
        r'[🎁🎉🎊🎈✨💝🛍️📧✈️🍕🎭🏨💰🔥⚡🌟😍🎯💎🎪🌈]+',  # Emojis
        r'(?:^|\s)(?:re|fwd?):\s*',  # RE:, FWD:
        r'(?:limited|exclusive|special|flash|final|last)\s+(?:time|offer|deal|sale|chance)',
        r'(?:don\'t|do not)\s+miss',
        r'(?:hurry|act|shop|buy|get|save|discover|explore)\s+(?:now|today|fast)?',
        r'\d+%\s+off',
        r'\$\d+\s+off',
        r'(?:today|this week|now|ends?|expires?)\s+(?:only)?',
        r'[!]{2,}',  # Multiple exclamation marks
        r'psst+[.,!]*',
        r'^(?:hey|hi|hello),?\s*',
    ]
    
    cleaned = subject
    for pattern in noise_patterns:
        cleaned = re.sub(pattern, ' ', cleaned, flags=re.IGNORECASE)
    
    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split()).strip()
    
    # Look for capitalized words at start (likely brand name)
    words = cleaned.split()
    if words:
        # Take first 1-3 capitalized words
        brand_words = []
        for word in words[:4]:
            if word and word[0].isupper() and len(word) > 1:
                # Skip common marketing words even if capitalized
                skip_words = ['Get', 'Save', 'Shop', 'Buy', 'Discover', 'Explore', 'New', 
                             'Free', 'Experience', 'Enjoy', 'Find', 'Join', 'Start', 'Try',
                             'Your', 'The', 'A', 'An']
                if word not in skip_words:
                    brand_words.append(word)
                    if len(brand_words) == 3 or len(' '.join(brand_words)) > 25:
                        break
            else:
                break
        
        if brand_words:
            brand = ' '.join(brand_words)
            if len(brand) >= 3:
                return brand
    
    # FALLBACK: Use first 40 chars of cleaned subject
    if len(cleaned) > 3:
        return cleaned[:40] + ('...' if len(cleaned) > 40 else '')
    
    # ULTIMATE FALLBACK
    return "Unknown Merchant"



def extract_promos(text: str, subject: str = "", sender: str = "") -> List[Dict]:
    """
    Extract promo codes and discounts from email text.
    Conservative approach - only extract codes with clear context.
    """
    promos = []
    
    # STRICT promo code patterns - must have context indicating it's actually a code
    code_patterns = [
        # Explicit "code" or "coupon" mentions
        r"(?:promo\s*code|promocode|promo|code|coupon|voucher)[:\s]+([A-Z0-9]{4,20})",
        r"(?:use|enter|apply)\s+(?:code|promo)?\s*:?\s*([A-Z0-9]{4,20})\b",
        
        # "at checkout" context
        r"\b([A-Z0-9]{4,20})\s+at\s+checkout",
        r"checkout\s+(?:with|using)\s+(?:code\s+)?([A-Z0-9]{4,20})",
        
        # Clear discount context - code near percentage/dollar amount
        r"\b([A-Z][A-Z0-9]{3,15})\s+(?:for|to\s+(?:get|save|receive))\s+(?:\d+%|\$\d+)",
        r"(?:save|get)\s+(?:\d+%|\$\d+)\s+(?:with|using)\s+(?:code\s+)?([A-Z0-9]{4,20})",
        
        # Format: CODE: XXXXX or Code = XXXXX
        r"code\s*[=:]\s*([A-Z0-9]{4,20})",
    ]
    
    found_codes = set()
    for pattern in code_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            code = match.upper() if isinstance(match, str) else match[0].upper()
            
            # Validate it looks like a real promo code
            if _is_valid_promo_code(code):
                found_codes.add(code)
    
    # Enhanced discount extraction - multiple formats
    discount_patterns = [
        r"(\d{1,3}%\s*(?:off|discount|savings?))",  # 20% off
        r"(\$\d{1,4}\s*(?:off|discount))",  # $50 off
        r"(save\s+\d{1,3}%)",  # save 20%
        r"(save\s+\$\d{1,4})",  # save $50
        r"(buy\s+\d+\s+get\s+\d+\s+free)",  # BOGO
        r"(free\s+shipping)",  # free shipping
        r"(up to \d{1,3}% off)",  # up to 50% off
    ]
    
    discounts = []
    for pattern in discount_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        discounts.extend([m if isinstance(m, str) else m[0] for m in matches])
    
    # Extract expiration dates
    expiry = extract_expiration_date(text)
    
    # Extract merchant name
    merchant = extract_merchant_name(subject, sender)
    
    # Create promo entries
    if found_codes:
        for code in found_codes:
            promo = {
                "code": code,
                "discount": discounts[0] if discounts else "Check email for details",
                "expiration": expiry,
                "merchant": merchant,
                "raw": text[:300],
                "subject": subject[:100]
            }
            promos.append(promo)
    elif discounts:
        # Discount found but no specific code - still useful!
        promo = {
            "code": "NO CODE NEEDED",
            "discount": ", ".join(discounts[:2]),
            "expiration": expiry,
            "merchant": merchant,
            "raw": text[:300],
            "subject": subject[:100]
        }
        promos.append(promo)
    
    return promos


def _is_valid_promo_code(code: str) -> bool:
    """
    Validate that a string actually looks like a promo code.
    Real promo codes have specific characteristics.
    """
    # Length check
    if len(code) < 4 or len(code) > 20:
        return False
    
    # Must have at least one number OR be a recognizable discount pattern
    has_number = any(c.isdigit() for c in code)
    discount_patterns = ['SAVE', 'OFF', 'DEAL', 'SALE', 'PROMO', 'WELCOME', 
                        'GET', 'FREE', 'BOGO', 'SHIP']
    has_discount_word = any(pattern in code for pattern in discount_patterns)
    
    if not (has_number or has_discount_word):
        return False
    
    # Common false positives - generic words
    false_positives = {
        # Generic words
        "EMAIL", "HTTPS", "HTTP", "HTML", "GMAIL", "INBOX", 
        "SUBJECT", "FROM", "REPLY", "UNSUBSCRIBE", "CLICK",
        "IMAGE", "LINK", "BODY", "HEADER", "FOOTER", "STYLE",
        
        # Common content words that get mis-identified
        "LIVE", "READY", "STAGE", "WORK", "SKILLS", "INSIGHTS",
        "CREDIT", "AVAILABLE", "INTENDED", "REIMBURSEMENT", "RESERVE",
        "MONTHS", "CUSTOMERSERVICE", "QUESTION", "PREDILECTION",
        "AGENTFORCE", "RECOMMENDATIONS", "TAILORED",
        
        # More generic business words
        "CONTACT", "SUPPORT", "HELP", "INFO", "INFORMATION",
        "SERVICE", "CUSTOMER", "ACCOUNT", "LOGIN", "PASSWORD",
        "BUSINESS", "COMPANY", "TEAM", "MEMBER", "USER",
        "UPDATE", "NOTICE", "ALERT", "REMINDER", "MESSAGE",
    }
    
    if code.upper() in false_positives:
        return False
    
    # All numbers (usually order IDs, not promo codes)
    if code.isdigit():
        return False
    
    # All letters with no structure (probably just a word from content)
    if code.isalpha() and not has_discount_word:
        return False
    
    # Good patterns: mix of letters and numbers
    # Examples: SAVE20, WELCOME50, ABC123, FLIGHT40
    if has_number and len(code) >= 5:
        return True
    
    # Has discount-related word
    if has_discount_word:
        return True
    
    return False
    
    return promos


def extract_expiration_date(text: str) -> Optional[str]:
    """
    Extract expiration date from email text.
    Returns formatted date string or None.
    """
    # Common date patterns
    patterns = [
        r"expir(?:es|ing|ation)[:\s]*([A-Za-z]+\s+\d{1,2},?\s+\d{4})",  # expires January 15, 2025
        r"valid\s+(?:through|until|till)[:\s]*([A-Za-z]+\s+\d{1,2},?\s+\d{4})",
        r"ends?[:\s]*([A-Za-z]+\s+\d{1,2},?\s+\d{4})",
        r"(\d{1,2}/\d{1,2}/\d{2,4})",  # 12/31/2025
        r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None


def _is_false_positive(code: str) -> bool:
    """
    Filter out common false positives that aren't promo codes.
    """
    false_positives = {
        "EMAIL", "HTTPS", "HTTP", "HTML", "GMAIL", "INBOX", 
        "SUBJECT", "FROM", "REPLY", "UNSUBSCRIBE", "CLICK",
        "IMAGE", "LINK", "BODY", "HEADER", "FOOTER", "STYLE"
    }
    
    # Too short or too long
    if len(code) < 4 or len(code) > 15:
        return True
    
    # Known false positive
    if code.upper() in false_positives:
        return True
    
    # All numbers (likely not a promo code)
    if code.isdigit():
        return True
    
    return False


def categorize_promo(promo: Dict, categories_path: str = "categories.json") -> Dict:
    """
    Categorize promo based on keywords in email text and subject.
    Enhanced with scoring system for better accuracy.
    """
    with open(categories_path, "r") as f:
        cats = json.load(f)
    
    # Combine raw text and subject for better context
    text = (promo.get("raw", "") + " " + promo.get("subject", "")).lower()
    
    # Score each category
    category_scores = {}
    for cat, keywords in cats.items():
        if cat == "Other":
            continue
        score = sum(1 for keyword in keywords if keyword.lower() in text)
        if score > 0:
            category_scores[cat] = score
    
    # Assign to highest scoring category
    if category_scores:
        promo["category"] = max(category_scores, key=category_scores.get)
    else:
        promo["category"] = "Other"
    
    return promo


def deduplicate_promos(promos: List[Dict]) -> List[Dict]:
    """
    Remove duplicate promo codes, keeping the one with most information.
    """
    unique_promos = {}
    
    for promo in promos:
        code = promo["code"]
        
        if code not in unique_promos:
            unique_promos[code] = promo
        else:
            # Keep the one with more discount information
            existing = unique_promos[code]
            if len(promo.get("discount", "")) > len(existing.get("discount", "")):
                unique_promos[code] = promo
    
    return list(unique_promos.values())