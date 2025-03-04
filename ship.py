import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''A class to manage a ship'''

    def __init__(self,ai_game):
        super().__init__()
        '''ship at start captain'''
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        #using rectangles cause they easy and me am lazy af

        #load the pic bero
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #drop it to the ground
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a float for the ship's exact hori posi
        self.x = float(self.rect.x)

        #MOvement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''update movement based on flag'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed


        #update rect objects from self.x
        self.rect.x = self.x

    def blitme(self):
        #draw boom at current
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect. midbottom
        self.x = float(self.rect.x)
        