class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats() #we’ll need to reset some statistics each time the player starts a new game. To do this, we’ll initialize most of the statistics in the reset_stats() method, instead of directly in __init__(). We’ll call this method from __init__() so the statistics are set properly when the GameStats instance is first created. But we’ll also be able to call reset_stats() anytime the player starts a new game. 
        #Because the high score should never be reset, we initialize high_score in __init__() rather than in reset_stats().
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1