import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set it's starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings #assigning the settings attribute of the ai_game object (self.ship = Ship(self)) to the settings attribute of the current object (instance) being initialized.
        self.screen_rect = ai_game.screen.get_rect()

        #Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp') #load an image file (ship.bmp) using pygame.image.load() and assign the loaded image to the image attribute of the ship instance. 
        self.rect = self.image.get_rect() #The get_rect() method is then called on the image object to get the rectangle that encloses the ship image. This rectangle is assigned to the rect attribute of the ship instance. 
        #The get_rect() method returns a Rect object, which is a rectangle that represents the dimensions and position of the surface. This rectangle contains attributes such as x, y, width, and height that define the position and size of the surface.
        #In the context of Pygame, a Surface is an object that represents a rectangular area of a window or screen where you can draw graphical elements, such as images, shapes, or text.A Surface can be thought of as a blank canvas that you can draw on using various Pygame functions and methods. 

        #Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom #assigns the midbottom attribute of the ship's rectangle (self.rect) to the midbottom attribute of the game screen's rectangle (self.screen_rect).
        #The .midbottom attribute of a rectangle refers to the x, y coordinates of the middle point at the bottom edge of the rectangle. By assigning self.screen_rect.midbottom to self.rect.midbottom, the code is aligning the bottom center of self.rect with the bottom center of the screen. This assignment updates the position of self.rect and ensures that the object associated with it is initially positioned at the bottom center of the screen.

        #Store a float for the ship's exact horizontal position. rect x is stored as integer by default so this is necessary.
        self.x = float(self.rect.x) #rect.x only takes an integer value, so we need an intermim variable to be able to reference to be able to move the ship by fractions of a pixel (i.e. a float).

        self.moving_right = False #Movement flag; start with a ship that's not moving. 
        self.moving_left = False

    def update(self): #The update() method will be called from outside the class, so it’s not considered a helper method.
        """Update ship's position based on the movement flag"""
        #Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right: #If self.moving_right == True and not at right edge of screen. self.rect.right returns the x-coordinate of the right edge of the ship’s rect.
            self.x += self.settings.ship_speed #the ship's self.x attribute is incremented by the value of self.settings.ship_speed. This updates the ship's horizontal position to move it to the right.
        if self.moving_left and self.rect.left > 0: #self.rect.left returns the x-coordinate of the left edge of the ship’s rect. If greater than zero, it's not at left edge.
             self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x #We then set the interim variable self.x = to value of rect.x. rect will only keep intreger portion of that value, but that's fine for displaying the ship. This part ensures that the rectangle representing the ship's position (self.rect) is synchronized with the updated self.x position. By updating self.rect.x, the ship's visual representation on the screen can be correctly drawn or rendered at the updated position.

    def blitme(self):
        """Draw the ship at it's current location"""
        self.screen.blit(self.image, self.rect) #uses the blit() method of the game screen (self.screen) to blit (i.e., draw) the ship's image (self.image) onto the screen at the ship's rectangle position (self.rect).

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

