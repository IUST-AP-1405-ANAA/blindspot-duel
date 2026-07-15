import pygame
import math
from blindspot_duel.contracts.i_renderable import IRenderable
from blindspot_duel.ui.components.text_renderer import TextRenderer
from blindspot_duel.config.settings import (
    WIDTH, HEIGHT, GRID_SPACING, GRID_LINE_WIDTH, GLOW_DIVISOR,
    GLOW_RADIUS_OFFSET, GLOW_RING_WIDTH, ENTITY_BORDER_WIDTH,
    CENTER_DOT_RADIUS, DEFAULT_FONT_SIZE
)
from blindspot_duel.config.colors import GRID_COLOR, CENTER_DOT_COLOR, TEXT_COLOR


class PygameRenderer(IRenderable):
    """
    Draws styled elements on pygame screen.
    """

    def __init__(self, screen_surface):
        self.screen = screen_surface
        self.text_renderer = TextRenderer()

    def clear_screen(self, color: tuple) -> None:
        # Fill background with the given color
        self.screen.fill(color)

        # Draw cyber grid lines
        grid_spacing = GRID_SPACING
        grid_color = GRID_COLOR  # Faint cyber grid lines

        for x in range(0, WIDTH, grid_spacing):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, HEIGHT), GRID_LINE_WIDTH)
        for y in range(0, HEIGHT, grid_spacing):
            pygame.draw.line(self.screen, grid_color, (0, y), (WIDTH, y), GRID_LINE_WIDTH)

    def draw_entity(self, x: float, y: float, radius: float, color: tuple, is_visible: bool = True) -> None:
        if not is_visible:
            return

        # Draw dynamic concentric neon glow
        glow_color = (color[0] // GLOW_DIVISOR, color[1] // GLOW_DIVISOR, color[2] // GLOW_DIVISOR)
        pygame.draw.circle(self.screen, glow_color, (int(x), int(y)), int(radius + GLOW_RADIUS_OFFSET), GLOW_RING_WIDTH)
        pygame.draw.circle(self.screen, color, (int(x), int(y)), int(radius), ENTITY_BORDER_WIDTH)
        pygame.draw.circle(self.screen, CENTER_DOT_COLOR, (int(x), int(y)), CENTER_DOT_RADIUS)

    def draw_ui_text(self, text: str, x: float, y: float, color: tuple = None, size: int = None, align: str = "left") -> None:
        if color is None:
            color = TEXT_COLOR
        if size is None:
            size = DEFAULT_FONT_SIZE
        self.text_renderer.render_text(text, x, y, self.screen, color, size, align)

    def flip_buffer(self) -> None:
        pygame.display.flip()