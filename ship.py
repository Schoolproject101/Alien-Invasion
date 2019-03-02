#ship class

# cant open image for ship

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""Ship Class"""

	def __init__(self,ai_settings,screen):
		"""Initilaizes the ship and sets its position"""
		super().__init__()
		self.screen = screen 
		self.ai_settings = ai_settings
		# Loads the ship image and gets its rect
		self.image = pygame.image.load('images\ship.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		# start each new ship at the bottom of the center of the screen
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		#Store ships center as a decimal value
		self.center = float(self.rect.centerx)

		# Movement Flag
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""Update ship's position based on the movement Flag"""	
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.image = pygame.image.load("images\ship_right.png")
			self.center += self.ai_settings.ship_speed_factor

		if self.moving_left and self.rect.left > 0:
			self.image = pygame.image.load("images\ship_left.png")
			self.center -= self.ai_settings.ship_speed_factor

		# Update rect object from self.center
		self.rect.centerx = self.center		

	def blitme(self):
		"""Draws the ship at its current location"""
		self.screen.blit(self.image,self.rect)

	def center_ship(self):
		"""Center the ship on the screen"""
		self.center = self.screen_rect.centerx			