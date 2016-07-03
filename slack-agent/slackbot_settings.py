import os, sys

API_TOKEN = os.environ['SLACK_API_TOKEN']

DEFAULT_REPLY = "Sorry but this does not look like a soccer to me."

PLUGINS = [
  # 'slackbot.plugins',
  'gateway',
]

ERRORS_TO = 'bot_errors'