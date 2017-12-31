from sqlalchemy import Column, ForeignKey, String, Table
from base import Base

word_to_link = Table('link_to_word_associations', Base.metadata,
    Column('link_href', String(255), ForeignKey('links.slug')),
    Column('word_slug', String(255), ForeignKey('words.slug'))
)

word_to_suggestion = Table('suggestion_to_word_associations', Base.metadata,
    Column('suggestion_slug', String(255), ForeignKey('suggestions.slug')),
    Column('word_slug', String(255), ForeignKey('words.slug'))
)
