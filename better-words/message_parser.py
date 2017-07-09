from os import listdir
from os.path import splitext
from collections import namedtuple
import re
import yaml

# A named tuple representing a match from the parser
ParserMatch = namedtuple('ParserMatch', 'message category entry word')

class MessageParser(object):
    """A class used to parse a given message for a target word or phrase."""
    def __init__(self):
        # iterate over all the word categories and load up each yml file
        words = {}
        for file_name in listdir('./better-words/words'):
            category, extension = splitext(file_name)
            if extension == '.yml':
                with open('./better-words/words/' + file_name, 'r') as stream:
                    words[category] = yaml.load(stream)

        self.words = self.parse_yaml(words)

    def parse_yaml(self, dictionary):
        """
        Recursively convert a dictionary into a generic named tuple
        we use this to transform our YML data into an immutable tuple
        """
        for key, value in dictionary.iteritems():
            if isinstance(value, dict):
                dictionary[key] = self.parse_yaml(value)
            if isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, dict):
                        value[index] = self.parse_yaml(item)

        return namedtuple('WordsYaml', dictionary.keys())(**dictionary)

    # TODO: handle messages that contain multiple matches
    # TODO: check if the user has opted out
    def is_match(self, message):
        """
        Check if the given message contains a word or phrase match

        @param message: the message to check
        @return: a ParserMatch tuple if a match is found, otherwise None
        """
        for category in self.words:
            for entry in category.entries:
                for word in entry.words:
                    match = word_match(word, message.get('text'))
                    if match:
                        return ParserMatch(message, category, entry, match.group(0))
        return None

def word_match(word, string):
    # Matches the word only if it is not surrounded by backticks
    regex = r'(?!\B`[^`]*)\b' + word + r'\b(?![^`]*`\B)'
    return re.search(regex, string, re.IGNORECASE)

def format_match(match):
    """format a message to be sent to the user"""
    user = match.message.get('user')
    message_text = match.message.get('text')

    # if the message is multiple lines, reduce the message text
    # to be quoted to only the line containing the matching word
    # TODO: replace by linking / sharing the original message
    # to the user
    lines = message_text.split('\n')
    if len(lines) > 1:
        for line in lines:
            if word_match(match.word, line):
                message_text = line
                break

    formatted = "Hey <@{}>, I noticed you said:\n".format(user)
    formatted += "> {}\n".format(message_text) # quoted message they sent
    formatted += "{}\n\n".format(match.category.response) # explanation of why word is harmful
    formatted += "Instead of _'{}'_, try some of the following examples:\n".format(match.word)
    formatted += "* {}".format('\n* '.join(match.entry.suggestions))
    return formatted
