import pygame.font


class button:
	def __init__(self,ai_settings,screen,msg):
		self.screen=screen
		self.screen_rect=screen.get_rect()

		#set dimen. and properties of button.
		self.width,self.height=200,50
		self.button_color=(0,225,0)
		self.text_color=(225,225,225)
		self.font=pygame.font.SysFont(None,48)

		#build rect obj of button and center it.
		self.rect=pygame.Rect(0,0,self.width,self.height)
		self.rect.center=self.screen_rect.center


		# The button message needs to be prepped only once.
		self.prep_msg(msg)


	def prep_msg(self,msg):
		self.msg_image=self.font.render(msg,True,self.text_color,self.button_color) #true for on/off antianailizing .
		self.msg_image_rect=self.msg_image.get_rect()
		self.msg_image_rect.center=self.rect.center


	def draw_button(self):
		self.screen.fill(self.button_color,self.rect)
		self.screen.blit(self.msg_image,self.msg_image_rect)








