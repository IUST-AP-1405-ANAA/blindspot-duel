"""
Pygame event processing.
"""
import pygame

class EventHandler:
    """
    Processes raw pygame events and checks window shutdown.
    """

    def __init__(self):
        self.is_window_open = True

    def poll_events(self) -> list:
        """Fetch and process events from pygame.event.get()."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.is_window_open = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
        return events
