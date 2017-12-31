from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from base import Base
from associations import word_to_link

class Link(Base):
    __tablename__ = 'links'
    slug = Column(Text, primary_key=True)
    href = Column(Text)
    words = relationship('Word',
        secondary=word_to_link,
        back_populates='links')
