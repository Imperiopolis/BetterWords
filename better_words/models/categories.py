from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from base import Base

class Category(Base):
    __tablename__ = 'categories'
    slug = Column(String(255), primary_key=True)
    response = Column(Text)
    words = relationship('Word', back_populates='category')
