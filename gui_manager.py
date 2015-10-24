import pygame
from pygame.locals import *
import time

# from threading import Thread

# class GUI_manager(Thread):
class GUI_manager():

	def __init__(self, callback):
		# Thread.__init__(self)
		pygame.init()
		self.screen = pygame.display.set_mode((700,480),0,24)
		pygame.display.set_caption("Flying QuadCopter")
		pygame.event.set_blocked(pygame.MOUSEMOTION)
		pygame.mouse.set_visible(0)
		# BLACK = (  0,   0,   0)
		# self.screen.fill(BLACK)
		self.callback = callback
		self.QUIT_GUI = False
		print "initialized GUI!"		
	# def run(self):
	# 	self.handle_event(self.callback)

	def handle_event(self):			
			print "handling keyboard events..."
			pygame.event.clear()
			while not self.QUIT_GUI:
				# time.sleep(1)
				events = pygame.event.get()
				self.event_get_keys_handler(events)
				self.event_loop_key_handler(events)

	def event_loop_key_handler(self, events):
		for e in events:
			if e.type == pygame.KEYDOWN:
				print "key down works....."

	def event_get_keys_handler(self, events):
		if not events: return			
		key_pressed = pygame.key.get_pressed()
		# print key_pressed, "presss worked by get_pressed!!!! .....", pygame.key.get_pressed()
	 	if key_pressed[pygame.K_UP]					: self.callback.notify("K_UP")
		if pygame.key.get_pressed()[pygame.K_DOWN]	: self.callback.notify("K_DOWN")
		if pygame.key.get_pressed()[pygame.K_LEFT]	: self.callback.notify("K_LEFT")
		if pygame.key.get_pressed()[pygame.K_RIGHT]	: self.callback.notify("K_RIGHT")
		if pygame.key.get_pressed()[pygame.K_a]		: self.callback.notify("K_a") # move left lean and move
		if pygame.key.get_pressed()[pygame.K_d]		: self.callback.notify("K_d")
		if pygame.key.get_pressed()[pygame.K_w]		: self.callback.notify("K_w") # front goes down and moves forward
		if pygame.key.get_pressed()[pygame.K_s]		: self.callback.notify("K_s")
		if pygame.key.get_pressed()[pygame.K_h]		: self.callback.notify("K_h")
		if pygame.key.get_pressed()[pygame.K_q]:
			self.QUIT_GUI = True
			# 	raise SystemExit
			# 	pygame.display.quit()
			pygame.quit()
		if key_pressed[pygame.QUIT]:
			self.QUIT_GUI = True
			pygame.quit()
			# pygame.event.pump()				

# from copter_commander import CopterCommander
# copter_commander = CopterCommander(None)
# gui = GUI_manager(copter_commander)
# gui.start()
# while True:
# 	pygame.mainloop(0.1)

# gui.handle_event(copter_commander)
# print "well thread started, waiting though"
# gui.join()
# print "main ends"

	# class Notifier(Thread):
	# 	def run():
	# 		while True:
	# 			print "I know thats thread is running!"
	# 			if pygame.key.get_pressed()[pygame.K_DOWN]: print "Down Key Notify"

