import sys
import pygame
import game_function as gf
from settings import settings
from ship import ship
from pygame.sprite import Group
from aliens import alien
from game_stats import game_stats
from button import button
from score_bored import score_bored 
# Main program to run the game
def run_game():
	pygame.init()
	ai_settings=settings()
	screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("Alien invasion by Aman Pandey")
	play_button=button(ai_settings,screen,'PLAY')
	stats=game_stats(ai_settings)
	sb=score_bored(ai_settings,screen,stats)
	ship_1=ship(screen,ai_settings)
	bullets=Group()
	aliens=Group()
	bg_color=(0,0,0)
	gf.create_fleet(ai_settings,screen,ship_1,aliens)
        # while the game is running 
	while True:
		gf.check_events(ai_settings,screen,sb,stats,play_button,ship_1,aliens,bullets)
		if stats.game_active:
			ship_1.update()
			gf.update_bullets(ai_settings,screen,stats,sb,ship_1,bullets,aliens)
			gf.update_aliens(ai_settings,stats,screen,sb,ship_1,aliens,bullets)
		gf.update_screen(ai_settings,screen,stats,sb,ship_1,aliens,bullets,play_button)
run_game()
