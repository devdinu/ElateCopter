# Chiru

Controls crazyflie without External Controllers (PS3, XBOX), Removes requirement for [Input Devices](https://wiki.bitcraze.io/projects:crazyflie:pc_utils:inputdevices). Use computer's Keyboard as the input device.

### Goal: Give it Intelligence and Fly in Autopilot Mode

# Configuration

It controls the flight parameters Thrust, Roll, Yaw, Pitch with the following configuration keys.

```
    pygame.K_UP : INCREASE_THRUST
    pygame.K_DOWN : DECREASE_THRUST
    pygame.K_LEFT : ROLL_LEFT
    pygame.K_RIGHT : ROLL_RIGHT
    pygame.K_a : YAW_LEFT
    pygame.K_d : YAW_RIGHT
    pygame.K_w : PITCH_DOWN
    pygame.K_s : PITCH_UP
    pygame.K_h : STOP
    pygame.K_SPACE : STOP
    pygame.K_q : clean_and_quit # Quit Application
```

STOP resets all flight parameters to 0 or respective reset values from `copter_config.py` eg:THRUST_RESET to 10000 (minimum Thrust value).


# Setup

* Download cfclient and add it to path.
* Install Required modules from requirements.py ```pip install -r requirements.py```
* fly by running ```python control_copter.py```



