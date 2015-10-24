import pygame
import time


class GUI_manager():
    def __init__(self, callback):
        pygame.init()
        self.screen = pygame.display.set_mode((700, 480), 0, 24)
        pygame.display.set_caption("Flying QuadCopter")
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.mouse.set_visible(0)
        self.callback = callback
        self.QUIT_GUI = False
        print "initialized GUI!"

    def handle_events(self):
        print "handling keyboard events..."
        pygame.event.clear()
        while not self.QUIT_GUI:
            time.sleep(0.1)
            events = pygame.event.get()
            self.check_for_exit_event(events)
            if not self.QUIT_GUI: self.event_get_keys_handler(events)

    def check_for_exit_event(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.clean_and_quit()

    def event_get_keys_handler(self, events):
        if not events: self.callback.notify(None)
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]: self.callback.notify("K_UP")
        if key_pressed[pygame.K_DOWN]: self.callback.notify("K_DOWN")
        if key_pressed[pygame.K_LEFT]: self.callback.notify("K_LEFT")
        if key_pressed[pygame.K_RIGHT]: self.callback.notify("K_RIGHT")
        if key_pressed[pygame.K_a]: self.callback.notify("K_a")
        if key_pressed[pygame.K_d]: self.callback.notify("K_d")
        if key_pressed[pygame.K_w]: self.callback.notify("K_w")
        if key_pressed[pygame.K_s]: self.callback.notify("K_s")
        if key_pressed[pygame.K_h]: self.callback.notify("K_h")
        if key_pressed[pygame.K_q]: self.clean_and_quit()

    def clean_and_quit(self):
        self.QUIT_GUI = True
        pygame.quit()
