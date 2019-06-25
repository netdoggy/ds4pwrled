#!/usr/bin/env python3
import glob
import time
import re
import os.path

class ds4control(object):
	device_path = None
	device_led_path = None
	default_led_colors = None
	
	def get_capacity(self):
		return self._device_read('/capacity')
	def get_charge_status(self):
		return self._device_read('/status')

	def R(self, value=None):
		return self.led('red/brightness', value)

	def G(self, value=None):
		return self.led('green/brightness', value)
		
	def B(self, value=None):
		return self.led('blue/brightness', value)

	def RGB(self, R=None,G=None,B=None):
		return [self.R(R),self.G(G),self.B(B)]
		
	def GL(self, value=None):
		return self.led('global/brightness', value)
		
	def led(self, led_name, value=None):
		path = ':' + led_name
		if value is not None:
			self._led_write(path, value)
		return self._led_read(path)

	def led_trigger(self, name, value=None, view_full = False):
		string = self.led(name + '/trigger', value)

		# re-read if value set
		if (value is not None):
			string = self.led(name + '/trigger')

		if (view_full):
			return string

		m = re.search('\[(.*?)\]+', string)
		return m.group(1)


	def _led_read(self, rel_path):
		if not os.path.isfile(self.device_led_path+ rel_path):
			raise Exception("Led file not found '" + rel_path + "'")
		return open(self.device_led_path + rel_path, 'r').read().rstrip()

	def _led_write(self,rel_path, value):
		if not os.path.isfile(self.device_led_path + rel_path):
			raise Exception("Led file not found")
		return open(self.device_led_path + rel_path, 'w').write(str(value))

	def _device_read(self, rel_path):
		if not os.path.isfile(self.device_path + rel_path):
			raise Exception("Device file not found '" + rel_path + "'")

		return open(self.device_path + rel_path, 'r').read().rstrip()
	def _device_write(self, rel_path, value):
		if not os.path.isfile(self.device_path + rel_path):
			raise Exception("Device file not found")

		return open(self.device_path + rel_path, 'w').write(str(value))

	def init_leds(self):
		# try to find ds4 leds
		path_led = glob.glob( self.device_path + '/device/leds/' + '*:global')[0]
		self.device_led_path = path_led.replace(":global", "")
		if os.path.isdir(self.device_led_path + ':red') == False:
			raise Exception ("Device LEDs search error") 
		pass
	def check_online(self):
		return os.path.isdir(self.device_path)

	def __init__(self, path):
		self.device_path = path		
		self.init_leds()
		self.default_led_colors = self.RGB()

		print("Init DS4 PwrLed", self.device_path)
		print(" Capacity:", self.get_capacity())
		print(" Bat Status:", self.get_charge_status())
		
 	
	def get_devices(path="/sys/class/power_supply/*"):
		paths = glob.glob(path)
		for device_path in paths:
			if device_path.__contains__("sony_controller_battery_dc"):
				yield device_path


device_list = {}
def ds4check (path):
	try:
		dev = device_list[path]
	except KeyError as ex:
		dev = device_list[path] = ds4control(path)

	if not dev.check_online():
		return

	dev.init_leds()
	capacity = int(dev.get_capacity())
	status = dev.get_charge_status()

	# > 30%
	if capacity > 30 and status == "Discharging":
		#print (">30%", dev.RGB())
		if dev.led_trigger('red') == 'heartbeat':
			 dev.led_trigger('red', 'none')

		if dev.RGB() != [0,0,10]:
			dev.RGB(0,0,10)
	# <= 30%
	elif (capacity <= 30 and capacity > 10 and status == "Discharging"):
		#print ("<=30%", dev.RGB())
		if dev.led_trigger('red') != 'none':
			 dev.led_trigger('red', 'none')

		if dev.RGB() != [1,0,5]:
			dev.RGB(1,0,5)
		
	# <= 10% / low bat
	elif (capacity <= 10 and status == "Discharging"):
		#print ("<10%", dev.RGB())#
		if dev.led_trigger('red') != 'heartbeat':
			dev.led_trigger('red', 'heartbeat')
			dev.RGB(16, 0, 0)
	

	elif (status == "Charging"):
		#print ("<=* charging", dev.RGB())
		dev.RGB(5,1,1)
		if dev.led_trigger('red') != 'timer':
			dev.led_trigger('red', 'timer')
	else:
		pass
		

while True:
	devices = ds4control.get_devices()
	for dev in devices:
		ds4check (dev)
		time.sleep(1)
