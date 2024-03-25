import sys
from time import sleep
import pygame
from setting import Settings
from game_stat import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    def __init__(self) -> None:
        pygame.init()
        self.settings=Settings()
        if self.settings.fullscreen == False:
           self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        else:
           self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
           self.settings.screen_width = self.screen.get_rect().width
           self.settings.screen_height = self.screen.get_rect().height    
        pygame.display.set_caption("Вторжение инопланетян!")
        self.stats = GameStats(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
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
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()    

    def _check_keyup_events(self, event):                    
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False    
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False 
                                     
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()          
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)    
        pygame.display.flip() 
    
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed: 
           new_bullet = Bullet(self)
           self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)           
    
    def _check_collisions(self):
       collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)            
       
    def _check_fleet_empty(self):
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()   
                      
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_spase_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x =available_spase_x // (2 * alien_width)
        
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -(3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
           for alien_number in range(number_aliens_x):
               self._create_alien(alien_number, row_number, alien_width)
            
            
    def _create_alien(self, alien_number, row_number, alien_width):
        alien = Alien(self)
        alien.x = alien_width+2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)                  
    
    def _update_aliens(self):
        self.aliens.update()
        
    def _check_collisions_ship(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
           print("Корабль сбит пришельцами!!!")
           self._ship_hit() 
        self._check_aliens_bottom()
    
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 
            
    def _ship_hit(self):
      if self.stats.ship_left > 0:  
        self.stats.ships_left -= 1
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        sleep(1)
      else:
        self.stats.game_active = False    
    
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break    
        
    def run_game(self):
        while True:
            self._chek_events()
            if self.stats.game_active:
              self.ship.update()
              self._update_bullets()
              self._check_collisions()
              self._check_fleet_empty()
              #print(len(self.bullets))        
              self._check_fleet_edges()
              self._update_aliens()
              self._check_collisions_ship()
            self._update_screen()
            
            
if __name__ == '__main__':
    ai=AlienInvasion()
    ai.run_game()                        