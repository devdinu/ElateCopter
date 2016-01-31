import getopt
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
    def __init__(self, auto_pilot=False, copter_logger=None):
        self.copter_interface = CopterInterface()
        copter_logger = CopterLogger()
        if auto_pilot:
            self.copter_interface.configure(auto_pilot=auto_pilot, imu_logger=copter_logger)
        self.setup_logger(copter_logger)
        # self.connected = False

    def setup_logger(self, copter_logger):
        self.copter_interface.add_log_configs_dicts(copter_logger.get_interested_loggers())
        # self.copter_interface.add_close_callbacks(copter_logger.stop_logs)

    def process(self):
        print("ElatedCopter processing ...")
        cid = self.copter_interface.get_first_copter_within_duration(5)
        if cid:
            self.copter_interface.connect(cid)
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
    parse_arguments(sys.argv[1:])
