from redis import StrictRedis as sr
import os
import json
from multiprocessing import Process as pr, Queue as qu
import time
import re
import datetime

#constructor to create redis connection. localhost is default for redis database
# A parameter has to be passed in for the port since we dealing with different instances of redis
#Default port will be 6379


class RedisConnect:
	def __init__(self, host='localhost', port=6379):
		self.port = port
		self.host = host
		self.redis = sr(host=self.host, port=self.port, decode_responses=True)

		self.p = self.redis.pubsub()
		self.p.subscribe('__keyspace@0__*')

		print('subscribed to  redis instance {}'.format(self.port))


def snort_log_fetch(redis_fetched_queue_snort):
	rc = RedisConnect(host='localhost', port=6379)
	# create an empty dict for comparisons.
	#Will be global to the loops
	pointer_data = dict()

	while True:
		try:
			#Listen for KA events.
			message = rc.p.get_message()

			if message and message['data'] == 'set':
			 # Obtain the key from the redis emmitted event if the event is a set event
			 # the format emmited by redis is in a dict form # the key is the value to the key 'channel'
			 # The key is in '__keyspace@0__*' form # obtain the last field of the list returned by split function

				key = message['channel'].split('__:')[-1]
				data_redis = json.loads((rc.redis.get(key)).replace("'", "\""))
				#first of, check the current json data and see if its 'sec' value is same
        		#that is the last in the accumulated data list
        		#if it is the same, increase time_count by one else pop that value

				if pointer_data.empty():

					pointer_data = data_redis.copy()
					pointer_data.setdefault('time_count', 1)
					# if pointer_data is not empty, compare the sec fields.
        			# If they are same, increase time_count
        			# Else push pointer data on the queue and set new pointer_data
					# To the current unmatched value
				else:

					if pointer_data["sec"] == data_redis["sec"]:
						pointer_data["time_count"] += 1

					else:
						redis_fetched_queue_snort.put(pointer_data)
      					#print(pointer_data)
        				#Empty pointer_data
						pointer_data.clear()
						pointer_data = data_redis.copy()
        				#Set pointer data to new value received
						
      					#pointer_data=data_redis.copy()
        				#set a new key-value field for time-count
						pointer_data.setdefault('time_count', 1)

        			# If not message is recieved, the process needs to rest a while
			else:

				time.sleep(1)

		except Exception as e:
			print('Redis'+port, e)
			continue

	# first of, check the current json data and see if its 'sec' value is same
    # that is the last in the accumulated data list
    # if it is the same, increase time_count by one else pop that value


def sys_monitor_fetch(redis_fetched_queue_sys):
	rc = RedisConnect(host='localhost', port=6380)
	# create an empty dict for comparisons; will be global to the for loops
	current_data = dict()

	while True:
		try:
			# Listen for KA Events
			monitor_message = rc.p.get_message()

			if monitor_message and monitor_message['data'] == 'set':
				# Obtain the key from the redis emmitted event if the event is a set event
				# the format emmited by redis is in a dict form # the key is the value to the key 'channel'
				# The key is in '__keyspace@0__*' form # obtain the last field of the list returned by split function

				key = monitor_message['channel'].split('__:')[-1]
				data_monitor = rc.redis.get(key)
				# the data structure is a nested json object so we need to fetch the value
				#related to the metric key
				sub_data_monitor = json.loads(data_monitor["metric"])

				if not current_data:
					current_data = sub_data_monitor.copy()

				else:
					if current_data["sec"] != sub_data_monitor["sec"]:
					#if they are same; keep checking new logs until they are not same
						redis_fetched_queue_sys.put(current_data)
						print(current_data)
						current_data.clear()
			else:
				time.sleep(0.01)

		except Exception as e:
			print('Redis'+port, e)
			continue


def producer_to_web():
      # create a multiprocess queue for comm b/n this function and the two forked processes
      # a multiprocessing queue for comm b/n sysmonitor and this process
	redis_fetched_queue_sys = qu()

	redis_fetched_queue_snort = qu()
	
	#this function calls two other functions and 
	#creates threads so they appear to run concurr$

	p_snort = pr(target = snort_log_fetch,name ='snort_process',args=(redis_fetched_queue_sys,))
	p_monitor = pr(target = sys_monitor_fetch,name ='sys_monitor_process',args=(redis_fetched_queue_snort,))

     
	p_snort.start()
	p_monitor.start()
	
	redis_web = RedisConnect(host='localhost',port=6381)

	while True:
    
    	#if not redis_fetched_queue_sys.empty() or redis_fetched_queue_snort.empty()
		processed_logs = {
					'snort': redis_fetched_queue_snort.get() if not redis_fetched_queue_snort.empty() else None,
					'sys_monitor':redis_fetched_queue_sys.get() if not redis_fetched_queue_sys.empty() else None
			}

		time= datetime.datetime.now()

		seq = re.sub(r"[^a-zA-Z0-9]","",str(time))

		send_data = json.dumps(processed_logs)
		
		redis_web.redis.setex(seq,'30',send_data)







    #process_snort.join()
    #process_sys_monitor.join()



def main():
	producer_to_web()


if __name__== "__main__":
	main()






