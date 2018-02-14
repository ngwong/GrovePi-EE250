import sys
import socket
#import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `from grovepi import *`
#sys.path.append('../../Software/Python/')

#from grovepi import *


def Main():
    """127.0.0.1 is the loopback address. Any packets sent to this address will
    essentially loop right back to your machine and look for any process 
    listening in on the port specified."""
    host = '192.168.1.168'
    port = 6000
    #led = 4

    s = socket.socket() #by default, the socket constructor creates an TCP/IPv4 socket
    s.connect((host,port))

    message = input("-> ")
    while message != 'q':
        s.send(message.encode('utf-8')) 
        #1024 is the receive buffer size. It's enough for us, and it's a nice number. 
        data = s.recv(1024).decode('utf-8') 
        print("Received from server: " + data)
        message = input("-> ")
    s.close()

"""This if-statement checks if you are running this python file directly. That 
is, if you run `python3 tcpClient.py` in terminal, this if-statement will be 
true"""
if __name__ == '__main__':
    Main()