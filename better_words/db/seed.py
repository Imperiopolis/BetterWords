from db import session

from os import listdir, getcwd
from os.path import splitext
from collections import namedtuple
import re
import yaml
from better_words.models import *

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

# TODO: Make this actually work
for category, value in words._asdict().iteritems():
    c = Category(slug=category, response=value.response)
    session.add(c)

    for entry in value.entries:
        for word in entry.words:
            session.add(Word(slug=category+'_'+word, word=word, category_slug=category))

    session.commit()

# u = models.User(id='abcd', name='123')
# session.add(u)
# session.commit()
