from os import listdir
from os.path import splitext
from collections import namedtuple
from db import session
from models import *
import re
import yaml
from sqlalchemy import and_

# A named tuple representing a match from the parser
ParserMatch = namedtuple('ParserMatch', 'message model word')
FormattedMatch = namedtuple('FormattedMatch', 'intro explanation')

# TODO: handle messages that contain multiple matches
# TODO: check if the user has opted out
def is_match(message):
    """
    Check if the given message contains a word or phrase match

    @param message: the message to check
    @return: a ParserMatch tuple if a match is found, otherwise None
    """
    user_id = message.get('user')

    # Fetch the user from the DB, or add if needed
    user = session.query(User).get(user_id)
    if not user:
        user = session.add(User(id=user_id))
        session.commit()

    # Find all the words the users hasn't opted out of
    words = session.query(Word)\
        .outerjoin(UserCategoryOptOut,
            and_(UserCategoryOptOut.category_slug == Word.category_slug,
                UserCategoryOptOut.user_id == user.id))\
        .filter(UserCategoryOptOut.category_slug == None)

    # Check each possible word for a match
    # TODO: Handle if more than one word matches, right now this just returns on
    # the very first match we locate
    # TODO: move the `word_match` functionality into the query above, so we don't
    # have to iterate over all the words to find which ones that actually apply
    for word in words:
        match = word_match(word.word, message.get('text'))
        if match:
            return ParserMatch(message, word, match.group(0))
    return None

def word_match(word, string):
    # Matches the word only if it is not surrounded by backticks
    regex = r'(?!\B`[^`]*)\b' + word + r'\b(?![^`]*`\B)'
    return re.search(regex, string, re.IGNORECASE)

def format_match(match):
    """format a message to be sent to the user"""
    user = match.message.get('user')
    message_text = match.message.get('text')
    suggestions = [suggestion.word for suggestion in match.model.suggestions]

    intro = "Hey <@{}>, I noticed you said \"{}\"\n\n".format(user, match.word)

    explanation = "{}\n\n".format(match.model.category.response) # explanation of why word is harmful
    explanation += "Instead of \"{}\", try some of the following examples:\n".format(match.word)
    explanation += "* {}".format('\n* '.join(suggestions))

    return FormattedMatch(intro, explanation)
