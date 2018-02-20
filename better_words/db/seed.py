from db import session

from os import listdir, getcwd
from os.path import splitext
from collections import namedtuple
from hashlib import sha1
import re
import yaml
from better_words.models import *

def create_id(value, prefix=""):
    # Hash the value to produce a clean id (no special characters, spaces, etc.)
    return sha1(prefix+value).hexdigest()

def parse_yaml(dictionary):
    """
    Recursively convert a dictionary into a generic named tuple
    we use this to transform our YML data into an immutable tuple
    """
    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            dictionary[key] = parse_yaml(value)
        if isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    value[index] = parse_yaml(item)

    return namedtuple('WordsYaml', dictionary.keys())(**dictionary)

# iterate over all the word categories and load up each yml file
words = {}
for file_name in listdir('./better_words/words'):
    category, extension = splitext(file_name)
    if extension == '.yml':
        with open('./better_words/words/' + file_name, 'r') as stream:
            words[category] = yaml.load(stream)

words = parse_yaml(words)

# Purge old word data from the DB
session.query(Category).delete()
session.query(Word).delete()
session.query(Suggestion).delete()
session.query(Link).delete()
session.execute('DELETE FROM link_to_word_associations')
session.execute('DELETE FROM suggestion_to_word_associations')

for category, value in words._asdict().iteritems():
    # Create the category, and store its response
    c = Category(slug=category, response=value.response)
    session.add(c)

    # Create each word entry for within the category
    for entry in value.entries:
        prefix = category+'_'+entry.type+'_'

        suggestion_models = []
        for suggestion in entry.suggestions:
            model = Suggestion(id=create_id(suggestion, prefix), word=suggestion)
            session.add(model)
            suggestion_models.append(model)

        link_models = []
        # Links are optional, so they might not exist
        if (hasattr(entry, 'links')):
            for link in entry.links:
                model = Link(id=create_id(link, prefix), href=link)
                session.add(model)
                link_models.append(model)

        for word in entry.words:
            model = Word(id=create_id(word, prefix), word=word, category_slug=category)

            # Create associations
            [model.suggestions.append(suggestion) for suggestion in suggestion_models]
            [model.links.append(link) for link in link_models if link_models]

            session.add(model)

session.commit()
