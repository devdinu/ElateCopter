from copter_config import CopterConfigs


class CopterCommander():
    def __init__(self):
        self.thrust = CopterConfigs.MIN_THRUST
        self.yaw = 0
        self.roll = self.pitch = 0
        self.copter_commander = None
        print "initialized copter commander!"

    def debug_current_values(self):
        print "=> roll:", self.roll, " pitch: ", self.pitch, " yaw: ", self.yaw, " thrust ", self.thrust

    def set_commander(self, commander):
        self.copter_commander = commander
        print "CopterCommander have been set."

    def check_values_range(self):
        self.thrust = min(self.thrust, CopterConfigs.MAX_THRUST)
        self.thrust = max(self.thrust, CopterConfigs.MIN_THRUST)
        self.yaw = max(self.yaw, CopterConfigs.MIN_YAW)
        self.yaw = min(self.yaw, CopterConfigs.MAX_YAW)
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
        self.thrust += CopterConfigs.THRUST_OFFSET
        self.send_commands()

    def decrease_thrust(self):
        self.thrust -= CopterConfigs.THRUST_OFFSET
        self.send_commands()

    def roll_left(self):
        self.roll -= CopterConfigs.ROLL_OFFSET
        self.send_commands()

    def roll_right(self):
        self.roll += CopterConfigs.ROLL_OFFSET
        self.send_commands()

    def yaw_left(self):
        self.yaw -= CopterConfigs.YAW_OFFSET
        self.send_commands()

    def yaw_right(self):
        self.yaw += CopterConfigs.YAW_OFFSET
        self.send_commands()

    def forward_pitch_down(self):
        self.pitch += CopterConfigs.PITCH_OFFSET
        self.send_commands()

    def backward_pitch_up(self):
        self.pitch -= CopterConfigs.PITCH_OFFSET
        self.send_commands()

    def halt(self):
        self.thrust = CopterConfigs.THRUST_RESET
        self.yaw = CopterConfigs.YAW_RESET
        self.roll = CopterConfigs.ROLL_RESET
        self.pitch = CopterConfigs.PITCH_RESET
        self.send_commands()

    def notify(self, key):
        # print "notified by keypress event", key
        if key == "INCREASE_THRUST":
            self.increase_thrust()
        elif key == "DECREASE_THRUST":
            self.decrease_thrust()
        elif key == "ROLL_LEFT":
            self.roll_left()
        elif key == "ROLL_RIGHT":
            self.roll_right()
        elif key == "YAW_LEFT":
            self.yaw_left()  # move left lean and move
        elif key == "YAW_RIGHT":
            self.yaw_right()
        elif key == "PITCH_DOWN":
            self.forward_pitch_down()  # front goes down and moves forward
        elif key == "PITCH_UP":
            self.backward_pitch_up()
        elif key == "STOP":
            self.halt()
        else:
            self.send_current_values()  # Stops if no command is sent! but with last saved values

    def is_commander_link_set(self):
        return self.copter_commander != None
