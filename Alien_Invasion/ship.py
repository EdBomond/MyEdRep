import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        self.image = pygame.image.load('alien_invasion/images/rocket.bmp')
        DEFAULT_IMAGE_SIZE = (80, 80)
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False
        self.settings = ai_game.settings
        self.x=float(self.rect.x)
    
    def update(self):
        if self.moving_right == True and self.rect.right <= self.screen_rect.right:
            self.x += self.settings.ship_speed
             
        if self.moving_left == True and self.rect.left >= 0:
            self.x -= self.settings.ship_speed

        self.rect.x=self.x
            
    def blitme(self):
        self.screen.blit(self.image,self.rect)   
        
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)     
