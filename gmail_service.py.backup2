"""
Gmail Service - Handles Gmail API operations
Wraps the existing gmail_agent.py logic for API use
"""

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import base64
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import json
import os

from promo_parser import extract_promos, categorize_promo, deduplicate_promos, extract_merchant_name
from dashboard_generator import enrich_promo_data

# OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# ============================================================================
# OAUTH FLOW
# ============================================================================

def create_oauth_flow(credentials_path: str, redirect_uri: str):
    """
    Create OAuth flow for user authorization
    
    Args:
        credentials_path: Path to OAuth credentials JSON
        redirect_uri: Where Google redirects after auth
    """
    return Flow.from_client_secrets_file(
        credentials_path,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )

def get_authorization_url(flow: Flow) -> Tuple[str, str]:
    """
    Generate authorization URL for user to visit
    
    Returns:
        (authorization_url, state)
    """
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'  # Force consent screen to get refresh token
    )
    return authorization_url, state

def exchange_code_for_token(flow: Flow, authorization_response: str) -> dict:
    """
    Exchange authorization code for access token
    
    Args:
        flow: OAuth flow object
        authorization_response: Full callback URL from Google
        
    Returns:
        Token info dictionary
    """
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

# ============================================================================
# GMAIL SERVICE
# ============================================================================

def get_gmail_service(token_info: dict):
    """
    Create Gmail API service from token info
    
    Args:
        token_info: Dictionary with token, refresh_token, etc.
    """
    credentials = Credentials(
        token=token_info['token'],
        refresh_token=token_info.get('refresh_token'),
        token_uri=token_info['token_uri'],
        client_id=token_info['client_id'],
        client_secret=token_info['client_secret'],
        scopes=token_info['scopes']
    )
    
    # Refresh if expired
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    
    return build('gmail', 'v1', credentials=credentials)

def refresh_token_if_needed(token_info: dict) -> dict:
    """
    Refresh token if expired
    
    Returns:
        Updated token_info
    """
    credentials = Credentials(
        token=token_info['token'],
        refresh_token=token_info.get('refresh_token'),
        token_uri=token_info['token_uri'],
        client_id=token_info['client_id'],
        client_secret=token_info['client_secret'],
        scopes=token_info['scopes']
    )
    
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        token_info['token'] = credentials.token
    
    return token_info

# ============================================================================
# EMAIL FETCHING
# ============================================================================

def fetch_promotional_emails(service, query: str = "category:promotions newer_than:7d", max_results: int = 50) -> List[Dict]:
    """
    Fetch promotional emails from Gmail
    
    Args:
        service: Gmail API service
        query: Gmail search query
        max_results: Maximum number of emails to fetch
        
    Returns:
        List of email messages
    """
    try:
        messages = []
        page_token = None
        
        while len(messages) < max_results:
            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=min(50, max_results - len(messages)),
                pageToken=page_token
            ).execute()
            
            batch = results.get('messages', [])
            if not batch:
                break
            
            messages.extend(batch)
            page_token = results.get('nextPageToken')
            
            if not page_token:
                break
        
        # Fetch full message details
        full_messages = []
        for msg in messages:
            try:
                full_msg = service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='full'
                ).execute()
                full_messages.append(full_msg)
            except Exception as e:
                print(f"Error fetching message {msg['id']}: {e}")
                continue
        
        return full_messages
        
    except Exception as e:
        print(f"Error fetching emails: {e}")
        raise

# ============================================================================
# EMAIL PARSING
# ============================================================================

def parse_email(msg: Dict) -> Tuple[str, str, str]:
    """
    Parse email to extract text, subject, and sender
    
    Returns:
        (body_text, subject, sender)
    """
    # Extract headers
    headers = msg['payload'].get('headers', [])
    subject = ''
    sender = ''
    
    for header in headers:
        header_name = header['name'].lower()
        if header_name == 'subject':
            subject = header['value']
        elif header_name == 'from':
            sender = header['value']
    
    # Extract body
    payload = msg['payload']
    body_text = ''
    
    if 'parts' in payload:
        for part in payload['parts']:
            body_text += _extract_part_text(part)
    else:
        body_text = _extract_part_text(payload)
    
    return body_text, subject, sender

def _extract_part_text(part: Dict) -> str:
    """Extract text from email part (handles HTML and plain text)"""
    mime_type = part.get('mimeType', '')
    body = part.get('body', {})
    data = body.get('data', '')
    
    if not data:
        if 'parts' in part:
            text = ''
            for nested_part in part['parts']:
                text += _extract_part_text(nested_part)
            return text
        return ''
    
    try:
        decoded = base64.urlsafe_b64decode(data.encode('UTF-8')).decode('UTF-8', errors='ignore')
        
        if 'html' in mime_type.lower():
            soup = BeautifulSoup(decoded, 'html.parser')
            for script in soup(['script', 'style']):
                script.decompose()
            text = soup.get_text(separator=' ', strip=True)
            return text
        else:
            return decoded
    
    except Exception as e:
        print(f"Error decoding email part: {e}")
        return ''

# ============================================================================
# PROMO EXTRACTION
# ============================================================================

def extract_promos_from_emails(emails: List[Dict], categories_path: str = "categories.json") -> List[Dict]:
    """
    Extract promo codes from a list of emails
    
    Args:
        emails: List of Gmail message objects
        categories_path: Path to categories.json
        
    Returns:
        List of extracted and enriched promo codes
    """
    all_promos = []
    
    for email in emails:
        try:
            body_text, subject, sender = parse_email(email)
            
            # Extract promos
            promos = extract_promos(body_text, subject, sender)
            
            # Categorize
            categorized = [categorize_promo(p, categories_path) for p in promos]
            
            all_promos.extend(categorized)
            
        except Exception as e:
            print(f"Error processing email: {e}")
            continue
    
    # Deduplicate
    unique_promos = deduplicate_promos(all_promos)
    
    # Enrich with urgency data
    enriched_promos = enrich_promo_data(unique_promos)
    
    return enriched_promos

# ============================================================================
# HIGH-LEVEL SCAN FUNCTION
# ============================================================================

def scan_gmail_for_promos(token_info: dict, query: str = "category:promotions newer_than:7d", max_emails: int = 50) -> Dict:
    """
    Complete Gmail scanning workflow
    
    Args:
        token_info: OAuth token dictionary
        query: Gmail search query
        max_emails: Maximum emails to process
        
    Returns:
        Dictionary with scan results and extracted promos
    """
    try:
        # Create Gmail service
        service = get_gmail_service(token_info)
        
        # Fetch emails
        emails = fetch_promotional_emails(service, query, max_emails)
        
        if not emails:
            return {
                'success': True,
                'emails_scanned': 0,
                'promos_found': 0,
                'promos': [],
                'message': 'No promotional emails found in the specified timeframe'
            }
        
        # Extract promos
        promos = extract_promos_from_emails(emails)
        
        return {
            'success': True,
            'emails_scanned': len(emails),
            'promos_found': len(promos),
            'promos': promos,
            'message': f'Successfully scanned {len(emails)} emails and found {len(promos)} promo codes'
        }
        
    except Exception as e:
        return {
            'success': False,
            'emails_scanned': 0,
            'promos_found': 0,
            'promos': [],
            'error': str(e),
            'message': f'Error scanning Gmail: {str(e)}'
        }

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def test_gmail_connection(token_info: dict) -> bool:
    """
    Test if Gmail API connection works
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        service = get_gmail_service(token_info)
        # Try to get user profile
        profile = service.users().getProfile(userId='me').execute()
        return True
    except Exception as e:
        print(f"Gmail connection test failed: {e}")
        return False

def get_user_email(token_info: dict) -> str:
    """
    Get the user's Gmail address
    
    Returns:
        Email address or None if error
    """
    try:
        service = get_gmail_service(token_info)
        profile = service.users().getProfile(userId='me').execute()
        return profile.get('emailAddress')
    except Exception as e:
        print(f"Error getting user email: {e}")
        return None