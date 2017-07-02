import yaml
import re
from os import listdir
from os.path import splitext

class MessageParser(object):
  def __init__(self):
    self.words = {}

    # iterate over all the word categories and load up each yml file
    for file in listdir('./better-words/words'):
      category, extension = splitext(file)
      if extension == '.yml':
        with open('./better-words/words/' + file, 'r') as stream:
          self.words[category] = yaml.load(stream)

  # check if the given message contains a word or phrase match
  # TODO: handle messages that contain multiple matches
  # TODO: check if the user has opted out
  def is_match(self, message):
    for category in self.words:
      for entry in self.words[category]['entries']:
        for word in entry['words']:
          regex = r'\b' + word + r'\b'
          match = re.search(regex, message.get('text'))
          if match:
            return {
              'message': message,
              'category': self.words[category],
              'entry': entry,
              'word': match.group(0)
            }
    return None

  # format a message to be sent to the user
  def format(self, match):
    message = match['message']
    response = match['category']['response']
    suggestions = match['entry']['suggestions']
    word = match['word']

    user = message.get('user')
    message_text = message.get('text')

    # if the message is multiple lines, reduce the message text
    # to be quoted to only the line containing the matching word
    # TODO: replace by linking / sharing the original message
    # to the user
    lines = message_text.split('\n')
    if len(lines) > 1:
      for l in lines:
        if word in l: # TODO replace by fancy
          message_text = l
          break

    formatted = "Hey <@{}>, I noticed you said:\n".format(user)
    formatted += "> {}\n".format(message_text) # quoted message they sent
    formatted += "{}\n\n".format(response) # explanation of why the word is harmful
    formatted += "Instead of _'{}'_, try some of the following examples:\n".format(word)
    formatted += "* {}".format('\n* '.join(suggestions))
    return formatted
