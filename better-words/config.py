from os import environ

SLACK_BOT_TOKEN = environ['SLACK_BOT_TOKEN']

SLACK_VERIFICATION_TOKEN = environ['SLACK_VERIFICATION_TOKEN']

if 'PORT' in environ:
	PORT = environ['PORT']
else:
	PORT = 3000
