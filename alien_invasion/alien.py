import os
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        image_path = os.path.join(os.path.dirname(__file__), 'images', 'alien_ship.jpeg')
        self.image = pygame.image.load(image_path).convert_alpha()

        scale = self.settings.alien_scale
        if scale is not None:
            width = max(1, int(self.image.get_width() * scale))
            height = max(1, int(self.image.get_height() * scale))
            self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.rect = self.image.get_rect()

        # Start each new alien at the exact top-left corner of the screen.
        self.rect.x = 0
        self.rect.y = 0

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
