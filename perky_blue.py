#! /usr/bin/python
#
# Title:perky_blue.py
# Description:
# Development Environment:OS X 10.9.3/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
#import time

from bluetooth import *

import Adafruit_BBIO.GPIO as GPIO

class GpioLed:
    yellowLed = 0
    greenLed = 0
    redLed = 0

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

    def toggleLed(self, led):
        if led == 'green':
            print "green led:%d" % self.greenLed
            if self.greenLed:
                GPIO.output('P9_15', GPIO.LOW)
                self.greenLed = 0
            else:
                GPIO.output('P9_15', GPIO.HIGH)
                self.greenLed = 1
        elif led == 'red':
            print "red led:%d" % self.redLed
            if self.redLed:
                GPIO.output('P9_23', GPIO.LOW)
                self.redLed = 0
            else:
                GPIO.output('P9_23', GPIO.HIGH)
                self.redLed = 1
        elif led == 'yellow':
            print "yellow led:%d" % self.yellowLed
            if self.yellowLed == 1:
                print 'set yellow low'
                GPIO.output('P9_12', GPIO.LOW)
                self.yellowLed = 0
            else:
                print 'set yellow high'
                GPIO.output('P9_12', GPIO.HIGH)
                self.yellowLed = 1
        else:
            print("unknown led:%s" % led)

class PerkyBlueServer:

    def execute(self):
        gpioLed = GpioLed()

        service_uuid = "00001101-0000-1000-8000-00805F9B34FB"

        server_sock = BluetoothSocket(RFCOMM)
        server_sock.bind(("", PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        advertise_service(server_sock, "PerkyBlue", service_id = service_uuid, service_classes = [service_uuid, SERIAL_PORT_CLASS], profiles = [SERIAL_PORT_PROFILE])

        print("awaiting RFCOMM connection on channel %d" % port)

        client_sock, client_info = server_sock.accept()
        print("accepted connection from ", client_info)

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
#    gpioLed = GpioLed()
#    gpioLed.toggleLed('yellow')
#    gpioLed.toggleLed('green')
#    time.sleep(5)
#    gpioLed.toggleLed('yellow')
#    gpioLed.toggleLed('green')
#    time.sleep(5)

    server = PerkyBlueServer()
    server.execute()

print 'stop'
