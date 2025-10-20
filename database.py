"""
Database models and operations for Gmail Promo Agent
Uses SQLAlchemy ORM with SQLite
"""

from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Create database engine
DATABASE_URL = "sqlite:///./promo_agent.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# ============================================================================
# DATABASE MODELS (Tables)
# ============================================================================

class User(Base):
    """User account"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)  # Unique user ID
    email = Column(String, unique=True, index=True)    # Gmail address
    gmail_token = Column(Text, nullable=True)          # Encrypted OAuth token
    created_at = Column(DateTime, default=datetime.utcnow)
    last_scan = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationship to promo codes
    promo_codes = relationship("PromoCode", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class PromoCode(Base):
    """Promotional code extracted from email"""
    __tablename__ = "promo_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    
    # Promo details
    code = Column(String, index=True)
    merchant = Column(String, index=True)
    discount = Column(String)
    category = Column(String, index=True)
    
    # Metadata
    expiration = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    raw_text = Column(Text, nullable=True)
    
    # Computed fields
    days_left = Column(Integer, nullable=True)
    urgency_text = Column(String, nullable=True)
    urgency_class = Column(String, nullable=True)
    
    # Status
    is_used = Column(Boolean, default=False)
    is_expired = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to user
    user = relationship("User", back_populates="promo_codes")
    
    def __repr__(self):
        return f"<PromoCode(code={self.code}, merchant={self.merchant})>"

# ============================================================================
# DATABASE OPERATIONS
# ============================================================================

def init_database():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized successfully")

def get_db():
    """Get database session (use with FastAPI Depends)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# USER OPERATIONS
# ============================================================================

def create_user(db, user_id: str, email: str, gmail_token: str = None):
    """Create a new user"""
    user = User(
        id=user_id,
        email=email,
        gmail_token=gmail_token
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db, user_id: str):
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db, email: str):
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def update_user_token(db, user_id: str, gmail_token: str):
    """Update user's Gmail token"""
    user = get_user(db, user_id)
    if user:
        user.gmail_token = gmail_token
        db.commit()
        return user
    return None

def update_last_scan(db, user_id: str):
    """Update user's last scan timestamp"""
    user = get_user(db, user_id)
    if user:
        user.last_scan = datetime.utcnow()
        db.commit()
        return user
    return None

# ============================================================================
# PROMO CODE OPERATIONS
# ============================================================================

def create_promo_code(db, user_id: str, promo_data: dict):
    """Create a new promo code"""
    promo = PromoCode(
        user_id=user_id,
        code=promo_data.get('code'),
        merchant=promo_data.get('merchant'),
        discount=promo_data.get('discount'),
        category=promo_data.get('category'),
        expiration=promo_data.get('expiration'),
        subject=promo_data.get('subject'),
        raw_text=promo_data.get('raw'),
        days_left=promo_data.get('days_left'),
        urgency_text=promo_data.get('urgency_text'),
        urgency_class=promo_data.get('urgency_class'),
        is_expired=promo_data.get('is_expired', False)
    )
    db.add(promo)
    db.commit()
    db.refresh(promo)
    return promo

def get_user_promos(db, user_id: str, category: str = None, include_expired: bool = False):
    """Get all promo codes for a user"""
    query = db.query(PromoCode).filter(PromoCode.user_id == user_id)
    
    # Filter out expired codes unless explicitly requested
    if not include_expired:
        query = query.filter(PromoCode.is_expired == False)
    
    # Filter by category if specified
    if category:
        query = query.filter(PromoCode.category == category)
    
    # Order by urgency (expiring soon first), then by creation date
    query = query.order_by(PromoCode.days_left, PromoCode.created_at.desc())
    
    return query.all()

def get_promo_by_code(db, user_id: str, code: str):
    """Get a specific promo code"""
    return db.query(PromoCode).filter(
        PromoCode.user_id == user_id,
        PromoCode.code == code
    ).first()

def mark_promo_used(db, user_id: str, code: str):
    """Mark a promo code as used"""
    promo = get_promo_by_code(db, user_id, code)
    if promo:
        promo.is_used = True
        db.commit()
        return promo
    return None

def delete_promo(db, user_id: str, code: str):
    """Delete a promo code"""
    promo = get_promo_by_code(db, user_id, code)
    if promo:
        db.delete(promo)
        db.commit()
        return True
    return False

def delete_all_user_promos(db, user_id: str):
    """Delete all promo codes for a user"""
    db.query(PromoCode).filter(PromoCode.user_id == user_id).delete()
    db.commit()

def get_promo_stats(db, user_id: str):
    """Get statistics about user's promo codes"""
    all_promos = db.query(PromoCode).filter(PromoCode.user_id == user_id)
    
    total = all_promos.count()
    active = all_promos.filter(PromoCode.is_expired == False).count()
    expired = all_promos.filter(PromoCode.is_expired == True).count()
    used = all_promos.filter(PromoCode.is_used == True).count()
    expiring_soon = all_promos.filter(
        PromoCode.is_expired == False,
        PromoCode.days_left <= 7
    ).count()
    
    # Category breakdown
    categories = {}
    for promo in all_promos.filter(PromoCode.is_expired == False).all():
        cat = promo.category
        categories[cat] = categories.get(cat, 0) + 1
    
    return {
        "total_promos": total,
        "active_promos": active,
        "expired_promos": expired,
        "used_promos": used,
        "expiring_soon": expiring_soon,
        "categories": categories
    }

# ============================================================================
# BULK OPERATIONS
# ============================================================================

def bulk_insert_promos(db, user_id: str, promos_list: list):
    """Insert multiple promo codes at once (faster for initial scan)"""
    promo_objects = []
    
    for promo_data in promos_list:
        promo = PromoCode(
            user_id=user_id,
            code=promo_data.get('code'),
            merchant=promo_data.get('merchant', 'Unknown'),
            discount=promo_data.get('discount', 'Check email for details'),
            category=promo_data.get('category', 'Other'),
            expiration=promo_data.get('expiration'),
            subject=promo_data.get('subject'),
            raw_text=promo_data.get('raw'),
            days_left=promo_data.get('days_left'),
            urgency_text=promo_data.get('urgency_text'),
            urgency_class=promo_data.get('urgency_class'),
            is_expired=promo_data.get('is_expired', False)
        )
        promo_objects.append(promo)
    
    db.bulk_save_objects(promo_objects)
    db.commit()
    
    return len(promo_objects)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def database_exists():
    """Check if database file exists"""
    return os.path.exists("promo_agent.db")

def get_database_stats():
    """Get overall database statistics"""
    db = SessionLocal()
    try:
        total_users = db.query(User).count()
        total_promos = db.query(PromoCode).count()
        active_promos = db.query(PromoCode).filter(PromoCode.is_expired == False).count()
        
        return {
            "total_users": total_users,
            "total_promos": total_promos,
            "active_promos": active_promos
        }
    finally:
        db.close()

if __name__ == "__main__":
    # Initialize database when run directly
    print("Initializing database...")
    init_database()
    print("Database setup complete!")
    print(f"Database file: {os.path.abspath('promo_agent.db')}")