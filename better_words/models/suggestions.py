from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from base import Base
from associations import word_to_suggestion

class Suggestion(Base):
    __tablename__ = 'suggestions'
    slug = Column(String(255), primary_key=True)
    word = Column(String(255), nullable=False)
    words = relationship('Word',
        secondary=word_to_suggestion,
        back_populates='suggestions')
