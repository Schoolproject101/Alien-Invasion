# module for game functions
import pygame
from time import sleep 
import sys

from bullet import Bullet
from alien import Alien


def check_keydown_events(event,ai_settings,screen,stats,sb,play_button,ship,aliens,
		bullets):
	"""Responds to keypresses"""
	if event.key == pygame.K_RIGHT:
		# move ship to the right
		ship.moving_right = True
			
	elif event.key == pygame.K_LEFT:
		# moves ship to the left
		ship.moving_left = True	

	elif event.key == pygame.K_SPACE:
		# Fire bullet
		fire_bullet(ai_settings,screen,ship,bullets)

	elif event.key == pygame.K_ESCAPE:
		# exits the game when the q button is pressed
		sys.exit()

	elif event.key == pygame.K_p:
		# Starts the game when p is pressed 
		p_pressed = True
		mouse_x, mouse_y = pygame.mouse.get_pos()
		check_play_button(ai_settings, screen, stats,sb, play_button, ship,
			aliens, bullets, mouse_x, mouse_y,p_pressed)		

def fire_bullet(ai_settings,screen,ship,bullets):
	"""fire a bullet if the limit is not yet reached"""
	# Create new bullet and add it the the bullets group
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)	

def check_keyup_events(event,ship):
	"""Responds to key releases"""
	if event.key == pygame.K_RIGHT:
		# stops ship movement to the right
		ship.moving_right = False
		ship.image = pygame.image.load("images\ship.png")

	elif event.key == pygame.K_LEFT:
		# stops ship mvement to the left
		ship.moving_left = False
		ship.image = pygame.image.load("images\ship.png")

	elif event.key == pygame.K_p:
		# stops starting the game
		p_pressed = False				

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,
		bullets):
	"""checks for keyboard and mouse inputs"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb,play_button, ship,
				aliens, bullets, mouse_x, mouse_y,False)	

		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)

		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)		


def check_play_button(ai_settings,screen,stats,sb,play_button,ship, aliens,
		bullets, mouse_x, mouse_y, p_pressed):
	"""Starts a  new game when the player clicks play"""
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if (button_clicked or p_pressed ) and not stats.game_active:
		start_game(ai_settings,screen,stats,sb,ship, aliens,
			bullets)

def start_game(ai_settings,screen, stats,sb,ship, aliens,
		bullets):
	"""Starts the game after the p button is pressed or the play button"""

	# Reset the game settings
	ai_settings.initialize_dynamic_settings()

	# Hide the mouse cursor
	pygame.mouse.set_visible(False)

	# reset the game statistics
	stats.reset_stats()
	stats.game_active = True

	# Reset the scoreboard image
	sb.prep_score()
	sb.prep_high_score()
	sb.prep_level()
	sb.prep_ships()

	# Empty the list of aliens and bullets
	aliens.empty()
	bullets.empty()

	# Create a new fleet and center the ship
	create_fleet(ai_settings, screen, ship, aliens)
	ship.center_ship


def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,
		play_button):
	"""updates images and flips to new screen"""

	# Redraw the screen during each pass through the loop
	#screen.fill(ai_settings.bg_color)
	screen.blit(ai_settings.bg_image,ai_settings.bg_rect)

	# Redraw all bullets behind ship and aliens.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)

	# draw the score information
	sb.show_score()

	# Draw the play button if the game is inactive
	if not stats.game_active:
		play_button.draw_button()

	# Make the most recently drawn screnn visible.
	pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,
		aliens,bullets):
	"""Update Bullet position and get rid of old bullets."""
	#Update Bullet posistion
	bullets.update()

	# Get rid of old bullets
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,
		aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,
		aliens,bullets):
	"""Respond to bullet_alien collisions"""
	#Remove any bullets and aliens that have collided
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points
			sb.prep_score()
		check_high_score(stats, sb)	

	if len(aliens) == 0:
		# If the entire fleet is destroyed, starta new level
		bullets.empty()
		ai_settings.increase_speed()

		# Increase level.
		stats.level += 1
		sb.prep_level()

		create_fleet(ai_settings,screen,ship,aliens)


def get_number_aliens_x(ai_settings, alien_width):
	"""Determine the number of aliens that fit in a row """
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens that fit on the screen"""
	available_space_y = (ai_settings.screen_height -
							(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (3 * alien_height))
	return number_rows



def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and place it in the row"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien = Alien(ai_settings,screen)
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
	"""Create a full fleet of aliens"""
	# Create a full fleet of aliens.
	# Spacing between each alien is equal to one alien width
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,
		alien.rect.height)

	# Create the fleet of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,
				row_number)

def check_fleet_edges(ai_settings,aliens):
	"""Respond appropriately if any aliens have reached the edge"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""Drop the entire fleet and change the fleet's direction"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,screen,stats,sb,ship,aliens, bullets):
	"""Respond to ship being hit by alien"""
	if stats.ships_left > 0 :
		# Decrement ships_left
		stats.ships_left -= 1

		# Update scoreboard
		sb.prep_ships()

		# Empty the list of aliens and bullets.
		aliens.empty()
		bullets.empty()

		# Create new fleet and center the ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

		# Pause
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)	

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens, bullets):
	"""Check if any aliens have reached the bottom of the screen"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treat this the same as if the ship got hit
			ship_hit(ai_settings,screen,stats,sb,ship,aliens, bullets)
			break			

def update_aliens(ai_settings,screen,stats,sb,ship,aliens, bullets):
	"""
	Check if the fleet is at an edge,
	and then update the positions of all aliens in the fleet
	"""
	# look for aliens hitting the bottom of the screen.
	check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens, bullets)

	check_fleet_edges(ai_settings,aliens)
	aliens.update()

	# Look for alien-ship collisions.
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,screen,stats,sb,ship,aliens, bullets)


def check_high_score(stats, sb):
	"""Check to see if there's a new high score"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score				


def ask_name():
	"""ask the user for there name and store it."""
	pass