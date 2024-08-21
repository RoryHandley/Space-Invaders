import pygame.font #Because Scoreboard writes text to the screen, we begin by importing the pygame.font module. 
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats #Next, we give __init__() the ai_game parameter so it can access the settings, screen, and stats objects, which it will need to report the values we’re tracking

        # Font settings for scoring information.
        self.text_color = (30, 30, 30) # Then we set a text color
        self.font = pygame.font.SysFont(None, 48) #and instantiate a font object

        # Prepare the initial score images.
        self.prep_score() #To turn the text to be displayed into an image, we call prep_score()
        self.prep_high_score() #The high score will be displayed separately from the score, so we need a new method, prep_high_score(), to prepare the high-score image
        self.prep_level() #To have Scoreboard display the current level
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1) #round function rounds a float to a set number of decimal places given as the second argument. However, when you pass a negative number as the second argument, round() will round the value to the nearest 10, 100, 1,000, and so on. E.g -1 rounds to the nearest 10, -2 rounds to the nearest 100, -3 rounds to the nearest 1000. This code tells Python to round the value of stats.score to the nearest 10 and assign it to rounded_score.
        score_str = f"Current Score: {rounded_score:,}" #We then use a format specifier in the f-string for the score. A format specifier is a special sequence of characters that modifies the way a variable’s value is presented. In this case the sequence :, tells Python to insert commas at appropriate places in the numerical value that’s provided. This specific format operator addes commas as thousands seperators, so this results in strings like 1,000,000 instead of 1000000.
        self.score_image = self.font.render(score_str, True,self.text_color, self.settings.bg_colour) #and then pass this string to render(), which creates the image. To display the score clearly onscreen, we pass the screen’s background color and the text color to render().

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect() # To make sure the score always lines up with the right side of the screen, we create a rect called score_rect
        self.score_rect.right = self.screen_rect.right - 20 #and set its right edge 20 pixels from the right edge of the screen
        self.score_rect.top = 20 #We then place the top edge 20 pixels down from the top of the screen

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1) #round the high score to the nearest 10 
        high_score_str = f"High Score: {high_score:,}" #and format it with commas
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_colour) #We then generate an image from the high score 

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx #center the high score rect horizontally
        self.high_score_rect.top = self.score_rect.top #set its top attribute to match the top of the score image

    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect) #This method draws the score image onscreen at the location score_rect specifies.
        self.screen.blit(self.high_score_image, self.high_score_rect) #Draws the high score at the top center of the screen.
        self.screen.blit(self.level_image, self.level_rect) #draws the level image to the screen
        self.ships.draw(self.screen) #To display the ships on the screen, we call draw() on the group, and Pygame draws each ship.

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score() #f the current score is greater, we update the value of high_score and call prep_high_score() to update the high score’s image.

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(f"Level: {self.stats.level}") 
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_colour) #Creates an image from the value stored in stats.level

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right #sets the image’s right attribute to match the score’s right attribute 
        self.level_rect.top = self.score_rect.bottom + 10 #sets the top attribute 10 pixels beneath the bottom of the score image to leave space between the score and the level 

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group() #creates an empty group, self.ships, to hold the ship instances
        for ship_number in range(self.stats.ships_left): #To fill this group, a loop runs once for every ship the player has left
            ship = Ship(self.ai_game) #Create a new ship
            ship.rect.x = 10 + ship_number * ship.rect.width #and set each ship’s x-coordinate value so the ships appear next to each other with a 10-pixel margin on the left side of the group of ships
            ship.rect.y = 10 #set the y-coordinate value 10 pixels down from the top of the screen so the ships appear in the upper-left corner of the screen
            self.ships.add(ship) #add each new ship to the group ships