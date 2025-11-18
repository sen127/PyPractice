import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()  # This turns on all pygame systems; think of it as powering up the engine before using it
        
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.fire_button_held = False
        self.last_shot_time = 0
        self.fire_delay = 150  # milliseconds between shots while the key is held

    def run_game(self):  # Self is the object's memory backpack so the game can access its own data
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._handle_continuous_fire()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _handle_continuous_fire(self):
        """Fire bullets repeatedly while the spacebar is held down."""
        if not self.fire_button_held:
            return
        self._fire_bullet()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_button_held = True
            self._fire_bullet(force=True)

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            self.fire_button_held = False

    def _fire_bullet(self, force=False):
        """Create a new bullet and add it to the bullets group."""
        current_time = pygame.time.get_ticks()
        if not force and current_time - self.last_shot_time < self.fire_delay:
            return
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        self.last_shot_time = current_time

    def _update_bullets(self):
        """Move bullets and remove ones that leave the screen."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()

        pygame.display.flip()


if __name__ == '__main__':  # This ensures the game runs only when this file is executed directly, not when imported
    # Make a game instance, and run the game.
    ai = AlienInvasion()   # Creating the object automatically triggers __init__ which sets up the game room
    ai.run_game()          # This is the heartbeat loop that keeps the game alive
