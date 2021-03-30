import pygame.font
from pygame.sprite import Group
from ship import ship

class score_bored():
	def __init__(self,ai_settings,screen,stats):
		self.screen=screen
		self.ai_settings=ai_settings
		self.stats=stats
		self.screen_rect=screen.get_rect()

		#font settings
		self.font_color=(30,30,30)
		self.font=pygame.font.SysFont(None,35)

		#prepare init. score image.
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()

	def prep_score(self):
		rounded_score=int(round(self.stats.score, -1)) #-1 tells python to roud the number in nearest 10.		
		self.score_str="{:,}".format(rounded_score) #""this converts into string,formating directives tells python to place comma at every 10 place 
		self.score_image=self.font.render(self.score_str,True,self.font_color,self.ai_settings.bg_color)

		#display score at top the of the screen.
		self.score_rect=self.score_image.get_rect()
		self.score_rect.right=self.screen_rect.right - 1
		self.score_rect.top=self.screen_rect.top + 1

	def prep_high_score(self):
		high_score=int(round(self.stats.high_score , -1))
		high_score_str="{:,}".format(high_score)
		self.high_score_img=self.font.render(high_score_str,True,self.font_color,self.ai_settings.bg_color)
		self.high_score_rect=self.high_score_img.get_rect()
		self.high_score_rect.centerx=self.screen_rect.centerx
		self.high_score_rect.top=self.screen_rect.top

	def prep_level(self):
		self.level_image=self.font.render(str(self.stats.level),True,self.font_color,self.ai_settings.bg_color)
		self.level_rect=self.level_image.get_rect()
		self.level_rect.right=self.screen_rect.right - 1
		self.level_rect.top=self.screen_rect.top + 30

	def prep_ships(self):
		self.ships=Group()
		for ship_num in range(self.stats.ship_left):
			ship_2=ship(self.screen,self.ai_settings)
			ship_2.rect.x=10 + ship_num*ship_2.rect.width
			ship_2.rect.y= 1 
			self.ships.add(ship_2)

	def show_score(self):
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.high_score_img,self.high_score_rect)
		self.screen.blit(self.level_image,self.level_rect)
		self.ships.draw(self.screen)

