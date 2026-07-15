import pygame

import src.config.settings as cfg
from src.config.colors import TEXT_COLOR, SHADOW_COLOR


class TextRenderer:
    """
    Helper class to render pygame fonts with outlines and styling.
    """

    def __init__(self):
        pygame.font.init()
        self.fonts = {}

    def _get_font(self, size: int):
        if size not in self.fonts:
            self.fonts[size] = pygame.font.SysFont(cfg.FONT_NAME, size, bold=True)
        return self.fonts[size]

    def render_text(self, text: str, x: float, y: float, surface, color=None, size=None, align="left") -> None:
        if color is None:
            color = TEXT_COLOR
        if size is None:
            size = cfg.DEFAULT_FONT_SIZE

        font = self._get_font(size)

        # Render shadow first
        shadow_surface = font.render(text, True, SHADOW_COLOR)
        shadow_rect = shadow_surface.get_rect()

        # Render main text
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect()

        # Alignment mapping
        offset = cfg.FONT_SHADOW_OFFSET
        if align == "center":
            rect.center = (int(x), int(y))
            shadow_rect.center = (int(x) + offset, int(y) + offset)
        elif align == "right":
            rect.topright = (int(x), int(y))
            shadow_rect.topright = (int(x) + offset, int(y) + offset)
        else:
            rect.topleft = (int(x), int(y))
            shadow_rect.topleft = (int(x) + offset, int(y) + offset)

        surface.blit(shadow_surface, shadow_rect)
        surface.blit(text_surface, rect)