#! /usr/bin/python
#
# Title:perky_blue.py
# Description:
# Development Environment:OS X 10.9.3/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import gpio

from bluetooth import *

class PerkyBlueServer:

    def toggleLed(self, target):
        print 'toggle'

	if target == 'green':
		print 'green'
		if self.green_led.getGpioValue() < 1:
                    self.green_led.setGpioValue(0)
                else:
                    self.green_led.setGpioValue(1)
	elif target == 'red':
		print 'red'
		if self.red_led.getGpioValue() < 1:
                    self.red_led.setGpioValue(0)
                else:
                    self.red_led.setGpioValue(1)
        elif target == 'yellow':
		print 'yellow'
		if self.yellow_led.getGpioValue() < 1:
                    self.yellow_led.setGpioValue(0)
                else:
                    self.yellow_led.setGpioValue(1)
	else:
		print 'unknown remote command'

    def execute(self):
	self.green_led = gpio.gpio(48)
        self.green_led.setDirectionValue('out')
        self.green_led.setGpioValue(0)

	self.red_led = gpio.gpio(49)
        self.red_led.setDirectionValue('out')
        self.red_led.setGpioValue(0)

	self.yellow_led = gpio.gpio(60)
        self.yellow_led.setDirectionValue('out')
        self.yellow_led.setGpioValue(0)

        service_uuid = "00001101-0000-1000-8000-00805F9B34FB"

        server_sock = BluetoothSocket(RFCOMM)
        server_sock.bind(("", PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        advertise_service(server_sock, "PerkyBlue", service_id = service_uuid, service_classes = [service_uuid, SERIAL_PORT_CLASS], profiles = [SERIAL_PORT_PROFILE])

        print("awaiting RFCOMM connection on channel:%d" % port)

        client_sock, client_info = server_sock.accept()
        print("accepted connection from:", client_info)

        try:
            while True:
                data = client_sock.recv(1024).strip()
                if len(data) == 0: break
                print("received [%s]" % data)
                client_sock.sendall('OK')

                self.toggleLed(data)
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
