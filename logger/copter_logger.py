import logging

from cfclient.utils.logconfigreader import LogConfig

from copter_config import CopterConfigs
from logger.Accelero import Accelero


class CopterLogger:
    def __init__(self):
        self._set_basic_config()
        self.log_listeners = []
        logging.info("Initialized CopterLogger")

    def add_log_listener(self, listener):
        self.log_listeners.append(listener)

    def get_interested_loggers(self):
        return [
            self._as_dict(self.get_accelerometer_log_config(), self.log_accel_data),
            self._as_dict(self.get_gyroscope_log_config(), self.log_gyro_data)
        ]

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

    def get_gyroscope_log_config(self):
        log_conf = LogConfig("GyroScope", period_in_ms=100)
        log_conf.add_variable("gyro.x", "float")
        log_conf.add_variable("gyro.y", "float")
        log_conf.add_variable("gyro.z", "float")
        return log_conf

    def _as_dict(self, log_conf, handler):
        print(log_conf)
        return {'conf': log_conf, 'handler': handler}

    def log_stab_data(self, data):
        logging.info("Stabilizer: Roll=%.2f, Pitch=%.2f, Yaw=%.2f" %
                     (data["stabilizer.roll"], data["stabilizer.pitch"], data["stabilizer.yaw"]))

    def _notify_listeners(self, data):
        for listener in self.log_listeners:
            listener.notify(data)

    def log_accel_data(self, timestamp, data, logconf):
        self.accel_logger.info(" Accelerometer: x=%.2f, y=%.2f, z=%.2f" %
                               (data["acc.x"], data["acc.y"], data["acc.z"]))
        self._notify_listeners(Accelero(data["acc.x"], data["acc.y"], data["acc.z"]))

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
        self.gyro_logger = self.get_logger(__name__, log_file=CopterConfigs.gyro_log_file, propagate=False)
        self.accel_logger = self.get_logger("GyroLogger", log_file=CopterConfigs.accelo_log_file, propagate=False)

    def log_gyro_data(self, timestamp, data, logconf):
        self.gyro_logger.info(" GyroScope: x=%.2f, y=%.2f, z=%.2f" %
                              (data["gyro.x"], data["gyro.y"], data["gyro.z"]))
