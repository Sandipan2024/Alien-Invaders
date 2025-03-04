'''Alien Invasion by Sandipan Bhattacharjee
Alein invasion game making start date 28/2/25 expected completion date 3/3/25.
1. first main instance along with display created and running succesfully.[28/2/23-08:01]
2. Added a new settings module for game settings such as height,width,bg_color[test running successfully]
3. Added ship and made it move left and right along with firing bullets
4. added fleet of alien ships.
5. made the fleet move.
6. Made sure bullet collisions delete aliens.
7. Repopulate the aliens.
8.speed uip bullets and add game over mechanics.
'''




import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import ScoreBoard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    '''Overall class to manage game assets and resources'''


    def __init__(self):
    #initialize and create resources
        pygame.init()
        self.settings = Settings()


        #create a frame rate clock
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption("Alien Invasion by Sandipan Bhattacharjee")

        #Create instance to store game stats
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #self Alien Invasion
        self.game_active = False
        self.play_button = Button(self,"PLAY")
    


    def run_game(self):
        '''Start main loop of game'''

        while True:
            #watch for events
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            self.clock.tick(60)


    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        #look for boom boom
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #look for aliens hitting the bottom of the screeen
        self._check_aliens_bottom()


    def _update_bullets(self):
            self.bullets.update()
        #delete the fired bullets
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <=0:
                    self.bullets.remove()
            
            self._check_bullet_alien_collisions()
            
    #ship hit behaviour
    def _ship_hit(self):
        '''hit by alien'''
        if self.stats.ships_left > 0:
            self.stats.ships_left -=1
            self.sb.prep_ships()
            #Get rid of amy remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            #Create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)

    
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            #Reset the game statistics
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            #get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            #hide the mouse cursor
            pygame.mouse.set_visible(False)
    
    #func for key press
    def _check_keydown_events(self,event):
            if event.key == pygame.K_RIGHT:
                        #move sight to right
                self.ship.rect.x +=1
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()

    def _check_bullet_alien_collisions(self):
        #remove bullets and aliens who collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
                #destroy existing bullets and crete new fleet
                self.bullets.empty()
                self._create_fleet()
                self.settings.increase_speed()
                self.stats.level +=1
                self.sb.prep_level()



    #func for key up
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False


    '''create a new bullet and add to magazine'''
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    #updates the screen dear
    def _update_screen(self):
        '''Update images on screen, and flip to the new naweli screen'''
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
            #most recently drawn screen visible
        pygame.display.flip()


    #what do you think it does genius
    def _create_fleet(self):
        '''Create the fleet of aliens'''
        #make alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y <(self.settings.screen_height - 3*alien_height):
            while current_x < (self.settings.screen_width - 2* alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    #does exactly what it says
    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x =x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    #checks if fleet touched the edge of screen
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    #changes fleet direction
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y +=  self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    #check if any fleet reach bottom of screen
    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #treat same as if ship got hit
                self._ship_hit()
                break


if __name__ == '__main__':
    #make a game instance
    ai=AlienInvasion()
    ai.run_game()