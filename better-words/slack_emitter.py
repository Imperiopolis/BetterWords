from pyee import EventEmitter
from slackeventsapi import SlackServer

# This file is copied from
# https://github.com/slackapi/python-slack-events-api/blob/master/slackeventsapi/__init__.py
# because we need to set the host to something it wouldn't support

class SlackEventAdapter(EventEmitter):
    # Initialize the Slack event server
    # If no endpoint is provided, default to listening on '/slack/events'
    def __init__(self, verification_token, endpoint="/slack/events"):
        EventEmitter.__init__(self)
        self.verification_token = verification_token
        self.server = SlackServer(verification_token, endpoint, self)

    def start(self, host='0.0.0.0', port=None, debug=False):
        self.server.run(host=host, port=port, debug=debug)
