import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `from grovepi import *`
sys.path.append('../../Software/Python/')

#from grovepi import *

import grovepi
#use UDP
import socket

def Main():
    # Change the host and port as needed. For ports, use a number in the 9000 
    # range. 
    host = '192.168.1.168'
    port = 8000

    server_addr = '192.168.1.248'

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    s.bind((host,port))

    # Connect the Grove Ultrasonic Ranger to digital port D4
    # SIG,NC,VCC,GND
    ultrasonic_ranger = 3

    # UDP is connectionless, so a client does not formally connect to a server
    # before sending a message.
    dst_port = input("destination port-> ")
    message = str(grovepi.ultrasonicRead(ultrasonic_ranger))
    while message != 'q':
        #tuples are immutable so we need to overwrite the last tuple
        server = (server_addr, int(dst_port))

        # for UDP, sendto() and recvfrom() are used instead
        s.sendto(message.encode('utf-8'), server) 
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("Received from server: " + data)
        dst_port = input("destination port-> ")
        try:
	    # Read distance value from Ultrasonic
            message = str(grovepi.ultrasonicRead(ultrasonic_ranger))

        except TypeError:
	    print ("Error")
	except IOError:
	    print ("Error")
    
    s.close()

if __name__ == '__main__':
    Main()


