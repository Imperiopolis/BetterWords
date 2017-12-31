from sqlalchemy import Column, String
from base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
