from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
from message_parser import is_match, format_match
from config import SLACK_BOT_TOKEN, SLACK_VERIFICATION_TOKEN

class EventMonitor(object):
    """A class that monitors for slack events and handles them appropriately"""
    def __init__(self):
        self.slack_client = SlackClient(SLACK_BOT_TOKEN)
        self.slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN)

        # register for the events we care about
        @self.slack_events_adapter.on('message')
        def handle_message(event_data):
            message = event_data['event']

            # we only want to parse basic messages, not bot messages or other special subtypes
            if message.get('subtype') is None:
                # check if is command, execute if true

                match = is_match(message)
                if match:
                    response = format_match(match)

                    user_info = self.slack_client.api_call('users.info', user=message.get('user'))

                    quote = {
                        'fallback': message.get('text'),
                        'author_name': user_info['user']['name'],
                        'author_icon': user_info['user']['profile']['image_24'],
                        'text': message.get('text'),
                        'footer': 'Posted in <#{}>'.format(message.get("channel")),
                        'ts': message.get('ts')
                    }

                    explanation = {'pretext': response.explanation}

                    # Send the response text to the user in a private message
                    self.slack_client.api_call('chat.postMessage',
                                               channel=message.get('user'),
                                               text=response.intro,
                                               as_user='better_words',
                                               attachments=[quote, explanation])

    def start(self, port=None, debug=False):
        """
        Start the flask server for the slack events adapter

        @param port: The port to run the server on
        @param debug: if True, debug mode will be enabled
        """
        self.slack_events_adapter.start(host='0.0.0.0', port=port, debug=debug)
