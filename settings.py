class Settings:
    #Settings for Alein Invasion
    
    def __init__(self):
        '''Initialize the Games setting boissss'''
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        
        #Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        
        #bullet babyyyy
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,80,60)
        self.bullets_allowed = 10 #burst fire baby
        
        #ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        #how quickly the game speeds up
        self.speedup_scale = 1.1
        #how quick point value increase
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''initialize settings that change throughtout the gear'''
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        #fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        #score of aliens
        self.alien_points = 50

    def increase_speed(self):
        '''Increase speed settings'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)