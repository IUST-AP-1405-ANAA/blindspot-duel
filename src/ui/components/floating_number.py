from src.config.colors import VFX_FLOATING_TEXT_COLOR
import src.config.settings as cfg


class FloatingNumber:
    """
    Represents a number that floats up and fades out.
    """
    def __init__(self, text: str, x: float, y: float, color=None, speed=None, duration=None):
        if color is None:
            color = VFX_FLOATING_TEXT_COLOR
        if speed is None:
            speed = cfg.VFX_DEFAULT_SPEED
        if duration is None:
            duration = cfg.VFX_DEFAULT_DURATION
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.duration = duration
        self.age = 0.0

    def update(self, dt: float) -> bool:
        """Return False if age exceeded duration to discard effect."""
        self.age += dt
        self.y -= self.speed * dt
        return self.age < self.duration