import time

import cflib
from cflib import crtp
from crazyflie import Crazyflie

from copter_commander import CopterCommander
from copter_config import CopterConfigs
from copter_control_parms import CopterControlParams
from gui_manager import GUI_manager
from logger.copter_logger import CopterLogger
from utils import Utils


class CopterInterface():
    def __init__(self):
        cflib.crtp.init_drivers()
        self.crazyflie = None
        self.copter_commander = CopterCommander()
        # optional
        self.connection_callbacks = []  # [self._create_log_packet]
        self.close_callbacks = []
        self.log_configs = []
        self.logger = CopterLogger.get_logger(__name__)
        print("initialized CopterInterface.")

    def get_radio_interfaces(self):
        available_interfaces = cflib.crtp.scan_interfaces()
        for i in available_interfaces:
            print("[INTF] Interface with URI {0} found and name/comment {1}".format(i[0], i[1]))
        return [interface for interface in available_interfaces if "radio" in interface[0]]

    def get_first_copter_within_duration(self, duration):
        radio_interfaces = None
        while not radio_interfaces and duration > 0:
            time.sleep(0.5)
            radio_interfaces = self.get_radio_interfaces()
            if radio_interfaces: return radio_interfaces[0][0]
            duration -= 0.5

    def connect(self, copter_id):
        print("[INTF] Connecting to ", copter_id)
        self.logger.info("using cache dir: {0}".format(CopterConfigs.ro_cache))
        # self.crazyflie = Crazyflie(ro_cache=CopterConfigs.ro_cache, rw_cache=CopterConfigs.rw_cache)
        self.crazyflie = Crazyflie()  # rw_cache=CopterConfigs.rw_cache)
        self.crazyflie.open_link(copter_id)
        self._add_callback_for_connection()

    def close(self):
        print("[INTF] cleanup...")
        if self.crazyflie:
            self.crazyflie.close_link()
        for callbacks in self.close_callbacks:
            callbacks()

    def __callbacks_after_connection__(self):
        for callbacks in self.connection_callbacks:
            callbacks()

    def _disconnected(self, uri):
        print("disconnected :some error occured callabck" + uri)

    def _lost(self, uri, msg):
        print("lost :some error occured callabck" + uri + msg)

    def _failed(self, uri):
        print("failed : some error occured callabck" + uri)

    def _add_callback_for_connection(self):
        self.crazyflie.connected.add_callback(self._link_commander_to_copter) # Not Working???
        # self.crazyflie.link_established.add_callback(self._link_commander_to_copter)
        self.crazyflie.disconnected.add_callback(self._disconnected)
        self.crazyflie.connection_failed.add_callback(self._failed)
        self.crazyflie.connection_lost.add_callback(self._lost)

    def test_flight(self):
        while not self.copter_commander.is_commander_link_set():
            print("In Test Flight Mode ...")
            time.sleep(0.3)
        Utils.test_flight_for_short_duration(CopterConfigs.TEST_FLIGHT_TIME, self.crazyflie,
                                             CopterControlParams(thrust=25000))
        print("Test Flight Success.")

    def _link_commander_to_copter(self, link):
        print("[INTF] link to copter commander successful.", link)
        self.copter_commander.set_commander(self.crazyflie.commander)
        self.test_flight()
        self.__callbacks_after_connection__()

    def initialize_event_handler(self):
        gui_manager = GUI_manager(self.copter_commander)
        gui_manager.handle_events()

    def add_connected_callbacks(self, callback):
        self.connection_callbacks.append(callback)

    def add_close_callbacks(self, callback):
        self.close_callbacks.append(callback)

    def add_log_configs_dicts(self, log_conf):
        self.log_configs += [log_conf]

    def _create_log_packet(self):
        print("In create log packet {0}".format(len(self.log_configs)))

        for lc in self.log_configs:
            print("log configs: {0}".format(lc))
            log_conf = lc['conf']
            self.crazyflie.log.add_config(log_conf)
            if log_conf.valid:
                log_conf.data_received_cb.add_callback(lc['handler'])
                log_conf.error_cb.add_callback(self._log_error_logconfig)
                log_conf.start()
                print("loggers setup in create log packet...")
            else:
                print("acc.x/y/z not found in log TOC or its invalid")
        self._test_toc()

    def _log_error_logconfig(self, logconf, msg):
        print("Error in logconfig " + logconf.name)
        self.logger.error("Error when logging {0}: {1}".format(logconf.name, msg))

    def _test_toc(self):
        toc = self.crazyflie.log.toc
        self.logger.info("toc: ", toc)
        for group in toc.toc.keys():
            for param in toc.toc[group].keys():
                toc_element = toc.toc[group][param]
                self.logger.info("name=%s.%s, index=%d, pytype=%s, ctype=%s" %
                                 (group, param, toc_element.ident, toc_element.pytype,
                                  toc_element.ctype))
