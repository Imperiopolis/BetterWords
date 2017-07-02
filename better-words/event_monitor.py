from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
from message_parser import MessageParser
from os import environ

class EventMonitor(object):
  def __init__(self):
    self.slack_client = SlackClient(environ['SLACK_BOT_TOKEN'])
    self.message_parser = MessageParser()
    self.slack_events_adapter = SlackEventAdapter(environ['SLACK_VERIFICATION_TOKEN'], '/slack/events')

    # register for the events we care about
    @self.slack_events_adapter.on('message')
    def handle_message(event_data):
      message = event_data['event']

      # we only want to parse basic messages, not bot messages or other special subtypes
      if message.get('subtype') is None:
        match = self.message_parser.is_match(message)
        if match:
          response = self.message_parser.format(match)

          # DM the response text to the user
          self.slack_client.api_call('chat.postMessage', channel=message.get('user'), text=response, as_user='better_words')

  def start(self, port=None, debug=False):
    self.slack_events_adapter.start(port=port, debug=debug)
