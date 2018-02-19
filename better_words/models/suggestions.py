from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from base import Base

class Suggestion(Base):
    __tablename__ = 'suggestions'
    id = Column(String(40), primary_key=True)
    word = Column(String(255), nullable=False)
