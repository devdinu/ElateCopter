import logging
import sys

import time

import crazyflie
import cflib
from cflib import *
from crazyflie import Crazyflie
from copter_control_parms import CopterControlParams
from copter_interface import CopterInterface
from copter_commander import *



# Other Utils for my customization
from gui_manager import GUI_manager
from logger.copter_logger import CopterLogger
from utils import Utils


# Sample Input
# roll    = 0.0
# pitch   = 0.0
# yaw = 0
# thrust  = 10001 to 60000


class ElatedCopter():
    def __init__(self):
        self.copter_interface = CopterInterface()
        self.setup_logger()
        # self.connected = False

    def setup_logger(self):
        copter_logger = CopterLogger()
        self.copter_interface.add_log_configs_dicts(copter_logger.get_interested_logger())
        # self.copter_interface.add_close_callbacks(copter_logger.stop_logs)

    def process(self):
        print("ElatedCopter processing ...")
        cid = self.copter_interface.get_first_copter_within_duration(5)
        if cid:
            self.copter_interface.connect(cid)
            self.copter_interface.initialize_event_handler()
        else:
            print("No copters found!!!")
        self.close()

    def close(self):
        self.copter_interface.close()


ElatedCopter().process()
