class CopterConfigs():
    # Roll/pitch: degree
    # Yaw: degree/second
    # Thrust: 0 - 60 000 (mapped to PWM output)

    ROLL_OFFSET = 5
    PITCH_OFFSET = 5
    YAW_OFFSET = 10

    MIN_ROLL = MIN_PITCH = -90
    MAX_ROLL = MAX_PITCH = 90
    MIN_YAW = 0
    MAX_YAW = 360

    MIN_THRUST = 9000
    MAX_THRUST = 60000

    PITCH_RESET = 0
    ROLL_RESET = 0
    THRUST_RESET = 10000
    YAW_RESET = 0

    THRUST_OFFSET = 300

    # MAX_ROLL =
    # MAX_PITCH
    # MAX_YAW

    TEST_FLIGHT_TIME = 50
