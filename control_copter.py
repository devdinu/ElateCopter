# Python libs
import sys
import time
import atexit

# CrazyFlie Specific libs
import crazyflie
import cflib
from cflib import *
from crazyflie import Crazyflie
from keys import *
# from keys import CopterController
# from keys import CopterCommander
from copter_commander import *
# Other Utils for my customization

# Util Methods
def crazyflie_connected(link):
	print("connected...", link)
	fly()


def get_copter_id():	
	cflib.crtp.init_drivers()
	available = cflib.crtp.scan_interfaces()
	for i in available:
	    print "Interface with URI [%s] found and name/comment [%s]" % (i[0], i[1])	
	radio_interfaces = [interface for interface in available if "radio" in interface[0]]
	if radio_interfaces:
		return radio_interfaces[0][0]

def connect_to_copter(id):
	print "Connecting to ", id
	crazyflie = Crazyflie()
	crazyflie.open_link(id)
	return crazyflie

COPTER_HANDLE = None
THRUST_MAX_LIMIT = 50000

# Sample Input
roll    = 0.0
pitch   = 0.0
yawrate = 0
thrust  = 40000 # 10001 to 60000

COPTER_CONTROLLER = CopterCommander()


def initialize():
	global COPTER_CONTROLLER
	gui_manager = GUI_manager(COPTER_CONTROLLER)
	gui_manager.handle_event()	
	# CrazyFlie Specific	


def process():
	print "processing...."
	global COPTER_HANDLE
	print "i hope everyting is perfect"
	cid = get_copter_id()	
	if cid:
		COPTER_HANDLE = connect_to_copter(cid)
		COPTER_HANDLE.connected.add_callback(crazyflie_connected) # connectSetupFinished.add_callback(crazyflie_connected) # is olderones
	else:
		print "No copters found!!!"
	cid = initialize()

def fly():
	global COPTER_HANDLE
	print "how many times its called???? ***"
	COPTER_CONTROLLER.set_commander(COPTER_HANDLE.commander)
	COPTER_HANDLE.close_link()
	print("I am flying....")
	# land()

# def takeoff(crazyflie):
# 	num = 10
# 	cthrust = 30000
# 	# input_to_quit = raw_input()!='q'
# 	while num  and cthrust < THRUST_MAX_LIMIT:
# 		time.sleep(1)
# 		print("flying at limit ", cthrust)
# 		crazyflie.commander.send_setpoint(roll, pitch, yawrate, thrust)
# 		num=num-1
# 		cthrust+=2000


def close_handlers():
	global COPTER_HANDLE
	print("cleanup...")	
	COPTER_HANDLE.close_link()


# Start of the Script
process()

if COPTER_HANDLE:
	print "ch:::" , COPTER_HANDLE
	atexit.register(close_handlers)
	sys.exit(1)

print "main thread ends..."
# if COPTER_HANDLE:
	# close_handlers()
