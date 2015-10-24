from gui_manager import *

# UP & Down - Thrust
# Left & Right - Roll

# some sample tests
# W,S - pitch
# A,D - yaw

class CopterController():

	def __init__(self, handle):
		self.copter_commander = handle

	# def keyboard_control(self, gui):
	# 	gui.handle_event(self.copter_commander)

