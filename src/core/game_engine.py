"""
Main game orchestrator.
"""
import pygame
from src.contracts.i_database import IDatabase
from src.contracts.i_renderable import IRenderable
from src.contracts.i_audio_player import IAudioPlayer
from src.core.state_manager import StateManager
from src.core.delta_clock import DeltaClock
from src.core.event_handler import EventHandler
from src.core.input_mapper import InputMapper
from src.utils.exception_logger import ExceptionLogger
from src.ui.vfx.animation_manager import AnimationManager
from src.ui.vfx.floating_text import FloatingTextVFX
from src.config.colors import BG_COLOR
from src.config.settings import DEFAULT_BG_MUSIC, INITIAL_STATE

class GameEngine:
    """
    Main orchestrator that runs the game loop.
    """

    def __init__(self, state_manager: StateManager, delta_clock: DeltaClock, 
                 renderer: IRenderable, database: IDatabase, audio: IAudioPlayer):
        self.state_manager = state_manager
        self.clock = delta_clock
        self.renderer = renderer
        self.database = database
        self.audio = audio
        
        self.event_handler = EventHandler()
        self.input_mapper = InputMapper()
        
        # VFX system
        self.vfx_system = FloatingTextVFX()
        self.animation_manager = AnimationManager()
        self.animation_manager.set_vfx(self.vfx_system)
        
        # Pass instances to state manager
        self.state_manager.setup(self)
        self.is_running = True

    def run(self) -> None:
        """The main while loop (events -> update -> render)."""
        ExceptionLogger.log_info("Game Engine started.")
        self.audio.play_background_music(DEFAULT_BG_MUSIC)
        
        # Transition to initial state
        self.state_manager.change_state(INITIAL_STATE)
        
        while self.is_running and self.state_manager.is_running:
            # Phase 0: Delta Time
            dt = self.clock.tick()
            
            # Phase 1: Event Polling
            events = self.event_handler.poll_events()
            if not self.event_handler.is_window_open:
                self.is_running = False
                break
                
            # Input Mapping
            commands = self.input_mapper.map_inputs(events)
            
            # Phase 2: Update logic based on state
            self.state_manager.update(dt, commands)
            
            # Update animations
            self.animation_manager.update(dt)
            
            # Phase 3: Render
            self.renderer.clear_screen(BG_COLOR)
            self.state_manager.render(self.renderer)
            
            # Draw float text VFX over state renders
            self.vfx_system.render(self.renderer)
            
            self.renderer.flip_buffer()
            
        self.audio.stop_all_sounds()
        pygame.quit()
        ExceptionLogger.log_info("Game Engine shutdown successfully.")
