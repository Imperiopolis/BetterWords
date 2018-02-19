from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from base import Base

class Link(Base):
    __tablename__ = 'links'
    id = Column(String(40), primary_key=True)
    href = Column(Text)
