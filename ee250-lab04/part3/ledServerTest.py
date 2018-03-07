import sys
import socket
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `from grovepi import *`
sys.path.append('../../Software/Python/')

from grovepi import *

# use TCP



def Main():
    host = '127.0.0.1'
    port = 5000

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
        if data == "LED_ON":
        	try:
		        #Blink the LED
		        digitalWrite(led,1)		# Send HIGH to switch on LED
		        print ("LED ON!")
		        time.sleep(1)
		    except KeyboardInterrupt:	# Turn LED off before stopping
	        	digitalWrite(led,0)
	        	break
		    except IOError:				# Print "Error" if communication error encountered
		        print ("Error")
		else if data == "LED_OFF":
			try:
				#Turn off the LED
				digitalWrite(led,0)		# Send LOW to switch off LED
		        print ("LED OFF!")
		        time.sleep(1)
		    except KeyboardInterrupt:
		    	digitalWrite(led,0)
		    	break
		   	except IOError:
		   		print("Error")
		else:
			print("Oops something went wrong")
			
        data = data.upper()
        print("Sending: " + data)
        c.send(data.encode('utf-8'))
    c.close()

if __name__ == '__main__':
    Main()