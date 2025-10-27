"""
Gmail Promo Agent - Improved Version with Structured Logging

Changes made:
1. Added structured logging with different levels (INFO, WARNING, ERROR)
2. Added comprehensive error handling for missing files and credentials
3. Added setup validation to check prerequisites before running
4. Added progress indicators for long-running operations
5. Added detailed error messages with actionable guidance
6. Added file existence checks before operations
7. Improved OAuth flow error handling
8. Added virtual environment detection and warning
"""

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email import message_from_bytes
import json
import yaml
import os
import sys
import logging
from datetime import datetime
from typing import List, Dict, Optional

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class SetupError(Exception):
    """Custom exception for setup-related errors"""
    pass

class ConfigurationError(Exception):
    """Custom exception for configuration-related errors"""
    pass


def check_virtual_environment():
    """
    Check if running in a virtual environment and warn if not.
    
    Change: Added virtual environment detection
    Why: Modern Python requires venv for pip installs
    """
    in_venv = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    
    if not in_venv:
        logger.warning("⚠️  Not running in a virtual environment")
        logger.warning("   Consider creating one: python3 -m venv venv")
        logger.warning("   Then activate: source venv/bin/activate")
        logger.warning("")


def validate_setup():
    """
    Validate that all required files and dependencies are present.
    
    Change: Added comprehensive setup validation
    Why: Prevents cryptic errors by checking prerequisites upfront
    Returns: List of setup issues found
    """
    logger.info("🔍 Validating setup...")
    issues = []
    
    # Check for required files
    required_files = {
        'config.yaml': 'Configuration file',
        'categories.json': 'Category definitions',
        'promo_parser.py': 'Promo parser module'
    }
    
    for filename, description in required_files.items():
        if not os.path.exists(filename):
            issues.append(f"Missing {description}: {filename}")
            logger.error(f"❌ {description} not found: {filename}")
        else:
            logger.info(f"✓ Found {description}")
    
    # Check for credentials (warn but don't fail)
    if not os.path.exists('credentials.json') and not os.path.exists('token.json'):
        logger.warning("⚠️  No OAuth credentials found")
        logger.warning("   You'll need to set up Google Cloud credentials:")
        logger.warning("   1. Go to https://console.cloud.google.com")
        logger.warning("   2. Create OAuth 2.0 credentials")
        logger.warning("   3. Download as credentials.json")
        logger.warning("")
        # Don't add to issues - we'll handle OAuth flow separately
    
    # Check for required Python modules
    required_modules = [
        ('googleapiclient', 'google-api-python-client'),
        ('google.oauth2', 'google-auth'),
        ('yaml', 'PyYAML')
    ]
    
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
            logger.info(f"✓ Found module: {package_name}")
        except ImportError:
            issues.append(f"Missing Python package: {package_name}")
            logger.error(f"❌ Module not found: {package_name}")
            logger.error(f"   Install with: pip install {package_name}")
    
    if issues:
        logger.error(f"\n❌ Setup validation failed with {len(issues)} issue(s)")
        return issues
    
    logger.info("✅ Setup validation passed\n")
    return []


def load_config() -> Dict:
    """
    Load configuration from YAML file with error handling.
    
    Change: Added error handling and validation
    Why: Provides clear error message if config is missing or invalid
    """
    try:
        logger.info("📄 Loading configuration...")
        
        if not os.path.exists('config.yaml'):
            raise ConfigurationError(
                "config.yaml not found. Create it from config.yaml.example or use the provided template."
            )
        
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        # Validate required config sections
        required_sections = ['gmail', 'report']
        for section in required_sections:
            if section not in config:
                raise ConfigurationError(f"Missing required section in config.yaml: {section}")
        
        logger.info(f"✓ Configuration loaded successfully")
        logger.info(f"  Query: {config['gmail']['query']}")
        logger.info(f"  Output: {config['report']['output_path']}\n")
        
        return config
        
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Invalid YAML in config.yaml: {e}")
    except Exception as e:
        raise ConfigurationError(f"Error loading configuration: {e}")


def get_gmail_service(creds_path: str):
    """
    Initialize Gmail API service with proper OAuth flow.
    
    Change: Added comprehensive error handling and OAuth flow
    Why: Original version crashed on missing credentials with no guidance
    """
    logger.info("🔐 Authenticating with Gmail...")
    creds = None
    token_path = 'token.json'
    
    # Check if we have a saved token
    if os.path.exists(token_path):
        try:
            logger.info("  Found existing token, validating...")
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            logger.info("  ✓ Token is valid")
        except Exception as e:
            logger.warning(f"  ⚠️  Token validation failed: {e}")
            creds = None
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("  Token expired, refreshing...")
            try:
                creds.refresh(Request())
                logger.info("  ✓ Token refreshed successfully")
            except Exception as e:
                logger.error(f"  ❌ Token refresh failed: {e}")
                creds = None
        
        if not creds:
            # Need fresh authentication
            if not os.path.exists(creds_path):
                raise SetupError(
                    f"\n❌ OAuth credentials not found: {creds_path}\n\n"
                    f"Setup required:\n"
                    f"1. Go to https://console.cloud.google.com\n"
                    f"2. Create a new project (or select existing)\n"
                    f"3. Enable Gmail API\n"
                    f"4. Create OAuth 2.0 credentials (Desktop app)\n"
                    f"5. Download credentials as: {os.path.abspath(creds_path)}\n\n"
                    f"See docs/setup/quickstart.md for detailed instructions.\n"
                )
            
            logger.info("\n🌐 Opening browser for OAuth authorization...")
            logger.info("  1. Sign in to your Gmail account")
            logger.info("  2. Grant read-only access to Gmail")
            logger.info("  3. Return here after authorization\n")
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=0)
                logger.info("✅ Authorization successful!")
            except Exception as e:
                raise SetupError(
                    f"\n❌ OAuth authorization failed: {e}\n\n"
                    f"Common issues:\n"
                    f"- credentials.json is not a valid OAuth client configuration\n"
                    f"- You need 'Desktop app' credentials, not 'Service account'\n"
                    f"- You haven't added yourself as a test user in Google Cloud Console\n"
                )
        
        # Save credentials for future runs
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        logger.info(f"✓ Credentials saved to {token_path}\n")
    
    try:
        service = build("gmail", "v1", credentials=creds)
        logger.info("✅ Gmail API service initialized\n")
        return service
    except Exception as e:
        raise SetupError(f"Failed to build Gmail service: {e}")


def fetch_promo_emails(service, query: str, max_results: int = 50) -> List[Dict]:
    """
    Fetch promotional emails from Gmail with progress tracking.
    
    Change: Added progress indicators and error handling
    Why: Users need feedback during long-running operations
    """
    logger.info(f"📧 Fetching promotional emails...")
    logger.info(f"  Query: {query}")
    
    try:
        # Get message IDs
        results = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
        messages = results.get("messages", [])
        
        if not messages:
            logger.warning("⚠️  No promotional emails found matching query")
            logger.warning("  Try adjusting the query in config.yaml")
            return []
        
        logger.info(f"  Found {len(messages)} emails, fetching details...")
        
        # Fetch full message details with progress
        full_messages = []
        for i, msg in enumerate(messages, 1):
            if i % 10 == 0:
                logger.info(f"  Progress: {i}/{len(messages)} emails fetched...")
            
            try:
                full_msg = service.users().messages().get(
                    userId="me", 
                    id=msg["id"], 
                    format="full"
                ).execute()
                full_messages.append(full_msg)
            except Exception as e:
                logger.warning(f"  ⚠️  Failed to fetch email {msg['id']}: {e}")
                continue
        
        logger.info(f"✅ Successfully fetched {len(full_messages)} emails\n")
        return full_messages
        
    except Exception as e:
        logger.error(f"❌ Error fetching emails: {e}")
        raise


def parse_email(msg: Dict) -> tuple[str, str, str]:
    """
    Parse email to extract text content, subject, and sender.
    
    Change: Now returns (text, subject, sender) tuple
    Why: Need subject and sender for merchant extraction
    
    Returns:
        Tuple of (body_text, subject, sender)
    """
    try:
        # Extract headers first
        headers = msg.get("payload", {}).get("headers", [])
        subject = ""
        sender = ""
        
        for header in headers:
            name = header.get("name", "").lower()
            if name == "subject":
                subject = header.get("value", "")
            elif name == "from":
                sender = header.get("value", "")
        
        # Extract body text
        payload = msg["payload"]
        parts = payload.get("parts", [])
        body_text = ""
        
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data")
                if data:
                    text = base64.urlsafe_b64decode(data.encode("UTF-8")).decode("UTF-8")
                    body_text = text
                    break
        
        # If no text/plain part found, try the main body
        if not body_text and "body" in payload and "data" in payload["body"]:
            data = payload["body"]["data"]
            body_text = base64.urlsafe_b64decode(data.encode("UTF-8")).decode("UTF-8")
        
        return body_text, subject, sender
        
    except Exception as e:
        logger.warning(f"  ⚠️  Error parsing email: {e}")
        return "", "", ""


def extract_promos_from_emails(emails: List[Dict], config: Dict) -> List[Dict]:
    """
    Extract promo codes from emails with progress tracking.
    
    Change: New function to handle extraction with logging
    Why: Separates concerns and adds progress feedback
    """
    logger.info(f"🔍 Extracting promo codes...")
    
    # Import here to handle potential import errors
    try:
        from promo_parser import extract_promos, categorize_promo
    except ImportError as e:
        raise SetupError(f"Failed to import promo_parser: {e}")
    
    all_promos = []
    emails_with_promos = 0
    
    for i, email in enumerate(emails, 1):
        if i % 10 == 0:
            logger.info(f"  Progress: {i}/{len(emails)} emails processed...")
        
        # Parse email to get text, subject, and sender
        text, subject, sender = parse_email(email)
        if not text:
            continue
        
        # Extract promos - pass subject and sender for better merchant extraction
        try:
            # Try the full version with 3 arguments
            promos = extract_promos(text, subject, sender)
        except TypeError:
            # Fallback to simple version with 1 argument
            try:
                promos = extract_promos(text)
                # Add subject and sender to each promo manually
                for promo in promos:
                    if "subject" not in promo or not promo["subject"]:
                        promo["subject"] = subject
                    if "merchant" not in promo or not promo["merchant"]:
                        # Extract merchant from sender or subject
                        from promo_parser import extract_merchant_name
                        promo["merchant"] = extract_merchant_name(subject, sender)
            except Exception as e:
                logger.warning(f"  ⚠️  Error extracting from email {i}: {e}")
                continue
        
        if promos:
            emails_with_promos += 1
            # Categorize each promo
            try:
                categories_path = config.get("report", {}).get("categories_path", "categories.json")
                categorized = [categorize_promo(p, categories_path) for p in promos]
                all_promos.extend(categorized)
            except Exception as e:
                logger.warning(f"  ⚠️  Error categorizing promos from email {i}: {e}")
                all_promos.extend(promos)
    
    logger.info(f"✅ Extracted {len(all_promos)} promo codes from {emails_with_promos} emails\n")
    return all_promos


def save_results(promos: List[Dict], output_path: str):
    """
    Save extracted promos to JSON file.
    
    Change: Added error handling and validation
    Why: File operations can fail for various reasons
    """
    logger.info(f"💾 Saving results...")
    
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"  Created output directory: {output_dir}")
        
        # Force JSON format if output is .md (config inconsistency)
        if output_path.endswith('.md'):
            json_path = output_path.replace('.md', '.json')
            logger.warning(f"  ⚠️  Config specifies .md but saving as JSON: {json_path}")
            output_path = json_path
        
        with open(output_path, "w") as out:
            json.dump(promos, out, indent=2)
        
        file_size = os.path.getsize(output_path)
        logger.info(f"✅ Results saved to: {output_path}")
        logger.info(f"  File size: {file_size:,} bytes")
        logger.info(f"  Total promos: {len(promos)}\n")
        
    except Exception as e:
        logger.error(f"❌ Error saving results: {e}")
        raise


def print_summary(promos: List[Dict]):
    """
    Print a summary of extracted promos.
    
    Change: New function for user-friendly output
    Why: Users want to see what was found without opening files
    """
    logger.info("=" * 60)
    logger.info("📊 SUMMARY")
    logger.info("=" * 60)
    
    if not promos:
        logger.info("No promo codes found.")
        return
    
    # Group by category
    categories = {}
    for promo in promos:
        cat = promo.get("category", "Other")
        categories[cat] = categories.get(cat, 0) + 1
    
    logger.info(f"\nTotal promo codes: {len(promos)}")
    logger.info("\nBy category:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        logger.info(f"  {cat:20s}: {count:3d} codes")
    
    # Show sample promos
    logger.info("\nSample codes:")
    for i, promo in enumerate(promos[:5], 1):
        code = promo.get("code", "N/A")
        discount = promo.get("discount", "N/A")
        category = promo.get("category", "N/A")
        logger.info(f"  {i}. {code:15s} - {discount:20s} [{category}]")
    
    if len(promos) > 5:
        logger.info(f"  ... and {len(promos) - 5} more")
    
    logger.info("=" * 60 + "\n")


def main():
    """
    Main execution function with comprehensive error handling.
    
    Change: Restructured with proper error handling and logging
    Why: Provides clear feedback and actionable error messages
    """
    start_time = datetime.now()
    
    logger.info("=" * 60)
    logger.info("📬 Gmail Promo Email Agent")
    logger.info("=" * 60)
    logger.info(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Check virtual environment
        check_virtual_environment()
        
        # Validate setup
        issues = validate_setup()
        if issues:
            logger.error("\nSetup validation failed. Please fix the following issues:")
            for issue in issues:
                logger.error(f"  • {issue}")
            logger.error("\nRefer to docs/setup/quickstart.md for setup instructions.")
            sys.exit(1)
        
        # Load configuration
        config = load_config()
        
        # Initialize Gmail service
        service = get_gmail_service(config["gmail"]["credentials_path"])
        
        # Fetch emails
        emails = fetch_promo_emails(service, config["gmail"]["query"])
        
        if not emails:
            logger.warning("No emails to process. Exiting.")
            return
        
        # Extract promos
        promos = extract_promos_from_emails(emails, config)
        
        # Save results
        output_path = config["report"]["output_path"]
        save_results(promos, output_path)
        
        # Print summary
        print_summary(promos)
        
        # Calculate duration
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(f"✅ Completed successfully in {duration:.1f} seconds")
        
    except (SetupError, ConfigurationError) as e:
        logger.error(f"\n{e}\n")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.warning("\n\n⚠️  Operation cancelled by user")
        sys.exit(130)
        
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}")
        logger.error("Stack trace:", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()