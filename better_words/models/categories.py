from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from base import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(String(40), primary_key=True)
    response = Column(Text)
    words = relationship('Word',
      backref='category',
      cascade='all, delete, delete-orphan')
