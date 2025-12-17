"""
Core Database Connection - FIXED VERSION
Use THIS file for all database connections
Compatible with SQLAlchemy 2.0
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
import sys
from pathlib import Path

# Add config to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.database_config import DATABASE_CONFIG

# Create Base for models
Base = declarative_base()

# Create database URL
DATABASE_URL = (
    f"mysql+mysqlconnector://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}/{DATABASE_CONFIG['database']}"
    f"?charset={DATABASE_CONFIG['charset']}"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,  # Set True for SQL logging
    pool_size=10,
    max_overflow=20
)

# Create SessionLocal
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


def get_db():
    """
    Get database session - MANUAL close required
    
    Usage:
        db = get_db()
        try:
            # Your code
            patient = db.query(Patient).first()
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()  # IMPORTANT!
    
    Returns:
        Session: SQLAlchemy session
    """
    return SessionLocal()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions - AUTO close
    
    Usage:
        with get_db_context() as db:
            patient = db.query(Patient).first()
            # Auto-commits on success, auto-rollback on error
    
    Yields:
        Session: SQLAlchemy session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Create all database tables"""
    # Import models to register them
    import core.models
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")


def drop_db():
    """Drop all database tables - USE WITH CAUTION!"""
    import core.models
    Base.metadata.drop_all(bind=engine)
    print("⚠️ All tables dropped")


def test_connection():
    """Test database connection - FIXED for SQLAlchemy 2.0"""
    try:
        with get_db_context() as db:
            # Use text() wrapper for raw SQL (SQLAlchemy 2.0 requirement)
            db.execute(text("SELECT 1"))
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def get_engine():
    """Get SQLAlchemy engine"""
    return engine


# Export everything
__all__ = [
    'Base',
    'engine',
    'SessionLocal',
    'get_db',
    'get_db_context',
    'init_db',
    'drop_db',
    'test_connection',
    'get_engine',
    'DATABASE_URL'
]