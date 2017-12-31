from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from better_words.models import *

engine = create_engine(environ.get('DATABASE_URL', 'sqlite:///db.sqlite'))

Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
