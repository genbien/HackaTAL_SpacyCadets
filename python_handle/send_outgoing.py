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
p = r.pubsub()
p.subscribe('outgoing')

def re_send(message, chan):
	user = 'cadet'
	text = message
	final_message = json.dumps({'user': user, 'text': text, 'chan': chan})
	r.publish('outgoing', final_message)
