import sys
import pygame
from bullet import bullet
from aliens import alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,stats,sb,play_button,ship_1,aliens,bullets):

	if event.key==pygame.K_RIGHT:
		ship_1.moving_right=True
	elif event.key==pygame.K_LEFT:
		ship_1.moving_left=True
	elif event.key==pygame.K_SPACE:
		fire_bullets(ai_settings,screen,ship_1,bullets)
	elif event.key==pygame.K_q:
		sys.exit()
	elif event.key==pygame.K_p:
		play_button_press(ai_settings,screen,stats,sb,play_button,ship_1,aliens,bullets,event)
		
				
def check_keyup_events(event,ship_1):

	if event.key==pygame.K_RIGHT:
		ship_1.moving_right=False
	elif event.key==pygame.K_LEFT:
		ship_1.moving_left=False

def check_events(ai_settings,screen,stats,sb,play_button,ship_1,aliens,bullets):
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()

		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,sb,stats,play_button,ship_1,aliens,bullets)

		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship_1)

		elif event.type==pygame.MOUSEBUTTONDOWN: #pygame detects MOUSEBUTTON event when it is clicked anywhere in the screen.
			mouse_x,mouse_y=pygame.mouse.get_pos()  # returns  position in the form of tuples,
			check_play_button(ai_settings,screen,stats,sb,play_button,ship_1,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship_1,aliens,bullets,mouse_x,mouse_y):
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	#check weather mouse click happens in the defined region of paly button.
	if button_clicked and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False) #hide cursor.
		stats.reset_stats()
		stats.game_active=True
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		#reset ship,alien,bullets
		aliens.empty()
		bullets.empty()

		create_fleet(ai_settings,screen,ship_1,aliens)
		ship_1.center_ship()

def play_button_press(ai_settings,screen,stats,sb,play_button,ship_1,aliens,bullets,event):
	if event.key==pygame.K_p and not stats.game_active: #check weather mouse click happens in the defined region of paly button.
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False) #hide cursor.
		stats.reset_stats()
		stats.game_active=True
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		#reset ship,alien,bullets
		aliens.empty()
		bullets.empty()

		create_fleet(ai_settings,screen,ship_1,aliens)
		ship_1.center_ship()

def update_bullets(ai_settings,screen,stats,sb,ship_1,bullets,aliens):
	bullets.update() #updates all the elements in the group.
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_collision(ai_settings,screen,stats,sb,ship_1,aliens,bullets)

def fire_bullets(ai_settings,screen,ship_1,bullets):
	if len(bullets) < ai_settings.bullets_allowed:
			new_bullet=bullet(ai_settings,screen,ship_1)
			bullets.add(new_bullet)

def get_num_alien(ai_settings,screen,alien_width):
	available_space_x=ai_settings.screen_width - 2*alien_width
	num_aliens=int((available_space_x)/(2*alien_width))
	return num_aliens

def get_num_rows(ai_settings,ship_height,alien_height):
	available_space_y=(ai_settings.screen_height -(3*alien_height) -(ship_height))
	num_rows=int(available_space_y/(2*alien_height))
	return num_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	alien_1=alien(ai_settings,screen)
	alien_width=alien_1.rect.width
	alien_1.x=alien_width + 2*alien_width*alien_number
	alien_1.rect.x=alien_1.x
	alien_1.rect.y=alien_1.rect.height + 2*alien_1.rect.height*row_number
	aliens.add(alien_1)

def create_fleet(ai_settings,screen,ship_1,aliens):
	alien_1=alien(ai_settings,screen)
	num_aliens=get_num_alien(ai_settings,screen,alien_1.rect.width)
	row_number=get_num_rows(ai_settings,ship_1.rect.height,alien_1.rect.height)

	for row in range(row_number):		
		for alien_number in range(num_aliens):
			create_alien(ai_settings,screen,aliens,alien_number,row)	

def change_fleet_direction(ai_settings,aliens):
	for alien_1 in aliens.sprites():
		alien_1.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings,aliens):
	for alien_1 in aliens.sprites():
		if alien_1.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def update_aliens(ai_settings,stats,screen,sb,ship_1,aliens,bullets):
	check_alien_bottom(ai_settings,stats,sb,screen,ship_1,aliens,bullets)
	check_fleet_edges(ai_settings,aliens)
	aliens.update() #it updates all the alien_1(element) in a grp.
	if pygame.sprite.spritecollideany(ship_1,aliens): #collision between  a gruop and spite.
		ship_hit(ai_settings,stats,sb,screen,ship_1,aliens,bullets)


def check_collision(ai_settings,screen,stats,sb,ship_1,aliens,bullets):
	collision =pygame.sprite.groupcollide(bullets,aliens,True,True) #collision b/w two groups.
	if collision :
		for aliens in collision.values():
			stats.score += ai_settings.alien_points*len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
	if len(aliens)==0:
		bullets.empty()
		ai_settings.increase_speed()
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings,screen,ship_1,aliens)


def ship_hit(ai_settings,stats,sb,screen,ship_1,aliens,bullets):
	if stats.ship_left > 0:
		stats.ship_left -= 1
		sb.prep_ships()
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings,screen,ship_1,aliens)
		ship_1.center_ship()
		sleep(0.5)
	else:
		stats.game_active=False
		pygame.mouse.set_visible(True)

def check_alien_bottom(ai_settings,stats,sb,screen,ship_1,aliens,bullets):
	screen_rect=screen.get_rect()
	for alien_1 in aliens.sprites():
		if alien_1.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings,stats,sb,screen,ship_1,aliens,bullets)
			break

def check_high_score(stats,sb):
	if stats.score > stats.high_score:
		stats.high_score=stats.score
		sb.prep_high_score()

def update_screen(ai_settings,screen,stats,sb,ship_1,aliens,bullets,play_button):
	screen.fill(ai_settings.bg_color)

	for bullet in bullets.sprites():
		bullet.draw_bullet()

	ship_1.blitme()
	aliens.draw(screen)
	sb.show_score()
	if not stats.game_active:
		play_button.draw_button()
	pygame.display.flip()

