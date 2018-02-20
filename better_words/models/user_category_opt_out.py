from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from base import Base

class UserCategoryOptOut(Base):
    __tablename__ = 'user_category_opt_out'
    user_id = Column(String(255), ForeignKey('users.id'), primary_key=True)
    category_slug = Column(String(255), ForeignKey('categories.slug'), primary_key=True)
    user = relationship('User', backref='opted_out_categories')
    category = relationship('Category', backref='opted_out_users')
