from typing import Any

from app.config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal: Any = sessionmaker(autocommit=False, autoflush=False, bind=engine)
