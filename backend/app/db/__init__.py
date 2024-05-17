from app import models

from .base import Base
from .session import engine

Base.metadata.create_all(engine)
