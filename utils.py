# Python libs
import sys
import time
import atexit

sys.path.append("/Users/dineshkumar/Documents/Learn/CrazyFlie/cfclient-2013.4.2/lib")
sys.path.append("/Users/dineshkumar/Documents/Learn/CrazyFlie/cfclient-2013.4.2/lib/cflib")

# CrazyFlie Specific libs
import crazyflie
import cflib
from cflib import *
from crazyflie import *

# Other Utils for my customization

import pygame
from pygame.locals import *

# Util Methods
def crazyflie_connected(link):
	print("connected...", link)
	fly()

def connect_finished(link):
	fly()
	print("connection finised...", link)

#Constants 
CRAZYFLY_ID = "radio://0/6/250K"

roll    = 0.0
pitch   = 0.0
yawrate = 0
thrust  = 40000 # 10001 to 60000

THRUST_MAX_LIMIT = 20000


def initialize():
	cflib.crtp.init_drivers()
	available = cflib.crtp.scan_interfaces()

	for i in available:
	    print "Interface with URI [%s] found and name/comment [%s]" % (i[0], i[1])

def connect_to_copter(id):
	crazyflie = Crazyflie()
	crazyflie.open_link(id)
	crazyflie.connected.add_callback(crazyflie_connected)
	crazyflie.connectSetupFinished.add_callback(connect_finished)
	return crazyflie

CONNECTED_COPTER = None

def process():
	global CONNECTED_COPTER 
	initialize()	
	CONNECTED_COPTER = connect_to_copter(CRAZYFLY_ID)
	# need to set it globally and called in fly
	# takeoff(cf)

def patience(seconds):
	print("sleeping...")
	time.sleep(seconds)

def fly():
	takeoff(CONNECTED_COPTER)
	print("I am flying....")
	# land()

def takeoff(crazyflie):
	num = 3000
	cthrust = 50000
	while num:
		time.sleep(1)
		print("flying at limit ", cthrust)
		crazyflie.commander.send_setpoint(roll, pitch, yawrate, thrust)
		num=num-1
		cthrust+=1000

def land():
	curr_thrust = THRUST_MAX_LIMIT
	while num:
		crazyflie.commander.send_setpoint(roll, pitch, yawrate, thrust)
		num=num-1

def close_handlers():
	print("cleanup...")	
	crazyflie.close_link()


# Start of the Script
process()
atexit.register(close_handlers)
patience(10)
