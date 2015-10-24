import cflib
from crazyflie import Crazyflie
import time
from copter_commander import CopterCommander
from copter_control_parms import CopterControlParams
from gui_manager import GUI_manager
from utils import Utils


class CopterInterface():
    def __init__(self):
        cflib.crtp.init_drivers()
        self.crazyflie = None
        self.copter_commander = CopterCommander()

    def get_radio_interfaces(self):
        available_interfaces = cflib.crtp.scan_interfaces()
        for i in available_interfaces:
            print "[INTF] Interface with URI [%s] found and name/comment [%s]" % (i[0], i[1])
        return [interface for interface in available_interfaces if "radio" in interface[0]]

    def get_first_copter_within_duration(self, duration):
        radio_interfaces = None
        while not radio_interfaces and duration > 0:
            time.sleep(0.3)
            radio_interfaces = self.get_radio_interfaces()
            if radio_interfaces: return radio_interfaces[0][0]
            duration -= 0.5

    def connect(self, copter_id):
        print "[INTF] Connecting to ", copter_id
        self.crazyflie = Crazyflie()
        self.crazyflie.open_link(copter_id)
        self.add_callback_for_connection()

    def close(self):
        print "[INTF] cleanup..."
        if self.crazyflie:
            self.crazyflie.close_link()

    def add_callback_for_connection(self):
        self.crazyflie.connected.add_callback(self.link_commander_to_copter)
        self.copter_commander.set_commander(self.crazyflie.commander)

    def test_flight(self):
        while not self.copter_commander.is_commander_link_set():
            print "In Test Flight Mode ..."
            time.sleep(0.3)
        Utils.test_flight_for_short_duration(5, self.crazyflie, CopterControlParams(thrust=10000))
        print("Test Flight Success.")

    def link_commander_to_copter(self, link):
        print "[INTF] link to copter commander successful.", link
        self.copter_commander.set_commander(self.crazyflie.commander)
        # self.test_flight()

    def initialize_event_handler(self):
        gui_manager = GUI_manager(self.copter_commander)
        gui_manager.handle_events()
