import time
import json
import requests
import redis
from send_outgoing import re_send
from request import send_sentence

# Python3 compat
try:
  basestring
except NameError:
  basestring = str


r = redis.StrictRedis(host='faulty.io', port=6379, db=0, password='Hackatal2016')
p = r.pubsub()
p.subscribe('incoming')
while (1):
    message = p.get_message()
    if (message and message['data']):
        if isinstance(message['data'], basestring):
            print(message)
            data = message['data']
        elif isinstance(message['data'], bytes):
            print(message)
            data = message['data'].decode('utf-8');
        else:
            print(message)
            continue
        data = json.loads(data)
        # print(data['text'])
        response = send_sentence(data['text'])
        # response = requests.post('https://api.recast.ai/v1/request', params={'text': data['text'],'language': 'en'}, headers={'Authorization': 'Token e47de569b3ca2bae6475931651f84dea'})
        # print(response)
        if response:
            re_send(response, data['chan'])
        # final_response = json.loads(response.text)
        # re_send(final_response['message'], data['chan'])
        # print(data['text'])
    time.sleep(0.002)
