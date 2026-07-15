"""
Asset loading utility.
"""
import os
import pygame
from src.utils.exception_logger import ExceptionLogger

from src.config.settings import ASSETS_DIR, IMAGES_SUBDIR, FALLBACK_IMAGE_SIZE, FALLBACK_IMAGE_RADIUS
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
            
        path = os.path.join(ASSETS_DIR, IMAGES_SUBDIR, file_name)
        if not os.path.exists(path):
            # Safe defensive fallback: Create colored shape surface
            surf = pygame.Surface(FALLBACK_IMAGE_SIZE, pygame.SRCALPHA)
            pygame.draw.circle(surf, FALLBACK_IMAGE_COLOR, (FALLBACK_IMAGE_RADIUS, FALLBACK_IMAGE_RADIUS), FALLBACK_IMAGE_RADIUS)
            cls._image_cache[file_name] = surf
            return surf
            
        try:
            image = pygame.image.load(path).convert_alpha()
            cls._image_cache[file_name] = image
            return image
        except Exception as e:
            ExceptionLogger.log_error(f"Error loading image {file_name}: {str(e)}")
            # Fallback
            surf = pygame.Surface(FALLBACK_IMAGE_SIZE, pygame.SRCALPHA)
            pygame.draw.circle(surf, FALLBACK_IMAGE_COLOR, (FALLBACK_IMAGE_RADIUS, FALLBACK_IMAGE_RADIUS), FALLBACK_IMAGE_RADIUS)
            cls._image_cache[file_name] = surf
            return surf
