# game stats

class GameStats():
	"""Track Alien Invasion statistics"""

	def __init__(self,ai_settings):
		"""Initialize statistics"""
		# High score should never be reset
		self.high_score = 0
		self.ai_settings = ai_settings
		self.reset_stats()
		# Start ALien Invasion in an inactive state.
		self.game_active = False

	def reset_stats(self):
		"""Initilaize statistics that can change during the game"""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
