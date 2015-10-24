from copter_config import CopterConfigs


class CopterCommander():
    def __init__(self):
        self.thrust = CopterConfigs.MIN_THRUS_TO_TEST
        self.yaw = 0
        self.roll = self.pitch = 0
        self.thrust_offset = 500
        self.yaw_offset = 1
        self.roll_offset = self.pitch_offset = 0.3
        self.copter_commander = None
        print "initialized copter commander!"

    def debug_current_values(self):
        print "values: ", self.roll, self.pitch, self.yaw, self.thrust

    def set_commander(self, commander):
        self.copter_commander = commander
        print self.copter_commander

    def check_values_range(self):
        self.thrust = min(self.thrust, CopterConfigs.MAX_THRUST)
        self.thrust = max(self.thrust, CopterConfigs.MIN_THRUST)
        self.yaw = min(self.yaw, CopterConfigs.MIN_YAW)

    # self.roll = max(self.roll, CopterConfigs.MIN_ROLL)

    def get_flying_params(self):
        return self.roll, self.pitch, self.yaw, self.thrust

    def send_current_values(self):
        if self.copter_commander:
            self.copter_commander.send_setpoint(self.roll, self.pitch, self.yaw, self.thrust)

    def send_commands_from_outside(self, roll, pitch, yaw, thrust):
        self.copter_commander.send_setpoint(roll, pitch, yaw, thrust)

    def send_commands(self):
        self.check_values_range()
        self.debug_current_values()
        if self.copter_commander:
            print "sending commands...."
            for d in range(0, 10):
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
        # print "notified by keypress event", key
        if key == "K_UP":
            self.increase_thrust()
        elif key == "K_DOWN":
            self.decrease_thrust()
        elif key == "K_LEFT":
            self.roll_left()
        elif key == "K_RIGHT":
            self.roll_right()
        elif key == "K_a":
            self.yaw_left()  # move left lean and move
        elif key == "K_d":
            self.yaw_right()
        elif key == "K_w":
            self.forward_pitch_down()  # front goes down and moves forward
        elif key == "K_s":
            self.backward_pitch_up()
        elif key == "K_h":
            self.halt()
        # else: self.send_current_values()

    def is_commander_link_set(self):
        return self.copter_commander != None
