"""
Interface for renderable game objects.
"""
from abc import ABC, abstractmethod

class IRenderable(ABC):
    """Abstract base class for rendering operations."""

    @abstractmethod
    def clear_screen(self, color: tuple) -> None:
        """Fill the screen with a single background color."""
        pass

    @abstractmethod
    def draw_entity(self, x: float, y: float, radius: float, color: tuple, is_visible: bool = True) -> None:
        """Draw circles or shapes representing targets or crosshairs."""
        pass

    @abstractmethod
    def draw_ui_text(self, text: str, x: float, y: float, color: tuple = (255, 255, 255), size: int = 24, align: str = "left") -> None:
        """Render text on screen with custom alignments."""
        pass

    @abstractmethod
    def flip_buffer(self) -> None:
        """Present the rendered screen buffer to the display."""
        pass
