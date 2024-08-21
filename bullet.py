import pygame
from pygame.sprite import Sprite #from the sprite module in Pygame, import the Sprite Class

class Bullet(Sprite): #This indicates that the class being defined (in this case, Bullet) is inheriting from the parent class (Sprite).
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game): #The method takes two parameters: self, which refers to the instance of the class being created, and ai_game, which is an object representing the current instance of the game.
        """Create a bullet object at the ship's current position"""
        super().__init__() #This line calls the constructor of the parent class. It ensures that any necessary setup in the parent class (Sprite) is performed before executing the code in the current constructor.
        self.screen = ai_game.screen #Assign the values of ai_game.screen and ai_game.settings to the self.screen and self.settings attributes, respectively. These attributes allow the bullet object to access the screen and game settings from the ai_game object.
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color #This line assigns the value of self.settings.bullet_color to the self.color attribute. It retrieves the bullet color from the game settings and stores it in the bullet object.

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height) #These lines create a rectangle object (self.rect) using the pygame.Rect() constructor. The rectangle's width and height are set to the values specified in self.settings.bullet_width and self.settings.bullet_height, respectively. 
        self.rect.midtop = ai_game.ship.rect.midtop #The midtop attribute of self.rect is then set to the midtop attribute of the ship's rectangle (ai_game.ship.rect.midtop), positioning the bullet at the top center of the ship.

        # Store the bullet's position as a float.
        self.y = float(self.rect.y) #This line converts the self.rect.y attribute (the vertical position of the bullet) to a float and assigns it to the self.y attribute. This allows for more precise positioning and movement calculations.

    def update(self):
        """Move the bullet up the screen."""
        # Update the exact position of the bullet.
        self.y -= self.settings.bullet_speed #When a bullet is fired, it moves up the screen, which corresponds to a decreasing y-coordinate value. To update the position, we subtract the amount stored in settings.bullet_speed from self.y. Once a bullet is fired, we never change the value of its x-coordinate, so it will travel vertically in a straight line even if the ship moves.
        # Update the rect position.
        self.rect.y = self.y #We then use the value of self.y to set the value of self.rect.y 

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect) #fills the part of the screen defined by the bullet’s rect with the color stored in self.color