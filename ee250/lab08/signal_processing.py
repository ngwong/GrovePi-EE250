import paho.mqtt.client as mqtt
import time
import requests
import json
from datetime import datetime

# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000
ultrasonic_ranger1_topic = "ultrasonic_ranger1"
ultrasonic_ranger2_topic = "ultrasonic_ranger2"

# Lists holding the ultrasonic ranger sensor distance readings. Change the 
# value of MAX_LIST_LENGTH depending on how many distance samples you would 
# like to keep at any point in time.
MAX_LIST_LENGTH = 100
ranger1_dist = []
ranger2_dist = []

AVERAGE_SIZE = 5

ranger1_average = [0] * AVERAGE_SIZE
ranger2_average = [0] * AVERAGE_SIZE

STATIONARY_MARGIN = 30
DIRECTIONAL_MARGIN = 100


def ranger1_callback(client, userdata, msg):
    global ranger1_dist
    ranger1_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]
    update_average_ranger1()

def ranger2_callback(client, userdata, msg):
    global ranger2_dist
    ranger2_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]
    update_average_ranger2()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(ultrasonic_ranger1_topic)
    client.message_callback_add(ultrasonic_ranger1_topic, ranger1_callback)
    client.subscribe(ultrasonic_ranger2_topic)
    client.message_callback_add(ultrasonic_ranger2_topic, ranger2_callback)

# The callback for when a PUBLISH message is received from the server.
# This should not be called.
def on_message(client, userdata, msg): 
    print(msg.topic + " " + str(msg.payload))

# This updates the moving average buffer so the newest element 
# is the average of the last AVERAGE_SIZE of ranger1
def update_average_ranger1():
	global ranger1_average
	ranger1_average.append(sum(ranger1_dist[-AVERAGE_SIZE:])/AVERAGE_SIZE)
	ranger1_average = ranger1_average[-MAX_LIST_LENGTH:]

# This updates the moving average buffer so the newest element 
# is the average of the last AVERAGE_SIZE of ranger1
def update_average_ranger2():
	global ranger2_average
	ranger2_average.append(sum(ranger2_dist[-AVERAGE_SIZE:])/AVERAGE_SIZE)
	ranger2_average = ranger2_average[-MAX_LIST_LENGTH:]

# Convert a list of size n to a list of the difference of the adjacent positions of size n - 1
def calc_change(avg_list):
	change_list = [0] * (len(avg_list) - 1)
	for i in range(0, len(avg_list) - 1):
		change_list[i] = avg_list[i] - avg_list[i + 1]
	return change_list

def msg_direction(avg_list_ranger1, avg_list_ranger2):
	avg_ranger1 = sum(avg_list_ranger1)/len(avg_list_ranger1)
	avg_ranger2 = sum(avg_list_ranger2)/len(avg_list_ranger2)

	tot_ranger1 = sum(calc_change(avg_list_ranger1))/len(avg_list_ranger1)
	tot_ranger2 = sum(calc_change(avg_list_ranger2))/len(avg_list_ranger2)

	print ("average ranger 1: " + str(avg_list_ranger1) + ", average ranger 2: " + str(avg_list_ranger2))
	print ("total ranger 1: " + str(tot_ranger1) + ", total ranger 2: " + str(tot_ranger2))

	if (abs(tot_ranger1 + tot_ranger2) < STATIONARY_MARGIN):
		if(avg_ranger1 > avg_ranger2 + DIRECTIONAL_MARGIN):
			return "Still - Right"
		elif (avg_ranger2 > avg_ranger1 + DIRECTIONAL_MARGIN):
			return "Still - Left"
		else:
			return "Still - Middle"
	else:
		if ((tot_ranger1 < -STATIONARY_MARGIN) or (tot_ranger2 > STATIONARY_MARGIN)):
			return "Moving Right"
		elif ((tot_ranger1 > STATIONARY_MARGIN) or (tot_ranger2 < -STATIONARY_MARGIN)):
			return "Moving Left"
		else:
			return "Can't tell"

if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_hostname, broker_port, 60)
    client.loop_start()

    # This header sets the HTTP request's mimetype to `application/json`. This
    # means the payload of the HTTP message will be formatted as a json ojbect
    hdr = {
        'Content-Type': 'application/json',
        'Authorization': None #not using HTTP secure
    }

    # The payload of our message starts as a simple dictionary. Before sending
    # the HTTP message, we will format this into a json object
    payload = {
        'time': str(datetime.now()),
        'event': msg_direction(ranger1_average[-AVERAGE_SIZE:], ranger2_average[-AVERAGE_SIZE:])
    }

    while True:
        """ You have two lists, ranger1_dist and ranger2_dist, which hold a window
        of the past MAX_LIST_LENGTH samples published by ultrasonic ranger 1
        and 2, respectively. The signals are published roughly at intervals of
        200ms, or 5 samples/second (5 Hz). The values published are the 
        distances in centimeters to the closest object. Expect values between 
        0 and 512. However, these rangers do not detect people well beyond 
        ~125cm. """

        # Send an HTTP POST message and block until a response is given.
        # Note: requests() is NOT the same thing as request() under the flask 
        # library.
        response = requests.post("http://0.0.0.0:5000/post-event", headers = hdr,
                                 data = json.dumps(payload))

        # Print the json object from the HTTP response
        print(response.json())
        
        # print("ranger1: " + str(ranger1_dist[-1:]) + ", ranger2: " + str(ranger2_dist[-1:])) 
        
        # print("ranger1_average: " + str(ranger1_average[-1:]) + ", ranger2_average: " + str(ranger2_average[-1:]))

        print(msg_direction(ranger1_average[-AVERAGE_SIZE:], ranger2_average[-AVERAGE_SIZE:]))

        time.sleep(0.2)