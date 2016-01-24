import logging

from cfclient.utils.logconfigreader import LogConfig

from copter_config import CopterConfigs


class CopterLogger:
    def __init__(self):
        self.log_file = CopterConfigs.inertia_log_file
        self._set_basic_config()

    def get_interested_logger(self):
        return self._as_dict(self.get_accelerometer_log_config(), self.log_accel_data)  # ge`t_stabilizer_log_config()
        # return self._as_dict(self.similar_conf(), self.log_stab_data)  # ge`t_stabilizer_log_config()  # self.get_accelerometer_log_config()

    def get_accelerometer_log_config(self):
        log_conf = LogConfig("Accel", period_in_ms=100)
        log_conf.add_variable("acc.x", "float")
        log_conf.add_variable("acc.y", "float")
        log_conf.add_variable("acc.z", "float")
        return log_conf

    def get_stabilizer_log_config(self):
        stab_log_conf = LogConfig("stabilizer", period_in_ms=100)
        stab_log_conf.add_variable("stabilizer.roll", "float")
        stab_log_conf.add_variable("stabilizer.pitch", "float")
        stab_log_conf.add_variable("stabilizer.yaw", "float")
        return stab_log_conf

    def _as_dict(self, log_conf, handler):
        print(log_conf)
        return {'conf': log_conf, 'handler': handler}

    def log_stab_data(self, data):
        logging.info("Stabilizer: Roll=%.2f, Pitch=%.2f, Yaw=%.2f" %
                     (data["stabilizer.roll"], data["stabilizer.pitch"], data["stabilizer.yaw"]))

    def log_accel_data(self, timestamp, data, logconf):
        print(logconf.name, data + " Accelerometer: x=%.2f, y=%.2f, z=%.2f" %
              (data["acc.x"], data["acc.y"], data["acc.z"]))

    def log_conf_error(self, logconf, msg):
        print("Error logconf" + logconf + "message: " + msg)

    @classmethod
    def get_logger(cls, name, log_file=None, propagate=True):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        if (log_file):
            logger.addHandler(logging.FileHandler(filename=log_file, mode='w'))
        logger.propagate = propagate
        return logger

    def _set_basic_config(self):
        # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        # datefmt='%H:%M:%S'
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.FileHandler(filename=self.log_file, mode='w'))
