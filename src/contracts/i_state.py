"""
Interface for application states.
"""
from abc import ABC, abstractmethod
from src.contracts.i_renderable import IRenderable

class IState(ABC):
    """Abstract base class representing a state."""

    @abstractmethod
    def enter(self) -> None:
        """Logic to run when entering the state."""
        pass

    @abstractmethod
    def update(self, dt: float, commands: dict) -> None:
        """Update state based on commands and elapsed time."""
        pass

    @abstractmethod
    def render(self, renderer: IRenderable) -> None:
        """Draw state visuals using the renderer."""
        pass

    @abstractmethod
    def exit(self) -> None:
        """Cleanup when exiting the state."""
        pass
