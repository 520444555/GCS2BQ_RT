import json
import logging

def getfile(message):
	#Decoding message
	message = message.decode('utf-8')
	json_object = json.loads(message)
	#Getting bucket name
	bucket=json_object['bucket']
	#Getting file name
	file_name=json_object['name']
	full_name='gs://'+bucket+'/'+file_name
	#Adding logging
	logging.info('Pubsub file name ------------------: %s ', full_name)
	#Returning full name
	return full_name
