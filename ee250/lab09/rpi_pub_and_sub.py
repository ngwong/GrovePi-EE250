# Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
from grovepi import *
import grovepi

from grove_rgb_lcd import *

led = 3
humidity_temperature = 7

led_status = 0

def on_connect(client, userdata, flags, rc):
	print("Connected to server (i.e., broker) with result code "+str(rc))

	client.subscribe("anrg-pi10/led")
	client.message_callback_add("anrg-pi10/led", custom_callback_led)

	client.subscribe("anrg-pi10/lcd")
	client.message_callback_add("anrg-pi10/lcd", custom_callback_lcd)
	#subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
	print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#Custom callbacks need to be structured with three args like on_message()
def custom_callback_led(client, userdata, message):
	#the third argument is 'message' here unlike 'msg' in on_message
	global led_status # use the global variable so state change can be tracked
	convMessage = str(message.payload, "utf-8") #converts massage payload from byte string to string
	if ("LED_toggle" in convMessage): #checks payload if the LED needs to be toggled
		try:
			led_status = 1 if led_status is 0 else 0
			digitalWrite(led, led_status)  #toggles LED
		except IOError:
			print ("Error")

	print("custom_callback_led: " + message.topic + " " + convMessage)
	print("custom_callback_led: message.payload is of type " + 
		  str(type(message.payload)))

def custom_callback_lcd(client, userdata, message):
	convMessage2 = str(message.payload, "utf-8") #converts message payload from byte string to string
	setText(convMessage2)#prints onto LED board


if __name__ == '__main__':
	#this section is covered in publisher_and_subscriber_example.py
	client = mqtt.Client()
	client.on_message = on_message
	client.on_connect = on_connect
	client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
	client.loop_start()

	while True:  
		# Storing the humidity and temperature data
		[humidity, temperature] = dht(humidity_temperature, 0)

		# Publishing the data to the MQTT server
		client.publish("anrg-pi10/temperature", str(temperature) + " C")
		client.publish("anrg-pi10/humidity", str(humidity) + "%")

		time.sleep(1) #timer so that ultrasonic only sends every second