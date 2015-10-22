# Python libs
import sys
import time

sys.path.append("/Users/dineshkumar/Documents/Learn/CrazyFlie/cfclient-2013.4.2/lib")
sys.path.append("/Users/dineshkumar/Documents/Learn/CrazyFlie/cfclient-2013.4.2/lib/cflib")

# CrazyFlie Specific libs
import crazyflie
import cflib
from cflib import *
from crazyflie import *

# Util Methods
def crazyflie_connected(link):
	print("connected...", link)
	fly()

def connect_finished(link):
	fly()
	print("connection finised...", link)

#Constants 

CRAZYFLY_ID = "radio://0/6/250K"

cflib.crtp.init_drivers()
available = cflib.crtp.scan_interfaces()

for i in available:
    print "Interface with URI [%s] found and name/comment [%s]" % (i[0], i[1])

crazyflie = Crazyflie()

crazyflie.open_link(CRAZYFLY_ID)
crazyflie.connected.add_callback(crazyflie_connected)
crazyflie.connectSetupFinished.add_callback(connect_finished)

roll    = 0.0
pitch   = 0.0
yawrate = 0
thrust  = 40000 # 10001 to 60000

THRUST_MAX_LIMIT = 40000

def patience():
	print("sleeping...")
	time.sleep(8)

def fly():
	takeoff()
	print("I am flying....")
	land()

def takeoff():
	num = 3000
	cthrust = 0
	while num:
		crazyflie.commander.send_setpoint(roll, pitch, yawrate, thrust)
		num=num-1
		cthrust+=1

def land():
	curr_thrust = THRUST_MAX_LIMIT
	while num:
		crazyflie.commander.send_setpoint(roll, pitch, yawrate, thrust)
		num=num-1

patience()
crazyflie.close_link()