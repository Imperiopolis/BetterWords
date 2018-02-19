from sqlalchemy import Column, ForeignKey, String, Table
from base import Base

word_to_link = Table('link_to_word_associations', Base.metadata,
    Column('link_id', String(40), ForeignKey('links.id'), primary_key=True),
    Column('word_id', String(40), ForeignKey('words.id'), primary_key=True)
)

word_to_suggestion = Table('suggestion_to_word_associations', Base.metadata,
    Column('suggestion_id', String(40), ForeignKey('suggestions.id'), primary_key=True),
    Column('word_id', String(40), ForeignKey('words.id'), primary_key=True)
)
