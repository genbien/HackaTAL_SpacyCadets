import time
import redis
import json
import requests
from test import re_send

r = redis.StrictRedis(host='faulty.io', port=6379, db=0, password='Hackatal2016')
p = r.pubsub()
p.subscribe('incoming')
while (1):
	message = p.get_message()
	if (message and message['data'] and isinstance(message['data'], basestring)):
		data = json.loads(message['data'])
		response = requests.post('https://api.recast.ai/v1/request', params={'text': data['text'],'language': 'en'}, headers={'Authorization': 'Token e47de569b3ca2bae6475931651f84dea'})
		print(response.text)
		final_response = json.loads(response.text)
		re_send(final_response['message'], data['chan'])
		# print(data['text'])
	time.sleep(0.2)
