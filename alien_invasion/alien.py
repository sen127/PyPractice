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

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self):
        """Move the alien to the right or left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x