"""
Maps raw inputs to logical game actions.
"""
import pygame
from src.config.keybinds import P1_KEYS, P2_KEYS

class InputMapper:
    """
    Translates keyboard keys to abstract commands (e.g., P1_SHOOT).
    """

    def map_inputs(self, events: list) -> dict:
        """Returns the dictionary of active game actions mapped from keys."""
        keys = pygame.key.get_pressed()
        
        # Vector movements
        p1_dx = 0
        p1_dy = 0
        if keys[P1_KEYS["LEFT"]]: p1_dx -= 1
        if keys[P1_KEYS["RIGHT"]]: p1_dx += 1
        if keys[P1_KEYS["UP"]]: p1_dy -= 1
        if keys[P1_KEYS["DOWN"]]: p1_dy += 1
        
        p2_dx = 0
        p2_dy = 0
        if keys[P2_KEYS["LEFT"]]: p2_dx -= 1
        if keys[P2_KEYS["RIGHT"]]: p2_dx += 1
        if keys[P2_KEYS["UP"]]: p2_dy -= 1
        if keys[P2_KEYS["DOWN"]]: p2_dy += 1

        # Check for shoot trigger events
        p1_shoot = False
        p2_shoot = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == P1_KEYS["SHOOT"]:
                    p1_shoot = True
                elif event.key == P2_KEYS["SHOOT"]:
                    p2_shoot = True

        return {
            "p1_move": (p1_dx, p1_dy),
            "p2_move": (p2_dx, p2_dy),
            "p1_shoot": p1_shoot,
            "p2_shoot": p2_shoot,
            "raw_events": events
        }
