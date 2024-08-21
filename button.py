import pygame.font #module which lets Pygame render text to the screen. 

class Button:
    """A class to build buttons for the game."""

    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48) #creates a font object with the system default font and a size of 48 pixels

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center # create a rectangular object (self.rect) for the button using pygame.Rect(). The rectangle is initially positioned at (0, 0) and has the dimensions specified by self.width and self.height. Then, the center attribute of self.rect is set to the center of the screen (self.screen_rect.center), which centers the button on the screen.

        # The button message needs to be prepped only once.
        self._prep_msg(msg) #Pygame works with text by rendering the string you want to display as an image. Finally, we call _prep_msg() to handle this rendering
    
    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color) #The call to font.render() turns the text stored in msg into an image, which we then store in self.msg_image. The font.render() method also takes a Boolean value to turn antialiasing on or off (antialiasing makes the edges of the text smoother). The remaining arguments are the specified font color and background color. 
        self.msg_image_rect = self.msg_image.get_rect() #We center the text image on the button by creating a rect from the image 
        self.msg_image_rect.center = self.rect.center #and setting its center attribute to match that of the button

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect) #We call screen.fill() to draw the rectangular portion of the button.
        self.screen.blit(self.msg_image, self.msg_image_rect) #Then we call screen.blit() to draw the text image to the screen, passing it an image and the rect object associated with the image. 