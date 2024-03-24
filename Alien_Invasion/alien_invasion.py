import sys
import pygame
from setting import Settings
from ship import Ship

class AlienInvasion:
    def __init__(self) -> None:
        pygame.init()
        self.settings=Settings()
        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Вторжение инопланетян!")
        self.ship = Ship(self)
      
        
        
    def _chek_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)  
                elif event.type == pygame.KEYUP:       
                    self._check_keyup_events(event)                           
    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_q
            sys.exit()                                  

    def _check_keyup_events(self, event):                    
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False    
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False 
                                     
    def _update_screen(self):
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()          
            pygame.display.flip() 
                      
    def run_game(self):
        while True:
            self._chek_events()
            self.ship.update()
            self._update_screen()
            
            
if __name__ == '__main__':
    ai=AlienInvasion()
    ai.run_game()                        