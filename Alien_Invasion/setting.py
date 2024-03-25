class Settings():
    def __init__(self) -> None:
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5
        self.fullscreen = True
        
        #снаряды
        self.bullet_speed = 0.5
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 3
        
        #чужие
        self.alien_speed = 0.1
        self.fleet_drop_speed = 100
        self.fleet_direction = 1
        self.ship_limit = 2
        self.speedup_scale = 1.2
        self.score_scale = 1.5
        
        
        self.init_dyn_settings()
        
    def init_dyn_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 1.0
        self.alien_points = 50
        self.fleet_direction = 1
    
    def increase_speed(self):
        self.ship_speed_factor *= self.ship_speed_factor
        self.bullet_speed_factor *= self.bullet_speed_factor
        self.alien_speed_factor *= self.alien_speed_factor 
        self.alien_points = int(self.alien_points * self.score_scale)
        
            