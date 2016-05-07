import getopt
import logging
import sys

from copter_interface import CopterInterface

# Other Utils for my customization
from logger.copter_logger import CopterLogger


# Sample Input
# roll    = 0.0
# pitch   = 0.0
# yaw = 0
# thrust  = 10001 to 60000


class ElatedCopter():
    def __init__(self, auto_pilot=False):
        self.copter_interface = CopterInterface()
        self.auto_pilot = auto_pilot

    def configure_interface(self, auto_pilot):
        copter_logger = self.setup_logger()
        if auto_pilot:
            logging.info("Auto Pilot Mode")
            self.copter_interface.configure(auto_pilot=auto_pilot, imu_logger=copter_logger)
        else:
            logging.info("Manual Mode")
            self.copter_interface.configure()

    def setup_logger(self):
        copter_logger = CopterLogger()
        self.copter_interface.add_log_configs_dicts(copter_logger.get_interested_loggers())
        return copter_logger

    def process(self):
        print("ElatedCopter processing ...")
        cid = self.copter_interface.get_first_copter()
        if cid:
            self.copter_interface.connect(cid)
            self.configure_interface(self.auto_pilot)
        else:
            print("No copters found!!!")
        self.close()

    def close(self):
        self.copter_interface.close()


def parse_arguments(args):
    try:
        opts, args = getopt.getopt(args, "hag", ["auto", "gui"])
        for opt, values in opts:
            if opt in ["-a", "--auto"]:
                ElatedCopter(auto_pilot=True).process()
            elif opt in ["-g", "--gui"]:
                ElatedCopter().process()
    except getopt.GetoptError as err:
        print(str(err))


if __name__ == "__main__":
    print("Running program")
    parse_arguments(sys.argv[1:])
