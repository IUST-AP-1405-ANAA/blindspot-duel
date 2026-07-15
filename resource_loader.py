import os
import pygame
from pathlib import Path
from typing import Dict

from src.utils.exception_logger import Logger


class ResourceLoader:
    
    _image_cache: Dict[str, pygame.Surface] = {}
    _sound_cache: Dict[str, pygame.mixer.Sound] = {}
    _font_cache: Dict[str, pygame.font.Font] = {}
    
    _assets_dir = Path("assets")
    _initialized = False
    
    @classmethod
    def _initialize(cls):
        if cls._initialized:
            return
        
        pygame.init()
        cls._initialized = True
        Logger.info("ResourceLoader initialized")
    
    @classmethod
    def load_image(cls, filename: str) -> pygame.Surface:
        cls._initialize()
        
        if filename in cls._image_cache:
            return cls._image_cache[filename]
        
        image_path = cls._assets_dir / "images" / filename
        
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        try:
            image = pygame.image.load(str(image_path)).convert_alpha()
            cls._image_cache[filename] = image
            Logger.info(f"Image loaded: {filename}")
            return image
        except Exception as e:
            Logger.error(f"Failed to load image {filename}: {str(e)}")
            raise
    
    @classmethod
    def load_sound(cls, filename: str) -> pygame.mixer.Sound:
        """لود صدا"""
        cls._initialize()
        
        if filename in cls._sound_cache:
            return cls._sound_cache[filename]
        
        sound_path = cls._assets_dir / "sounds" / filename
        
        if not sound_path.exists():
            raise FileNotFoundError(f"Sound not found: {sound_path}")
        
        try:
            sound = pygame.mixer.Sound(str(sound_path))
            cls._sound_cache[filename] = sound
            Logger.info(f"Sound loaded: {filename}")
            return sound
        except Exception as e:
            Logger.error(f"Failed to load sound {filename}: {str(e)}")
            raise
    
    @classmethod
    def load_font(cls, filename: str, size: int) -> pygame.font.Font:

        cls._initialize()
        
        cache_key = f"{filename}_{size}"
        
        if cache_key in cls._font_cache:
            return cls._font_cache[cache_key]
        
        font_path = cls._assets_dir / "fonts" / filename
        
        if not font_path.exists():
            raise FileNotFoundError(f"Font not found: {font_path}")
        
        try:
            font = pygame.font.Font(str(font_path), size)
            cls._font_cache[cache_key] = font
            Logger.info(f"Font loaded: {filename} size {size}")
            return font
        except Exception as e:
            Logger.error(f"Failed to load font {filename}: {str(e)}")
            raise