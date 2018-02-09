import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `from grovepi import *`
sys.path.append('../../Software/Python/')

from grovepi import *
import grovepi
import socket

#use UDP

def Process1():
    # Change the host and port as needed. For ports, use a number in the 9000 
    # range. 
    host = '192.168.1.168'
    port = 9000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))

    print("Process 1 Server Started")
    while True:
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("Message From: " + str(addr))
        print("From connected user: " + data)
        data = data.upper()
        print("Sending: " + data)
        s.sendto(data.encode('utf-8'), addr)
    c.close()

if __name__ == '__main__':
    Process1()

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 3

while True:
    try:
        # Read distance value from Ultrasonic
        print(grovepi.ultrasonicRead(ultrasonic_ranger))

    except TypeError:
        print ("Error")
    except IOError:
        print ("Error")
