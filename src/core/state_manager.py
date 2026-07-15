"""
Manages state transitions.
"""
from src.contracts.i_state import IState
from src.contracts.i_renderable import IRenderable
from src.utils.exception_logger import ExceptionLogger

class StateManager:
    """
    Handles switching between different game states (menu, game, leaderboard).
    """

    def __init__(self):
        self._current_state_name = None
        self._current_state = None
        self.is_running = True
        self.engine = None
        self.states = {}

    def setup(self, engine) -> None:
        """Initialize states after game engine creation."""
        self.engine = engine
        
        # Resolve circular imports by importing states here
        from src.ui.screens.auth_screen import AuthScreen
        from src.ui.screens.start_menu_screen import StartMenuScreen
        from src.ui.screens.leaderboard_screen import LeaderboardScreen
        from src.ui.screens.settings_screen import SettingsScreen
        from src.ui.screens.match_results_screen import MatchResultsScreen
        
        # Create states
        self.states = {
            "AUTH_SCREEN": AuthScreen(self, engine.database),
            "MAIN_MENU": StartMenuScreen(self),
            "SETTINGS": SettingsScreen(self),
            "MATCH_RESULTS": MatchResultsScreen(self),
            "PLAYING": None, # Will be created fresh each play session
            "LEADERBOARD": LeaderboardScreen(self, engine.database)
        }

    def change_state(self, new_state_name: str) -> None:
        """Transition to a new State."""
        if self._current_state:
            ExceptionLogger.log_info(f"Exiting state: {self._current_state_name}")
            self._current_state.exit()
            
        self._current_state_name = new_state_name
        
        if new_state_name == "PLAYING":
            # Instantiate playing state fresh for setup and cleanup
            from src.core.game_engine import GameEngine
            from src.ui.screens.playing_state import PlayingState
            self.states["PLAYING"] = PlayingState(self, self.engine)
            
        self._current_state = self.states[new_state_name]
        ExceptionLogger.log_info(f"Entering state: {self._current_state_name}")
        self._current_state.enter()

    def update(self, dt: float, commands: dict) -> None:
        """Update current state."""
        if self._current_state:
            self._current_state.update(dt, commands)

    def render(self, renderer: IRenderable) -> None:
        """Render current state."""
        if self._current_state:
            self._current_state.render(renderer)
