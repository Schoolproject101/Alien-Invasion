# settings for Alien Invasion clone

import pygame

class Settings():
	"""A class to store all settings for Alien Invasion clone"""

	def __init__(self,width,height,bg_color = (0,0,255)):
		"""Initialize game#s static settings"""
		
		#Screen settings
		self.screen_height = height
		self.screen_width = width
		self.bg_color = bg_color

		# Background image
		self.bg_image = pygame.image.load("images//Space_2.png")
		self.bg_rect = self.bg_image.get_rect()

		# Ship settings
		self.ship_limit = 3

		# Bullet settings
		self.bullet_width = 5
		self.bullet_height  = 18
		self.bullet_color = (200,200,255)
		self.bullets_allowed = 3

		# Alien settings
		self.fleet_drop_speed = 10
		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

		# how quickly the game speeds up
		self.speedup_scale = 1.1
		# how quickly the alien point values increase
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game"""
		self.ship_speed_factor = 16
		self.bullet_speed_factor = 24
		self.alien_speed_factor = 8

		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

		# Scoring 
		self.alien_points = 50

	def increase_speed(self):
		"""Increase speed settings and alien point values."""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)			



