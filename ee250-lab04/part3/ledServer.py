import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `from grovepi import *`
sys.path.append('../../Software/Python/')

from grovepi import *
import time
import socket

# Connect the Grove LED to digital port D2
led = 2

def Main():
    host = '192.168.1.168'
    port = 6000

    s = socket.socket()
    s.bind((host,port))

    s.listen(1)
    c, addr = s.accept()
    print("Connection from: " + str(addr))
    while True:
        data = c.recv(1024).decode('utf-8')
        if not data:
            break
        print("From connected user: " + data)
        data = data.upper()

        if (data == "LED_ON"): 
            try:
                digitalWrite(led,1)		# Send HIGH to switch on LED
                data = "LED is now ON!"
            except IOError:	# Print "Error" if communication error encountered
                print ("Error")

        elif (data == "LED_OFF"):
            try:
                digitalWrite(led,0)
                data = "LED is now OFF"
            except: IOError:
                print("Error");
        else:
            data = "Error: Resend Message"

        print("Sending: " + data)
        c.send(data.encode('utf-8'))
    c.close()

if __name__ == '__main__':
    Main()
