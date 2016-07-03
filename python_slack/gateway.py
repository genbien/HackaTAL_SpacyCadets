from slackbot.bot import respond_to
from slackbot.bot import listen_to
import os, sys
import re
import redis
import json

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PASS = os.environ['REDIS_PASS']

if REDIS_HOST is None or REDIS_PASS is None:
  print("Environment variables REDIS_HOST and REDIS_PASS must be set")
  sys.exit()

r = redis.StrictRedis(host=REDIS_HOST, password=REDIS_PASS)

@listen_to('.*', re.IGNORECASE)
def forward_to_gateway(message):
    # pprint.pprint('Forwarding %s' % message.body)
    text = message.body['text']
    user = message.channel._client.users[message.body['user']][u'name']
    chan = message.channel._client.channels[message.body['channel']][u'name']

    data = json.dumps({'user': user, 'text': text, 'chan': chan})
    print('Debug: listen_to', data);
    r.publish('incoming', data);

    message.react('+1')
    # message.reply('```'+data+'```');


# @respond_to('.*', re.IGNORECASE)
# def forward_to_gateway(message):
#     text = message.body['text']
#     user = message.channel._client.users[message.body['user']][u'name']
#     chan = message.channel._client.channels[message.body['channel']][u'name']

#     data = json.dumps({'user': user, 'text': text, 'chan': chan})
#     print('Debug: respond_to', data);
#     r.publish('incoming', data);

#     message.react('+1')
#     message.reply('```'+data+'```');
