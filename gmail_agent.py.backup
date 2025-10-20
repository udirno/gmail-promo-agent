from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email import message_from_bytes
from bs4 import BeautifulSoup
from promo_parser import extract_promos, categorize_promo, deduplicate_promos
from jinja2 import Template
import json
import yaml
import os
from typing import List, Dict
from datetime import datetime
from dashboard_generator import generate_html_dashboard

# Gmail API scope - read only
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def load_config():
    """Load configuration from YAML file."""
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def get_gmail_service(creds_path: str):
    """
    Initialize Gmail API service with proper OAuth flow.
    Handles both first-time setup and subsequent runs.
    """
    creds = None
    token_path = 'token.json'
    
    # Check if we have a saved token from previous authentication
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception as e:
            print(f"⚠️  Error loading saved token: {e}")
            print("   Will re-authenticate...")
            creds = None
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Token expired but can be refreshed
            try:
                print("🔄 Refreshing expired token...")
                creds.refresh(Request())
            except Exception as e:
                print(f"⚠️  Could not refresh token: {e}")
                creds = None
        
        if not creds:
            # Need fresh authentication
            if not os.path.exists(creds_path):
                raise FileNotFoundError(
                    f"\n❌ Credentials file not found: {creds_path}\n\n"
                    f"Please download OAuth credentials from Google Cloud Console:\n"
                    f"1. Go to https://console.cloud.google.com\n"
                    f"2. Navigate to APIs & Services > Credentials\n"
                    f"3. Download your OAuth 2.0 Client ID as 'credentials.json'\n"
                    f"4. Place it in: {os.path.abspath(creds_path)}\n"
                )
            
            print("\n🔐 First time setup - Opening browser for authentication...")
            print("   1. Sign in to your Gmail account")
            print("   2. Grant read-only access")
            print("   3. Return here after authorization\n")
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                raise Exception(
                    f"\n❌ Authentication failed: {e}\n\n"
                    f"Make sure credentials.json is a valid OAuth client configuration.\n"
                    f"It should contain 'installed' or 'web' credentials, not a service account.\n"
                )
        
        # Save credentials for future runs
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        print(f"✓ Authentication successful! Token saved to {token_path}")
    
    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except Exception as e:
        print(f"❌ Error building Gmail service: {e}")
        raise


def fetch_promo_emails(service, query: str, max_results: int = 50) -> List[Dict]:
    """
    Fetch promotional emails from Gmail.
    Enhanced with error handling and pagination support.
    """
    try:
        messages = []
        page_token = None
        
        while len(messages) < max_results:
            results = service.users().messages().list(
                userId="me", 
                q=query,
                maxResults=min(50, max_results - len(messages)),
                pageToken=page_token
            ).execute()
            
            batch = results.get("messages", [])
            if not batch:
                break
            
            messages.extend(batch)
            page_token = results.get("nextPageToken")
            
            if not page_token:
                break
        
        print(f"✓ Fetched {len(messages)} promotional emails")
        
        # Get full message details
        full_messages = []
        for i, msg in enumerate(messages, 1):
            try:
                if i % 10 == 0:
                    print(f"  Processing email {i}/{len(messages)}...")
                
                full_msg = service.users().messages().get(
                    userId="me", 
                    id=msg["id"], 
                    format="full"
                ).execute()
                full_messages.append(full_msg)
            except Exception as e:
                print(f"⚠️  Error fetching message {msg['id']}: {e}")
                continue
        
        return full_messages
    
    except Exception as e:
        print(f"❌ Error fetching emails: {e}")
        return []


def parse_email(msg: Dict) -> tuple[str, str, str]:
    """
    Parse email to extract text content, subject, and sender.
    Enhanced to handle both HTML and plain text emails.
    Returns: (body_text, subject, sender)
    """
    # Extract headers
    headers = msg["payload"].get("headers", [])
    subject = ""
    sender = ""
    
    for header in headers:
        header_name = header["name"].lower()
        if header_name == "subject":
            subject = header["value"]
        elif header_name == "from":
            sender = header["value"]
    
    # Extract body
    payload = msg["payload"]
    body_text = ""
    
    # Handle multipart emails
    if "parts" in payload:
        for part in payload["parts"]:
            body_text += _extract_part_text(part)
    else:
        # Single part email
        body_text = _extract_part_text(payload)
    
    return body_text, subject, sender


def _extract_part_text(part: Dict) -> str:
    """
    Extract text from email part, handling both plain text and HTML.
    """
    mime_type = part.get("mimeType", "")
    body = part.get("body", {})
    data = body.get("data", "")
    
    if not data:
        # Check nested parts (for multipart/alternative)
        if "parts" in part:
            text = ""
            for nested_part in part["parts"]:
                text += _extract_part_text(nested_part)
            return text
        return ""
    
    try:
        decoded = base64.urlsafe_b64decode(data.encode("UTF-8")).decode("UTF-8", errors="ignore")
        
        # If HTML, extract text content
        if "html" in mime_type.lower():
            soup = BeautifulSoup(decoded, "html.parser")
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator=" ", strip=True)
            return text
        else:
            return decoded
    
    except Exception as e:
        print(f"⚠️  Error decoding email part: {e}")
        return ""


def generate_report(promos: List[Dict], config: Dict) -> None:
    """
    Generate a formatted Markdown report from categorized promos.
    Enhanced with better formatting and statistics.
    """
    # Group by category
    categorized = {}
    for promo in promos:
        cat = promo.get("category", "Other")
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append(promo)
    
    # Sort categories by number of promos
    categorized = dict(sorted(categorized.items(), key=lambda x: len(x[1]), reverse=True))
    
    # Load template
    with open(config["report"]["template_path"], "r") as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # Prepare context with statistics
    context = {
        "categorized_promos": categorized,
        "total_promos": len(promos),
        "total_categories": len(categorized),
        "generated_date": datetime.now().strftime("%B %d, %Y at %I:%M %p")
    }
    
    # Render report
    report = template.render(**context)
    
    # Write to file
    output_path = config["report"]["output_path"]
    with open(output_path, "w") as out:
        out.write(report)
    
    print(f"\n✓ Report generated: {output_path}")
    print(f"  Total promos: {len(promos)}")
    print(f"  Categories: {', '.join(categorized.keys())}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("Gmail Promo Email Agent - Weekly Summary")
    print("=" * 60)
    
    try:
        # Load configuration
        config = load_config()
        
        # Initialize Gmail service
        print("\n[1/5] Connecting to Gmail...")
        service = get_gmail_service(config["gmail"]["credentials_path"])
        print("✓ Connected to Gmail API")
        
        # Fetch promotional emails
        print("\n[2/5] Fetching promotional emails...")
        emails = fetch_promo_emails(service, config["gmail"]["query"])
        
        if not emails:
            print("\n⚠️  No promotional emails found.")
            print("   Try adjusting the query in config.yaml")
            print("   Current query:", config["gmail"]["query"])
            return
        
        # Extract promos from emails
        print("\n[3/5] Extracting promo codes and discounts...")
        all_promos = []
        
        for email in emails:
            body_text, subject, sender = parse_email(email)
            promos = extract_promos(body_text, subject, sender)
            
            # Categorize each promo
            categorized = [
                categorize_promo(p, config["report"]["categories_path"]) 
                for p in promos
            ]
            all_promos.extend(categorized)
        
        print(f"✓ Found {len(all_promos)} promotional offers")
        
        # Deduplicate
        print("\n[4/5] Removing duplicates...")
        unique_promos = deduplicate_promos(all_promos)
        print(f"✓ {len(unique_promos)} unique offers after deduplication")
        
        # Generate reports
        print("\n[5/5] Generating reports...")
        
        # Save JSON backup first
        json_path = config["report"]["output_path"].replace(".md", ".json")
        with open(json_path, "w") as f:
            json.dump(unique_promos, f, indent=2)
        print(f"✓ JSON data saved: {json_path}")
        
        # Generate HTML dashboard (primary output)
        dashboard_path = "promo_dashboard.html"
        generate_html_dashboard(unique_promos, dashboard_path)
        
        # Also generate markdown for compatibility
        generate_report(unique_promos, config)
        
        print("\n" + "=" * 60)
        print("Summary complete!")
        print("=" * 60)
        print(f"\n  View your dashboard: open {dashboard_path}")
        print(f"  Or open directly in browser")
        print(f"\n  Total active offers: {len(unique_promos)}")
        
        # Count expiring soon
        from dashboard_generator import parse_expiration, get_urgency_level
        expiring_soon = sum(1 for p in unique_promos 
                          if get_urgency_level(parse_expiration(p.get('expiration')))[2] is not None 
                          and get_urgency_level(parse_expiration(p.get('expiration')))[2] <= 7)
        if expiring_soon > 0:
            print(f"  ⚠️  {expiring_soon} offer(s) expiring this week - check urgency column!")
        
        print("\n" + "=" * 60)
        
    except FileNotFoundError as e:
        print(f"\n{e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()