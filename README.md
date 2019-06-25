# ds4pwrled
Simple DualShock4 (DS4) daemon for displaying the level of the battery charge on the joystick LED for Linux/Pi3/RetroPie

# Installation

Copy ds4pwrled.py file to /home/pi/ds4pwrled.py
and add line  to /etc/rc.local
```
sudo python3 /home/pi/ds4pwrled.py  &
```

# work algorithm
```
if capacity > 30 and status == "Discharging":
  // Reduces the brightness of the LED from 64 (default) to 10 to reduce power consumption
  led.RGB(0,0,10)
	
if capacity <= 30 and capacity > 10 and status == "Discharging"):
 // adds red
 led.RGB(1,0,5)
		
if (capacity <= 10 and status == "Discharging"):
  dev.RGB(16, 0, 0) blinking red as heartbeat
	
if (status == "Charging"):
  dev.RGB(5,1,1) / red blinking by timer
```

Enjoy

# Reference 
https://github.com/RetroPie/RetroPie-Setup/wiki/PS4-Controller
https://wiki.gentoo.org/wiki/Sony_DualShock
https://github.com/torvalds/linux/blob/master/drivers/hid/hid-sony.c
https://www.psdevwiki.com/ps4/DualShock_4
