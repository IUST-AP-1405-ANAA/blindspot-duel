import pygame
from typing import Dict

from src.utils.exception_logger import Logger
from src.utils.resource_loader import ResourceLoader


class AudioManager:

    CHANNEL_MUSIC = 0
    CHANNEL_SFX = 1
    CHANNEL_UI = 2

    _initialized = False
    _channels: Dict[int, pygame.mixer.Channel] = {}

    @classmethod
    def _initialize(cls):
        if cls._initialized:
            return

        try:
            pygame.mixer.init()
            pygame.mixer.set_num_channels(3)

            cls._channels[cls.CHANNEL_MUSIC] = pygame.mixer.Channel(cls.CHANNEL_MUSIC)
            cls._channels[cls.CHANNEL_SFX] = pygame.mixer.Channel(cls.CHANNEL_SFX)
            cls._channels[cls.CHANNEL_UI] = pygame.mixer.Channel(cls.CHANNEL_UI)

            cls._initialized = True
            Logger.info("AudioManager initialized")
        except Exception as e:
            Logger.error(f"Failed to initialize AudioManager: {str(e)}")

    @classmethod
    def play_sfx(cls, sound_name: str):

        cls._initialize()

        try:
            sound = ResourceLoader.load_sound(sound_name)
            cls._channels[cls.CHANNEL_SFX].play(sound)
            Logger.debug(f"SFX played: {sound_name}")
        except Exception as e:
            Logger.error(f"Failed to play SFX: {str(e)}")

    @classmethod
    def stop_sfx(cls):

        cls._initialize()
        cls._channels[cls.CHANNEL_SFX].stop()
