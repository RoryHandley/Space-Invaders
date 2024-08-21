import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self,ai_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #Load the alien image and set it's rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width #We initially place each alien near the top-left corner of the screen; we add a space to the left of it that’s equal to the alien’s width and a space above it equal to its height, so it’s easy to see. Note new_alien.x represents the horizontal position (x-coordinate) of the alien object independently of its associated rectangle (rect). The new_alien.rect.x attribute represents the horizontal position (x-coordinate) of the alien's rectangle.
        self.rect.y = self.rect.height

        #Store the alien's exact horizontal position.
        self.x = float(self.rect.x) #We’re mainly concerned with the aliens’ horizontal speed, so we’ll track the horizontal position of each alien precisely

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0) #The alien is at the right edge if the right attribute of its rect is greater than or equal to the right attribute of the screen’s rect. It’s at the left edge if its left value is less than or equal to 0. Rather than put this conditional test in an if block, we put the test directly in the return statement. This method will return True if the alien is at the right or left edge, and False if it is not at either edge.

    def update(self):
        """Move the alien right or left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction #allow motion to the left or right by multiplying the alien’s speed by the value of fleet_direction. If fleet_direction is 1, the value of alien_speed will be added to the alien’s current position, moving the alien to the right; if fleet_direction is −1, the value will be subtracted from the alien’s position, moving the alien to the left.
        self.rect.x = self.x

