#
# Title:gpio.py
# Description: GPIO wrapper
# Development Environment:OS X 10.9.3/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import os

class gpio:
    gpio_directory = '/sys/class/gpio'

    def __init__(self, port):
        self.port = port

	self.port_directory = "%s/gpio%d" % (self.gpio_directory, self.port)
	if not os.path.isdir(self.port_directory):
		export_file = open("%s/export" % self.gpio_directory, 'w')
		export_file.write(str(port))
		export_file.close()

    def getActiveLowValue(self):
        temp_name = "%s/active_low" % (self.port_directory)
	temp_file = open(temp_name, 'r')
	self.gpio_active_low = int(temp_file.readline())
	temp_file.close()
	return self.gpio_active_low

    def getDirectionValue(self):
        temp_name = "%s/direction" % (self.port_directory)
	temp_file = open(temp_name, 'r')
	self.gpio_direction = temp_file.readline().strip()
	temp_file.close()
	return self.gpio_direction

    def setDirectionValue(self, arg):
        self.gpio_direction = arg
        temp_name = "%s/direction" % (self.port_directory)
	temp_file = open(temp_name, 'w')
	temp_file.write(arg)
	temp_file.close()

    def getEdgeValue(self):
        temp_name = "%s/edge" % (self.port_directory)
	temp_file = open(temp_name, 'r')
	self.gpio_edge = temp_file.readline().strip()
	temp_file.close()
	return self.gpio_edge

    def getGpioValue(self):
        temp_name = "%s/value" % (self.port_directory)
	temp_file = open(temp_name, 'r')
	self.gpio_value = int(temp_file.readline())
	temp_file.close()
	return self.gpio_value

    def setGpioValue(self, arg):
        self.gpio_value = arg
        temp_name = "%s/value" % (self.port_directory)
	temp_file = open(temp_name, 'w')
	temp_file.write(str(arg))
	temp_file.close()

    def toggleGpioValue(self):
        if self.gpio_value < 1:
            self.setGpioValue(1)
        else:
            self.setGpioValue(0)

