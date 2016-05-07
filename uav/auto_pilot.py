# from threading import Thread
import logging
import math
import time

from behaviour.log_listener import LogListener
from copter_config import CopterConfigs
from copter_control_parms import CopterControlParams


class AutoPilot(LogListener):
    def __init__(self, callback):
        self.callback = callback
        self.roll = self.pitch = CopterConfigs.MIN_ROLL
        self.thrust = CopterConfigs.MIN_THRUST + 2000
        self.yaw = 0
        self.prev_data = None
        self.connected = self.halt = False
        logging.info("Initialized AutoPilot")

    def _increase_thrust(self):
        self.thrust += CopterConfigs.THRUST_OFFSET

    def notify(self, data):
        # data is accelerometer for now
        # Yaw is rotation, so don't bother :)
        if self._can_increase_thrust(data):
            self._increase_thrust()
        else:
            print("cant increaset thrust")
        self.roll = math.atan2(data.y, data.z)
        self.pitch = math.atan2(data.x, data.z)
        self._send_values()
        self.prev_data = data
        if not self.connected: self.connected = True

    def _can_increase_thrust(self, data):
        return self.prev_data == data or data.x == data.y == 0 or self.thrust < CopterConfigs.THRUST_FLYING_LEVEL

    def fly(self):
        while not self.halt:
            print("Waiting...")
            time.sleep(0.2)
            if self.connected:
                self._send_values()

    def _send_values(self):
        self.callback.send_commands_from_outside(
            CopterControlParams(self.thrust, self.yaw, self.roll, self.pitch)
        )
