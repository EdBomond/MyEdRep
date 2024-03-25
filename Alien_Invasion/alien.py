import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game) -> None:
        super().__init__()
        self.screen = ai_game.screen
        
        self.settings = ai_game.settings       
        self.image = pygame.image.load('alien_invasion/images/alien.bmp')
        DEFAULT_IMAGE_SIZE = (60, 60)
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)        
        self.rect = self.image.get_rect()
        
        self.rect.x = self.rect.width/2
        self.rect.y = self.rect.height/2
        
        self.x = float(self.rect.x)
        
    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
           return True    
        
