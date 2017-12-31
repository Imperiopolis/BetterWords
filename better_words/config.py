from os import environ

SLACK_BOT_TOKEN = environ['SLACK_BOT_TOKEN']

SLACK_VERIFICATION_TOKEN = environ['SLACK_VERIFICATION_TOKEN']

PORT = environ.get('PORT', 3000)
