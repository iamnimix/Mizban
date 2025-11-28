from sqlalchemy import Column, String, Integer

from .database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String(5), nullable=False, index=True, unique=True)
