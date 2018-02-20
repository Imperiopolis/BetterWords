from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from base import Base
from associations import word_to_link, word_to_suggestion

class Word(Base):
    __tablename__ = 'words'
    id = Column(String(40), primary_key=True)
    word = Column(String(255), nullable=False)
    category_slug = Column(String(255), ForeignKey('categories.slug'))
    category = relationship('Category', back_populates='words')
    links = relationship('Link',
        secondary=word_to_link,
        backref='words')
    suggestions = relationship('Suggestion',
        secondary=word_to_suggestion,
        backref='words')
