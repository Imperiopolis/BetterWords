from slack_emitter import SlackEventAdapter
from slackclient import SlackClient
from message_parser import MessageParser, format_match
from config import SLACK_BOT_TOKEN, SLACK_VERIFICATION_TOKEN

class EventMonitor(object):
    """A class that monitors for slack events and handles them appropriately"""
    def __init__(self):
        self.slack_client = SlackClient(SLACK_BOT_TOKEN)
        self.message_parser = MessageParser()
        self.slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN)

        # register for the events we care about
        @self.slack_events_adapter.on('message')
        def handle_message(event_data):
            message = event_data['event']

            # we only want to parse basic messages, not bot messages or other special subtypes
            if message.get('subtype') is None:
                match = self.message_parser.is_match(message)
                if match:
                    response = format_match(match)

                    # Send the response text to the user in a private message
                    self.slack_client.api_call('chat.postMessage',
                                               channel=message.get('user'),
                                               text=response,
                                               as_user='better_words')

    def start(self, port=None, debug=False):
        """
        Start the flask server for the slack events adapter

        @param port: The port to run the server on
        @param debug: if True, debug mode will be enabled
        """
        self.slack_events_adapter.start(port=port, debug=debug)
