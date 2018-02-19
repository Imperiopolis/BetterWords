from sqlalchemy import Column, String
from base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(String(40), primary_key=True)
