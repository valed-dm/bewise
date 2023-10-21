"""Quiz question table model"""

import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime
)
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DB_URL = os.environ.get("PG_CONN_STR")
DB_ECHO = True

engine = create_engine(url=DB_URL, echo=DB_ECHO)


class Base(DeclarativeBase):
    """SQLAlchemy Base class"""


class Quiz(Base):
    """Quiz questions table"""
    __tablename__ = 'questions'

    id: int = Column(Integer, primary_key=True)
    question: str = Column(String(400), unique=True)
    answer: str = Column(String(100))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)


def create_database() -> None:
    """Creates database tables"""
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_database()
