import yaml
import re
from os import listdir
from os.path import splitext
from collections import namedtuple

# A named tuple representing a match from the parser
ParserMatch = namedtuple('ParserMatch', 'message category entry word')

class MessageParser(object):
  def __init__(self):
    # iterate over all the word categories and load up each yml file
    words = {}
    for file in listdir('./better-words/words'):
      category, extension = splitext(file)
      if extension == '.yml':
        with open('./better-words/words/' + file, 'r') as stream:
          words[category] = yaml.load(stream)

    self.words = self.parseYaml(words)

  # Recursively convert a dictionary into a generic named tuple
  # we use this to transform our YML data into an immutable tuple
  def parseYaml(self, dictionary):
    for key, value in dictionary.iteritems():
      if isinstance(value, dict):
        dictionary[key] = self.parseYaml(value)
      if isinstance(value, list):
        for index, v in enumerate(value):
          if isinstance(v, dict):
            value[index] = self.parseYaml(v)

    return namedtuple('WordsYaml', dictionary.keys())(**dictionary)

  # check if the given message contains a word or phrase match
  # TODO: handle messages that contain multiple matches
  # TODO: check if the user has opted out
  def is_match(self, message):
    for category in self.words:
      for entry in category.entries:
        for word in entry.words:
          regex = r'\b' + word + r'\b'
          match = re.search(regex, message.get('text'))
          if match:
            return ParserMatch(message, category, entry, match.group(0))
    return None

  # format a message to be sent to the user
  def format(self, match):
    user = match.message.get('user')
    message_text = match.message.get('text')

    # if the message is multiple lines, reduce the message text
    # to be quoted to only the line containing the matching word
    # TODO: replace by linking / sharing the original message
    # to the user
    lines = message_text.split('\n')
    if len(lines) > 1:
      for line in lines:
        regex = r'\b' + match.word + r'\b'
        match = re.search(regex, line)
        if match:
          message_text = line
          break

    formatted = "Hey <@{}>, I noticed you said:\n".format(user)
    formatted += "> {}\n".format(message_text) # quoted message they sent
    formatted += "{}\n\n".format(match.category.response) # explanation of why the word is harmful
    formatted += "Instead of _'{}'_, try some of the following examples:\n".format(match.word)
    formatted += "* {}".format('\n* '.join(match.entry.suggestions))
    return formatted
