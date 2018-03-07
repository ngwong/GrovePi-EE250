"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
from grovepi import *

led = 6
ultra = 5

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload))

#Custom callbacks need to be structured with three args like on_message()
def custom_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    if (str(message.payload) == "LED_ON"):
        try:
            digitalWrite(led, 1)
        except IOError:
            print ("Error")
    elif (str(message.payload) == "LED_OFF"):
        try:
            digitalWrite(led, 0)
        except IOError:
            print ("Error")

    print("custom_callback: " + message.topic + " " + str(message.payload))
    print("custom_callback: message.payload is of type " + 
          str(type(message.payload)))


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    client.subscribe("anrg-pi10/led")
    client.message_callback_add("anrg-pi10/led", custom_callback)

    while True:
        
        #print("delete this line")
        time.sleep(1)