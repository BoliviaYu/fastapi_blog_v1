from app.config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(settings.DATABASE_URL)


def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
