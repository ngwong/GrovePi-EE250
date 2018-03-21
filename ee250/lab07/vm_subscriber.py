"""EE 250L Lab 07 Skeleton Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time

#ultrasonic = ""

def on_connect(client, userdata, flags, rc): #sets up where to subscribe to
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("anrg-pi10/ultrasonicRanger") #subscribes to specific channel
    client.message_callback_add("anrg-pi10/ultrasonicRanger", custom_callback_ultrasonic) #adds where to pass info to

    client.subscribe("anrg-pi10/button")#subsrcibes to specific channel
    client.message_callback_add("anrg-pi10/button", custom_callback_button) #adds where to pass info to
    #subscribe to the ultrasonic ranger topic here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

<<<<<<< HEAD
#Custom callbacks need to be structured with three args like on_message()
def custom_callback_ultrasonic(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    ultrasonic = str(message.payload, "utf-8") #converts message payload into str from byte string
    print("custom_callback_ultrasonic: " + message.topic + " " + ultrasonic)
    print("custom_callback_ultrasonic: message.payload is of type " + 
          str(type(message.payload)))

def custom_callback_button(client, userdata, message):
#callback for button press info
    convMessage = str(message.payload, "utf-8") #converts bit str to string
    print(convMessage) #prints message

=======
>>>>>>> upstream/sp18-master
if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        True #loop nescessary to keep program running
        #print('\n')
        #time.sleep(1)
            

