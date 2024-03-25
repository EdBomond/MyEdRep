class Settings():
    def __init__(self) -> None:
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5
        self.fullscreen = False
        
        #снаряды
        self.bullet_speed = 0.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 3
        
        #чужие
        self.alien_speed = 0.1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.ship_limit = 3