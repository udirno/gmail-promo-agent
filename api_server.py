"""
FastAPI Backend for Gmail Promo Agent
Now with database integration and OAuth!
"""

# IMPORTANT: Allow HTTP for local OAuth development
# In production, always use HTTPS!
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
import uvicorn
from datetime import datetime
import os
import secrets

# Import database
from database import (
    init_database, get_db, 
    create_user, get_user, get_user_by_email,
    create_promo_code, get_user_promos, get_promo_by_code,
    mark_promo_used, delete_promo, get_promo_stats,
    bulk_insert_promos, delete_all_user_promos,
    database_exists, get_database_stats
)

# Import Gmail service
from gmail_service import (
    create_oauth_flow, get_authorization_url, exchange_code_for_token,
    scan_gmail_for_promos, test_gmail_connection, get_user_email,
    refresh_token_if_needed
)
import secrets

# Store for OAuth states (in production, use Redis)
oauth_states = {}

# Initialize FastAPI app
app = FastAPI(
    title="Gmail Promo Agent API",
    description="Extract and manage promotional codes from Gmail",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DATA MODELS
# ============================================================================

class PromoCode(BaseModel):
    """Represents a single promo code"""
    code: str
    merchant: str
    discount: str
    category: str
    expiration: Optional[str] = None
    urgency_text: Optional[str] = None
    urgency_class: Optional[str] = None
    days_left: Optional[int] = None
    subject: Optional[str] = None
    is_used: bool = False
    is_expired: bool = False
    created_at: Optional[str] = None

class CreateUserRequest(BaseModel):
    """Request to create a new user"""
    user_id: str
    email: str

class ScanRequest(BaseModel):
    """Request to scan Gmail for promos"""
    user_id: str

class ScanResponse(BaseModel):
    """Response after scanning"""
    success: bool
    total_promos: int
    active_promos: int
    expiring_soon: int
    categories: List[str]
    message: str

class StatsResponse(BaseModel):
    """User statistics response"""
    total_promos: int
    active_promos: int
    expired_promos: int
    used_promos: int
    expiring_soon: int
    categories: dict
    last_scan: Optional[str] = None

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "message": "Gmail Promo Agent API is running",
        "version": "1.0.0",
        "database": "connected" if database_exists() else "not initialized",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check(db: Session = Depends(get_db)):
    """Detailed health check"""
    try:
        db_stats = get_database_stats()
        return {
            "status": "healthy",
            "database": "connected",
            "gmail_api": "ready",
            "stats": db_stats
        }
    except Exception as e:
        return {
            "status": "degraded",
            "database": "error",
            "error": str(e)
        }

# ============================================================================
# OAUTH ENDPOINTS
# ============================================================================

@app.get("/api/auth/start")
async def start_oauth(user_id: str, db: Session = Depends(get_db)):
    """
    Start OAuth flow - generates authorization URL
    
    Parameters:
    - user_id: User identifier
    
    Returns:
    - authorization_url: URL for user to visit
    - state: Security token (store this)
    """
    try:
        # Check if credentials.json exists
        if not os.path.exists("credentials.json"):
            raise HTTPException(
                status_code=500,
                detail="OAuth credentials not configured. Admin needs to set up credentials.json"
            )
        
        # Create OAuth flow
        redirect_uri = "http://localhost:8000/api/auth/callback"
        flow = create_oauth_flow("credentials.json", redirect_uri)
        
        # Generate authorization URL
        auth_url, state = get_authorization_url(flow)
        
        # Store state temporarily (link it to user_id)
        oauth_states[state] = {
            'user_id': user_id,
            'flow': flow,
            'timestamp': datetime.now()
        }
        
        return {
            'authorization_url': auth_url,
            'state': state,
            'message': 'Visit the authorization_url to connect your Gmail account'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/auth/callback")
async def oauth_callback(code: str = None, state: str = None, error: str = None, db: Session = Depends(get_db)):
    """
    OAuth callback - Google redirects here after user authorizes
    
    This is called automatically by Google after user clicks "Allow"
    """
    try:
        if error:
            return {
                'success': False,
                'error': error,
                'message': 'User denied authorization or error occurred'
            }
        
        if not code or not state:
            raise HTTPException(status_code=400, detail="Missing code or state")
        
        # Retrieve stored state
        if state not in oauth_states:
            raise HTTPException(status_code=400, detail="Invalid state - may have expired")
        
        state_data = oauth_states[state]
        user_id = state_data['user_id']
        flow = state_data['flow']
        
        # Exchange code for token
        authorization_response = f"http://localhost:8000/api/auth/callback?code={code}&state={state}"
        token_info = exchange_code_for_token(flow, authorization_response)
        
        # Get user's email address
        user_email = get_user_email(token_info)
        
        # Store token in database
        import json
        from database import update_user_token, create_user, get_user
        
        # Check if user exists
        user = get_user(db, user_id)
        if not user:
            # Create new user
            user = create_user(db, user_id, user_email, json.dumps(token_info))
        else:
            # Update token
            update_user_token(db, user_id, json.dumps(token_info))
        
        # Clean up state
        del oauth_states[state]
        
        return {
            'success': True,
            'user_id': user_id,
            'email': user_email,
            'message': 'Gmail connected successfully! You can close this window.'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/auth/status/{user_id}")
async def check_auth_status(user_id: str, db: Session = Depends(get_db)):
    """Check if user has connected their Gmail"""
    try:
        from database import get_user
        
        user = get_user(db, user_id)
        if not user:
            return {
                'connected': False,
                'message': 'User not found'
            }
        
        if not user.gmail_token:
            return {
                'connected': False,
                'email': None,
                'message': 'Gmail not connected'
            }
        
        # Test connection
        import json
        token_info = json.loads(user.gmail_token)
        is_valid = test_gmail_connection(token_info)
        
        return {
            'connected': is_valid,
            'email': user.email,
            'message': 'Gmail connected' if is_valid else 'Token expired or invalid'
        }
        
    except Exception as e:
        return {
            'connected': False,
            'error': str(e)
        }

@app.post("/api/auth/disconnect/{user_id}")
async def disconnect_gmail(user_id: str, db: Session = Depends(get_db)):
    """Disconnect Gmail from account"""
    try:
        from database import update_user_token
        
        update_user_token(db, user_id, None)
        
        return {
            'success': True,
            'message': 'Gmail disconnected successfully'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# USER ENDPOINTS
# ============================================================================

@app.post("/api/users")
async def create_new_user(request: CreateUserRequest, db: Session = Depends(get_db)):
    """Create a new user account"""
    try:
        # Check if user already exists
        existing_user = get_user(db, request.user_id)
        if existing_user:
            return {
                "success": False,
                "message": "User already exists",
                "user_id": request.user_id
            }
        
        # Create user
        user = create_user(db, request.user_id, request.email)
        
        return {
            "success": True,
            "message": "User created successfully",
            "user_id": user.id,
            "email": user.email
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/{user_id}")
async def get_user_info(user_id: str, db: Session = Depends(get_db)):
    """Get user information"""
    user = get_user(db, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "last_scan": user.last_scan.isoformat() if user.last_scan else None,
        "is_active": user.is_active
    }

# ============================================================================
# PROMO CODE ENDPOINTS
# ============================================================================

@app.post("/api/scan", response_model=ScanResponse)
async def scan_gmail(request: ScanRequest, db: Session = Depends(get_db)):
    """
    Scan Gmail for promo codes - REAL VERSION (Phase 3)
    """
    
    try:
        # Get user from database
        user = get_user(db, request.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if Gmail is connected
        if not user.gmail_token:
            raise HTTPException(
                status_code=400, 
                detail="Gmail not connected. Please connect your Gmail account first."
            )
        
        # Parse token from database
        import json
        token_info = json.loads(user.gmail_token)
        
        # Refresh token if needed
        token_info = refresh_token_if_needed(token_info)
        
        # REAL GMAIL SCAN - This calls the functions we just fixed!
        print(f"\n🔍 Starting Gmail scan for user: {request.user_id}")
        scan_result = scan_gmail_for_promos(
            token_info,
            query="category:promotions newer_than:7d",
            max_emails=50
        )
        
        if not scan_result['success']:
            raise HTTPException(
                status_code=500,
                detail=f"Gmail scan failed: {scan_result.get('message', 'Unknown error')}"
            )
        
        promos = scan_result['promos']
        print(f"✅ Scan complete! Found {len(promos)} promos")
        
        # Clear existing promos for this user
        delete_all_user_promos(db, request.user_id)
        
        # Insert new promos into database
        inserted_count = bulk_insert_promos(db, request.user_id, promos)
        
        # Update last scan time
        from database import update_last_scan
        update_last_scan(db, request.user_id)
        
        # Get updated stats
        stats = get_promo_stats(db, request.user_id)
        
        return ScanResponse(
            success=True,
            total_promos=inserted_count,
            active_promos=stats["active_promos"],
            expiring_soon=stats["expiring_soon"],
            categories=list(stats["categories"].keys()),
            message=f"Successfully scanned {scan_result['emails_scanned']} emails and found {inserted_count} promo codes"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Scan error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/promos/{user_id}", response_model=List[PromoCode])
async def get_promos(
    user_id: str, 
    category: Optional[str] = None,
    include_expired: bool = False,
    db: Session = Depends(get_db)
):
    """Get all promo codes for a user"""
    
    try:
        user = get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        promos = get_user_promos(db, user_id, category, include_expired)
        
        # Convert to response format
        return [
            PromoCode(
                code=p.code,
                merchant=p.merchant,
                discount=p.discount,
                category=p.category,
                expiration=p.expiration,
                urgency_text=p.urgency_text,
                urgency_class=p.urgency_class,
                days_left=p.days_left,
                subject=p.subject,
                is_used=p.is_used,
                is_expired=p.is_expired,
                created_at=p.created_at.isoformat() if p.created_at else None
            )
            for p in promos
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/categories")
async def get_categories():
    """Get all available categories"""
    
    import json
    
    try:
        with open("categories.json", "r") as f:
            categories = json.load(f)
        
        return {
            "categories": list(categories.keys()),
            "count": len(categories)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats/{user_id}", response_model=StatsResponse)
async def get_stats(user_id: str, db: Session = Depends(get_db)):
    """Get statistics for user's promo codes"""
    
    try:
        user = get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        stats = get_promo_stats(db, user_id)
        
        return StatsResponse(
            total_promos=stats["total_promos"],
            active_promos=stats["active_promos"],
            expired_promos=stats["expired_promos"],
            used_promos=stats["used_promos"],
            expiring_soon=stats["expiring_soon"],
            categories=stats["categories"],
            last_scan=user.last_scan.isoformat() if user.last_scan else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/promos/{user_id}/{code}")
async def delete_promo_code(user_id: str, code: str, db: Session = Depends(get_db)):
    """Delete a specific promo code"""
    
    try:
        user = get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        success = delete_promo(db, user_id, code)
        
        if not success:
            raise HTTPException(status_code=404, detail="Promo code not found")
        
        return {
            "success": True,
            "message": f"Deleted promo code: {code}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/promos/{user_id}/{code}/mark-used")
async def mark_code_used(user_id: str, code: str, db: Session = Depends(get_db)):
    """Mark a promo code as used"""
    
    try:
        user = get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        promo = mark_promo_used(db, user_id, code)
        
        if not promo:
            raise HTTPException(status_code=404, detail="Promo code not found")
        
        return {
            "success": True,
            "message": f"Marked promo code {code} as used"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# STARTUP / SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run when server starts"""
    print("=" * 60)
    print("🚀 Gmail Promo Agent API Starting...")
    print("=" * 60)
    
    # Initialize database if it doesn't exist
    if not database_exists():
        print("📦 Creating database...")
        init_database()
        print("✓ Database created successfully")
    else:
        print("✓ Database already exists")
    
    print("📍 Server running at: http://localhost:8000")
    print("📚 API docs available at: http://localhost:8000/docs")
    print("⚠️  Dev mode: HTTP allowed for OAuth (use HTTPS in production)")
    print("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Run when server shuts down"""
    print("\n👋 Gmail Promo Agent API shutting down...")

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )