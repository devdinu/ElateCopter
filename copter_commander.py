
class CopterConfigs():
	MAX_THRUST = 70000
	MIN_THRUST = 10000
	MIN_THRUS_TO_TEST = 30000
	MIN_ROLL = MIN_YAW = MIN_PITCH = 0
	# MAX_ROLL =
	# MAX_PITCH
	# MAX_YAW

class CopterCommander():

	def __init__(self):
		self.thrust = CopterConfigs.MIN_THRUS_TO_TEST
		self.yaw = 0
		self.roll = self.pitch = 0		
		self.thrust_offset = 1000
		self.yaw_offset = 1
		self.roll_offset = self.pitch_offset = 0.3
		self.copter_commander = None
		print "initialized copter commander!"

	def set_commander(self, commander):
		self.copter_commander = commander

	def check_values_range(self):
		self.thrust = min(self.thrust, CopterConfigs.MAX_THRUST)
		self.yaw = max(self.yaw, CopterConfigs.MIN_YAW)
		self.roll = max(self.roll, CopterConfigs.MIN_ROLL)

	def send_commands(self):
		self.check_values_range()
		if self.copter_commander:
			print "sending", self.roll, self.pitch, self.yaw, self.thrust
			self.copter_commander.send_setpoint(self.roll, self.pitch, self.yaw, self.thrust)

	def increase_thrust(self):
		self.thrust += self.thrust_offset
		self.send_commands()

	def decrease_thrust(self):
		self.thrust -= self.thrust_offset
		self.send_commands()

	def roll_left(self):
		self.roll -= self.roll_offset
		self.send_commands()

	def roll_right(self):
		self.roll += self.roll_offset
		self.send_commands()

	def yaw_left(self):
		self.yaw -= self.yaw_offset
		self.send_commands()

	def yaw_right(self):
		self.yaw += self.yaw_offset
		self.send_commands()

	def forward_pitch_down(self):
		self.pitch += self.pitch_offset
		self.send_commands()

	def backward_pitch_up(self):
		self.pitch -= self.pitch_offset
		self.send_commands()

	def halt(self):
		self.thrust = self.yaw = self.roll = self.pitch = 0
		self.send_commands()


	def notify(self, key):
		print "notified by keypress event"
		if key == "K_UP" 	: self.increase_thrust()
		if key == "K_DOWN" 	: self.decrease_thrust()
		if key == "K_LEFT" 	: self.roll_left()
		if key == "K_RIGHT" : self.roll_right()
		if key == "K_a" 	: self.yaw_left() # move left lean and move
		if key == "K_d" 	: self.yaw_right()
		if key == "K_w" 	: self.forward_pitch_down() # front goes down and moves forward
		if key == "K_s" 	: self.backward_pitch_up()
		if key == "K_h" 	: self.halt()
