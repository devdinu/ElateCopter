# from threading import Thread
import logging
import math

from behaviour.log_listener import LogListener
from copter_config import CopterConfigs


class AutoPilot(LogListener):
    def __init__(self, callback):
        self.callback = callback
        self.roll = self.pitch = CopterConfigs.MIN_ROLL
        self.thrust = CopterConfigs.MIN_THRUST
        self.yaw = CopterConfigs.MIN_YAW
        self.prev_data = None
        logging.info("Initialized AutoPilot")

    def _increase_thrust(self):
        self.thrust += CopterConfigs.THRUST_OFFSET

    def notify(self, data):
        # data is accelerometer for now
        # Yaw is rotation, so don't bother :)
        if self._can_increase_thrust(data): self._increase_thrust()
        self.roll = math.atan2(data.y, data.z)
        self.pitch = math.atan2(data.x, data.z)
        self._send_values()
        self.prev_data = data

    def _can_increase_thrust(self, data):
        return self.prev_data == data or data.x == data.y == 0

    def fly(self):
        pass

    def _send_values(self):
        self.callback.send_commands_from_outside(self.roll, self.pitch, self.yaw, self.thrust)
