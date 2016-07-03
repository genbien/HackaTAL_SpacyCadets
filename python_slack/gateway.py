from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import Bot
import inspect
import os, sys
import re
import redis
import json
import time

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PASS = os.environ['REDIS_PASS']

if REDIS_HOST is None or REDIS_PASS is None:
  print("Environment variables REDIS_HOST and REDIS_PASS must be set")
  sys.exit()

## Slack -> Redis

r = redis.StrictRedis(host=REDIS_HOST, password=REDIS_PASS)

@listen_to('.*', re.IGNORECASE)
def forward_to_gateway(message):
    text = message.body['text']
    user = message.channel._client.users[message.body['user']][u'name']
    chan = message.channel._client.channels[message.body['channel']][u'name']

    data = json.dumps({'user': user, 'text': text, 'chan': chan})
    print('Debug: listen_to', data);
    r.publish('incoming', data);

    message.react('+1')

## Redis -> Slack

# Steal slack client instance like it's the 4th of july
# https://github.com/gpailler/AtlassianBot/blob/a15c87a62f2b152444a278142832b22e0fe7a3b5/plugins/jira.py#L320
def __get_client():
    stack = inspect.stack()
    for frame in [f[0] for f in stack]:
        if 'self' in frame.f_locals:
            instance = frame.f_locals['self']
            if isinstance(instance, Bot):
                return instance._client
slack_client = __get_client()

def __get_channel(channelname):
    for id, channel in list(slack_client.channels.items()):
        if channel.get('name', None) == channelname:
            return id

def handle_outgoing(message):
    print('Debug: outgoing', message);
    if (message and message['data']):
        if (isinstance(message['data'], bytes)):
            data = message['data'].decode("utf-8");
        elif (isinstance(message['data'], str)):
            data = message['data']

        data = json.loads(data)
        chan = data['chan']
        text = data['text']
        slack_client.send_message(__get_channel(chan), text)

p = r.pubsub()
p.subscribe(**{'outgoing': handle_outgoing})
thread = p.run_in_thread(sleep_time=0.001)

