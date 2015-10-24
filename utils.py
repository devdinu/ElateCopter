

class Utils():

    @classmethod
    def test_flight_for_short_duration(cls, duration, copter_handle, fly_param):
        while duration:
            copter_handle.commander.send_setpoint(fly_param.roll, fly_param.pitch, fly_param.yaw, fly_param.thrust)
            duration -= 1
