import paho.mqtt.client as mqtt
import time

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

AVERAGE_SIZE = 10

ranger1_average = []
ranger2_average = []

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
	ranger1_average.append(sum(ranger1_dist[-AVERAGE_SIZE])/AVERAGE_SIZE)
	ranger1_average = ranger1_average[-MAX_LIST_LENGTH]

# This updates the moving average buffer so the newest element 
# is the average of the last AVERAGE_SIZE of ranger1
def update_average_ranger2():
	ranger2_average.append(sum(ranger2_dist[-AVERAGE_SIZE])/AVERAGE_SIZE)
	ranger2_average = ranger2_average[-MAX_LIST_LENGTH]


def calc_change(list):
	# TODO. Convert a list of size n to a list of the difference of the adjacent positions of size n - 1

if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_hostname, broker_port, 60)
    client.loop_start()

    while True:
        """ You have two lists, ranger1_dist and ranger2_dist, which hold a window
        of the past MAX_LIST_LENGTH samples published by ultrasonic ranger 1
        and 2, respectively. The signals are published roughly at intervals of
        200ms, or 5 samples/second (5 Hz). The values published are the 
        distances in centimeters to the closest object. Expect values between 
        0 and 512. However, these rangers do not detect people well beyond 
        ~125cm. """
        
        # TODO: detect movement and/or position
        
        print("ranger1: " + str(ranger1_dist[-1:]) + ", ranger2: " + str(ranger2_dist[-1:])) 
        
        print("ranger1_average: ") + str(ranger1_average[-1] + ", ranger2_average: " + str(ranger2_average[-1]))

        time.sleep(0.2)