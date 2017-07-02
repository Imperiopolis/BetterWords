from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
import os
import yaml

with open("words.yml", 'r') as stream:
    try:
        WORDS = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        # TODO: ??????
        exit

# Our app's Slack Event Adapter for receiving actions via the Events API
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
slack_events_adapter = SlackEventAdapter(SLACK_VERIFICATION_TOKEN, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
CLIENT = SlackClient(SLACK_BOT_TOKEN)

# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    user = message["user"]
    message_text = message.get('text')

    if message.get("subtype") is None:
        response = get_response(user, message_text)
        if response:
            CLIENT.api_call("chat.postMessage", channel=user, text=message_text, as_user="better_words")
            CLIENT.api_call("chat.postMessage", channel=user, text=response, as_user="better_words")

def get_response(user, message_text):
    for entry in WORDS:
        for word in entry['words']:
            if word in message_text: # TODO replace by fancy
                return format_message(user, message_text, word, entry)
    return ''

def format_message(user, message_text, word, entry):
    response = entry['response']
    suggestions = entry['suggestions']
    lines = message_text.split('\n')
    if len(lines) > 1:
        for l in lines:
            if word in l: # TODO replace by fancy
                message_text = l
                break

    to_send = "Hey <@{}>, I noticed you said:\n".format(user)
    to_send += "> {}\n".format(message_text) # quoted message they sent
    to_send += "{}\n\n".format(response) # explanation of why the word is harmful
    to_send += "Instead of _'{}'_, try some of the following examples:\n".format(word)
    to_send += "{}".format(', '.join(suggestions))
    return to_send

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)
