import sys
from time import sleep #We import the sleep() function from the time module in the Python standard library, so we can pause the game for a moment when the ship is hit. 

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button


class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self): #Constructor method of Class. Used to initialize the object's attributes and perform any necessary setup or configuration. The self parameter refers to the instance of the class that is being created and allows you to access and modify its attributes and methods
        """Initialize the game and create game resources"""
        pygame.init() #initializes all the modules required for Pygame to work properly. It initializes various aspects of the game, such as the display, sound, and joystick, and prepares them for use. By calling pygame.init() at the beginning of the class's constructor, it ensures that all the necessary Pygame modules are initialized before setting up the game resources and creating the game window.
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #When creating the screen surface, we pass a size of (0, 0) and the parameter pygame.FULLSCREEN. This tells Pygame to figure out a window size that will fill the screen.
        self.settings.screen_width = self.screen.get_rect().width #Because we don’t know the width and height of the screen ahead of time, we update these settings after the screen is created
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self) #Make instance of Ship after screen has been created. Ship class has two arguements (self, ai_game). So in that case, we need to provide an attribute for ai_game. I think using 'self' in this case means that an instance of AlienInvasion will be provided as the ai_game arguement. 
        self.bullets = pygame.sprite.Group() #create the group that holds the bullets
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an active state.
        self.game_active = False

        # Make the Play button.
        self.play_button = Button(self, "Play") #"Play" will be the msg arguement for Button. I think the current game instance will be (ai_game) (self = ai_game, "play" = msg)

    
    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            
            if self.game_active:
                self.ship.update() #The ship’s position will be updated AFTER we’ve checked for keyboard events and BEFORE we update the screen. This allows the ship’s position to be updated in response to player input and ensures the updated position will be used when drawing the ship to the screen.
                self._update_bullets()
                self._update_aliens() #We update the aliens’ positions after the bullets have been updated, because we’ll soon be checking to see whether any bullets hit any aliens.

            self._update_screen()
            self.clock.tick(60) #Used to control the frame rate of te game (60FPS). By calling self.clock.tick(60), the clock object limits the game loop to run at a maximum of 60 iterations per second. The argument 60 passed to tick() represents the desired frame rate in FPS. It instructs the clock object to delay the loop execution if necessary to maintain the specified frame rate. If the loop iteration takes less time than expected for a given frame rate, tick() will introduce a delay to keep the loop running at a consistent pace.

    def _check_events(self): #A helper method does work inside a class but isn’t meant to be used by code outside the class. In Python, a single leading underscore indicates a helper method.
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get(): #pygame.event.get() retrieves a list of events that have occurred since the last time this function was called. The loop iterates over each event in the list obtained in the previous step
                if event.type == pygame.QUIT:
                    sys.exit() #If the event type is pygame.QUIT, it means the user is trying to close the window. In response to this event, the code calls sys.exit(). This function is part of the sys module and is used to exit the Python program, terminating the application.
                elif event.type == pygame.KEYDOWN: #If pygame detects a keydown event
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP: #When right key is released, set moving flag = False. 
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN: #Pygame detects a MOUSEBUTTONDOWN event when the player clicks anywhere on the screen, but we want to restrict our game to respond to mouse clicks only on the Play button.
                    mouse_pos = pygame.mouse.get_pos() #To accomplish this, we use pygame.mouse.get_pos(), which returns a tuple containing the mouse cursor’s x- and y-coordinates when the mouse button is clicked
                    self._check_play_button(mouse_pos) #We send these values to the new method _check_play_button()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos) #We use the rect method collidepoint() to check whether the point of the mouse click overlaps the region defined by the Play button’s rect. If so, we set game_active to True, and the game begins! The flag button_clicked stores a True or False value , and the game will restart only if Play is clicked and the game is not currently active.
        if button_clicked and not self.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings() #Need to reset speed everytime the game starts again.
            # Reset the game statistics.
            self.stats.reset_stats() #We reset the game statistics, which gives the player three new ships. 
            self.sb.prep_score() #We call prep_score() after resetting the game stats when starting a new game. This preps the scoreboard with a score of 0.
            self.sb.prep_level() #We call prep_level() when the player clicks the Play button to ensure the level image updates properly at the start of a new game.
            self.sb.prep_ships() #To show the player how many ships they have to start with, we call prep_ships() when a new game starts.
            self.game_active = True

            #Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            #Hide the mouse cursor
            pygame.mouse.set_visible(False)
                    
    def _check_keydown_events(self,event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT: #if the key pressed is the right arrow key
            self.ship.moving_right = True #Set moving flag = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q: #If user presses Q, game will close. 
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False 
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self) #creates a new instance of the Bullet class by calling its constructor. 
            self.bullets.add(new_bullet) #self.bullets refers to a group (or container) of bullet objects. The line adds the newly created new_bullet object to this group using the add() method. By adding the bullet to the group, it becomes part of the collection of bullets that will be updated and drawn in the game.

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update() #When you call update() on a group, the group automatically calls update() for each sprite in the group. The line self.bullets.update() calls bullet.update() for each bullet we place in the group bullets
        # Get rid of bullets that have disappeared.

        for bullet in self.bullets.copy(): #When you use a for loop with a list (or a group in Pygame), Python expects that the list will stay the same length as long as the loop is running. That means you can’t remove items from a list or group within a for loop, so we have to loop over a copy of the group. We use the copy() method to set up the for loop ❶, which leaves us free to modify the original bullets group inside the loop.
            if bullet.rect.bottom <= 0: #If bottom of bullet has just moved off the top of the screen.
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True) #compares the positions of all the bullets in self.bullets and all the aliens in self.aliens, and identifies any that overlap. Whenever the rects of a bullet and alien overlap, groupcollide() adds a key-value pair to the dictionary it returns. The two True arguments tell Pygame to delete the bullets and aliens that have collided. E.g. if you wanted a bullet to not disappear and keep killing aliens until the end of the screen, you would use "False, True" arguements. 

        if collisions: #When a bullet hits an alien, Pygame returns a collisions dictionary. We check whether the dictionary exists, and if it does, the alien’s value is added to the score.
            for aliens in collisions.values(): #Each value in the dictionary is a list of aliens that were hit by a single bullet. The key in the dictionary corresponds to the bullet that caused the collisions. E.g. the dictionary would look like below:
                #collisions = {
                # bullet1: [alien1, alien2, alien3], bullet1 caused collisions with alien1, alien2, and alien3.
                # bullet2: [alien4, alien5],
                # bullet3: [alien6]
                #}
                self.stats.score += self.settings.alien_points * len(aliens) #We multiply the value of each alien by the number of aliens in each list and add this amount to the current score. 
            self.stats.score += self.settings.alien_points
            self.sb.prep_score() #We then call prep_score() to create a new image for the updated score.
            self.sb.check_high_score() #We need to call check_high_score() each time an alien is hit after updating the score

        if not self.aliens: #Executes if alien group is empty
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed() #Increase speed once player has cleared alien fleet. 

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level() #If a fleet is destroyed, we increment the value of stats.level and call prep_level() to make sure the new level displays correctly

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1 ## Decrement ships_left
            self.sb.prep_ships() #and update scoreboard. We call prep_ships() after decreasing the value of ships_left, so the correct number of remaining ships displays each time a ship is destroyed.
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            #pauses program execution for half a second, long enough for the player to see that the alien has hit the ship.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _update_aliens(self):
        """Update the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens): #two arguments: a sprite and a group. looks for any member of the group that has collided with the sprite and stops looping through the group as soon as it finds one member that has collided with the sprite. loops through the group aliens and returns the first alien it finds that has collided with ship
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.Spacing between aliens is one alien width.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self) #Create new instance of Alien class called alien. Represents a single alien in the fleet. 
        alien_width, alien_height = alien.rect.size #A rect’s size attribute is a tuple containing its width and height respectively
        
        current_x, current_y = alien_width, alien_height #get the alien’s width from the first alien we created, and then define a variable called current_x
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width): #continues until the value of current_x is less than the screen width minus twice the alien width. This condition ensures that the fleet of aliens is created within the game screen boundaries, leaving enough space for each alien.
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width #We add two alien widths to the horizontal position, to move past the alien we just added and to leave some space between the aliens as well. Python will re-evaluate the condition at the start of the while loop and decide if there’s room for another alien. When there’s no room left, the loop will end, and we should have a full row of aliens.

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

        self.aliens.add(alien)

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self) # Create new instance of alien class called new_alien
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges(): #If check_edges() returns True, we know an alien is at an edge and the whole fleet needs to change direction
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self): #loop through all the aliens and drop each one using the setting fleet_drop_speed
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 #then we change the value of fleet_direction by multiplying its current value by −1. The line that changes the fleet’s direction isn’t part of the for loop. We want to change each alien’s vertical position, but we only want to change the direction of the fleet once

    def _update_screen(self):
        """Update images on the screen and flip to the new screen"""
        self.screen.fill(self.settings.bg_colour)
        for bullet in self.bullets.sprites(): #iterates over each bullet object in the self.bullets group. The sprites() method is called on the self.bullets group, which returns a list of all the sprite objects (bullets) contained within the group
            bullet.draw_bullet() 
        self.ship.blitme() #Draw ship on screen
        self.aliens.draw(self.screen) #used to draw all the alien objects in the self.aliens group onto the game screen (self.screen). The draw() method is a built-in method provided by the pygame.sprite.Group class. In this case, self.aliens.draw() is called with the argument self.screen, which represents the game screen surface. By calling self.aliens.draw(self.screen), the draw() method iterates over each alien object in the self.aliens group and renders or blits their respective images onto the game screen.

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active: #To make the Play button visible above all other elements on the screen, we draw it after all the other elements have been drawn but before flipping to a new screen.
            self.play_button.draw_button()
    
        pygame.display.flip() #Pygame uses two buffers: a front buffer and a back buffer. The front buffer is the one displayed on the screen, while the back buffer is where changes are made before being displayed. When pygame.display.flip() is called, the contents of the back buffer are swapped with the front buffer, making the updated frame visible to the user.


if __name__ == '__main__': #checks whether the current module is being run as the main program or if it is being imported as a module. When a Python module is run directly as the main     program (i.e., it is not imported by another module), the special variable __name__ is set to '__main__'. if a module is imported by another module, the value of __name__ is set to the module's name.
    #Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
