#! /usr/bin/python
#
# Title:perky_blue.py
# Description:
# Development Environment:OS X 10.9.3/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#

from bluetooth import *

import Adafruit_BBIO.GPIO as GPIO

class GpioLed:
    def __init__(self):
        # yellow
        GPIO.setup("P9_12", GPIO.OUT)
        GPIO.output("P9_12", GPIO.LOW)

        # green
        GPIO.setup("P9_15", GPIO.OUT)
        GPIO.output("P9_15", GPIO.LOW)

        # red 
        GPIO.setup("P9_23", GPIO.OUT)
        GPIO.output("P9_23", GPIO.LOW)

    def toggleGpio(self, gpio):
        if GPIO.input(gpio):
            print "high noted"
            GPIO.output(gpio, GPIO.LOW)
        else:
            print "low noted"
            GPIO.output(gpio, GPIO.HIGH)

    def toggleLed(self, led):
        if led == 'green':
            toggleGpio('P9_15')
        elif led == 'red':
            toggleGpio('P9_23')
        elif led == 'yellow':
            toggleGpio('P9_12')
        else:
            print("unknown led:%s" % led)

class PerkyBlueServer:

    def execute(self):

        
        service_uuid = "00001101-0000-1000-8000-00805F9B34FB"

        server_sock = BluetoothSocket(RFCOMM)
        server_sock.bind(("", PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        advertise_service(server_sock, "PerkyBlue", service_id = service_uuid, service_classes = [uuid, SERIAL_PORT_CLASS], profiles = [SERIAL_PORT_PROFILE])

        print("awaiting RFCOMM connection on channel %d" % port)

        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)

        gpioLed = GpioLed()

        try:
            while True:
                data = client_sock.recv(1024)
                if len(data) == 0: break
                print("received [%s]" % data)
                client_sock.sendall('OK')

                gpioLed.toggleLed(data)
        except IOError:
            pass

        print("disconnected")

        client_sock.close()
        server_sock.close()
        print("all done")


print 'start'

#
if __name__ == '__main__':
    server = PerkyBlueServer()
    server.execute()

print 'stop'
