import time

import pygame
from copter_config import CopterConfigs

from my_config import MyConfig


class Resources():
    image = pygame.image.load(MyConfig.image_path)
    # window_size = (10, 10)
    window_size = image.get_rect().size
    start_point = (0, 0)


class GUI_manager():
    def __init__(self, callback):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode(
            # Resources.window_size, 0, 0)
            pygame.display.list_modes()[0],
            pygame.FULLSCREEN)  #

        pygame.display.set_caption("Flying QuadCopter")
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.mouse.set_visible(0)
        self.callback = callback
        self.QUIT_GUI = False
        self.font = pygame.font.SysFont("monospace", 15)
        print("initialized GUI!")

    def add_image(self):
        self.screen.blit(Resources.image, Resources.start_point)

    def handle_events(self):
        print("handling keyboard events...")
        pygame.event.clear()
        while not self.QUIT_GUI:
            time.sleep(0.1)
            pygame.event.pump()
            pygame.event.set_grab(True)
            events = pygame.event.get()
            self.check_for_exit_event(events)
            if not self.QUIT_GUI: self.event_get_keys_handler(events)

    def check_for_exit_event(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.clean_and_quit()

    def event_get_keys_handler(self, events):
        self.render_screen()
        if not events: self.callback.notify(None)
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]: self.callback.notify("INCREASE_THRUST")
        if key_pressed[pygame.K_DOWN]: self.callback.notify("DECREASE_THRUST")
        if key_pressed[pygame.K_LEFT]: self.callback.notify("ROLL_LEFT")
        if key_pressed[pygame.K_RIGHT]: self.callback.notify("ROLL_RIGHT")
        if key_pressed[pygame.K_a]: self.callback.notify("YAW_LEFT")
        if key_pressed[pygame.K_d]: self.callback.notify("YAW_RIGHT")
        if key_pressed[pygame.K_w]: self.callback.notify("PITCH_DOWN")
        if key_pressed[pygame.K_s]: self.callback.notify("PITCH_UP")
        if key_pressed[pygame.K_h]: self.callback.notify("STOP")
        if key_pressed[pygame.K_SPACE]: self.callback.notify("STOP")
        if key_pressed[pygame.K_q]: self.clean_and_quit()

    def clean_and_quit(self):
        self.QUIT_GUI = True
        pygame.quit()

    def show_values(self, value):
        label = self.font.render(value, 1, (255, 255, 0))
        self.screen.blit(label, (100, 100))

    def render_screen(self):
        self.add_image()
        mine = self.font.render(CopterConfigs.APP_NAME, 1, (255, 255, 0))
        self.screen.blit(mine, (0, 0))
        pygame.display.flip()
