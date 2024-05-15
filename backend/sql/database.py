from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, DateTime, String

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.mysql import DATETIME

engine = create_engine("mysql+pymysql://liam:LXLlxl520..@localhost:3306/test")

Session = sessionmaker(bind=engine)
Base = declarative_base()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


class BaseMixin:
    """model的基类，所有model都必须继承"""

    id = Column(Integer, primary_key=True)
    created_at = Column(DATETIME(fsp=6), default=datetime.now)
    updated_at = Column(
        DATETIME(fsp=6),
        default=datetime.now,
        onupdate=datetime.now,
        index=True,
    )


class User(Base, BaseMixin):
    __tablename__ = "user"

    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)


Base.metadata.create_all(engine)

with session_scope() as session:
    user = User(name="liam", email="", password="123456")
    session.add(user)
    session.commit()
