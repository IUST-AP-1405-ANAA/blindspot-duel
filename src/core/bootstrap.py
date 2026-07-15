"""
Dependency Injection and application setup.
"""
import pygame
from src.core.game_engine import GameEngine
from src.core.state_manager import StateManager
from src.core.delta_clock import DeltaClock
from src.utils.audio_manager import AudioManager
from src.utils.exception_logger import ExceptionLogger
from src.database.sqlite_repository import SQLiteRepository
from src.ui.pygame_renderer import PygameRenderer

def initialize_app() -> GameEngine:
    """
    Initializes all layers, database, repositories, managers and injects them
    into the GameEngine.
    """
    from src.config.config_manager import ConfigManager
    ConfigManager.load_settings()
    
    ExceptionLogger.log_info("Starting application bootstrapping...")
    
    # Initialize pygame
    pygame.init()
    from src.config.settings import WIDTH, HEIGHT, GAME_TITLE
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE | pygame.DOUBLEBUF)
    pygame.display.set_caption(GAME_TITLE)
    
    # Instantiate lower-level adapters
    db = SQLiteRepository()
    renderer = PygameRenderer(screen)
    audio = AudioManager()
    clock = DeltaClock()
    state_manager = StateManager()
    
    # Inject dependencies and assemble the GameEngine
    engine = GameEngine(state_manager, clock, renderer, db, audio)
    return engine
