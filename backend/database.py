# Database connection for Home & Verse
# Connects to the SAME database as dm-sales-app to share the product cache
import os
from sqlalchemy import create_engine, Column, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Get database URL from environment (same as dm-sales-app on Render)
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Handle Render's postgres:// vs postgresql:// URL format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine - use SQLite fallback for local development
if DATABASE_URL:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    print(f"DATABASE: Connected to PostgreSQL (shared with dm-sales-app)")
else:
    # Local SQLite fallback - for local testing only
    sqlite_path = os.path.join(os.path.dirname(__file__), "local.db")
    engine = create_engine(f"sqlite:///{sqlite_path}", connect_args={"check_same_thread": False})
    print(f"DATABASE: Using local SQLite at {sqlite_path}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ============ Models ============
# These mirror the dm-sales-app models for the shared cache

class ProductCache(Base):
    """Stores the cached product data from Zoho - shared with dm-sales-app"""
    __tablename__ = "product_cache"
    
    id = Column(String, primary_key=True, default="main")
    items_json = Column(Text, nullable=False)
    item_count = Column(Float, default=0)
    cached_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
