"""
Asset loading utility.
"""
import os
import pygame
from src.utils.exception_logger import ExceptionLogger

import src.config.settings as cfg
from src.config.colors import FALLBACK_IMAGE_COLOR

class ResourceLoader:
    """
    Safely loads images and fonts.
    """
    _image_cache = {}

    @classmethod
    def load_image(cls, file_name: str) -> pygame.Surface:
        if file_name in cls._image_cache:
            return cls._image_cache[file_name]
            
        path = os.path.join(cfg.ASSETS_DIR, cfg.IMAGES_SUBDIR, file_name)
        if not os.path.exists(path):
            # Safe defensive fallback: Create colored shape surface
            surf = pygame.Surface(cfg.FALLBACK_IMAGE_SIZE, pygame.SRCALPHA)
            pygame.draw.circle(surf, FALLBACK_IMAGE_COLOR, (cfg.FALLBACK_IMAGE_RADIUS, cfg.FALLBACK_IMAGE_RADIUS), cfg.FALLBACK_IMAGE_RADIUS)
            cls._image_cache[file_name] = surf
            return surf
            
        try:
            image = pygame.image.load(path).convert_alpha()
            cls._image_cache[file_name] = image
            return image
        except Exception as e:
            ExceptionLogger.log_error(f"Error loading image {file_name}: {str(e)}")
            # Fallback
            surf = pygame.Surface(cfg.FALLBACK_IMAGE_SIZE, pygame.SRCALPHA)
            pygame.draw.circle(surf, FALLBACK_IMAGE_COLOR, (cfg.FALLBACK_IMAGE_RADIUS, cfg.FALLBACK_IMAGE_RADIUS), cfg.FALLBACK_IMAGE_RADIUS)
            cls._image_cache[file_name] = surf
            return surf
