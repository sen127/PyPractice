class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 566
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        # Ship settings
        self.ship_scale = 0.03  # Percentage of original bitmap size
        self.ship_speed = 1.5

        # Alien settings
        self.alien_scale = 0.03
        self.alien_speed = 1.0
        self.fleet_drop_speed = 1
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Bullet Settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 115, 255)
        self.bullets_allowed = 100
