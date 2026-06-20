from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

"""Database connection and session management for the application."""
# def get_db():
#     """Dependency - yield a SQLAlchemy session and ensure it's closed after use."""
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
