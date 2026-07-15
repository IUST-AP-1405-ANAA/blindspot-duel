class AnimationManager:
    """
    Processes and updates visual animations over time.
    """

    def __init__(self):
        self.vfx = None

    def set_vfx(self, vfx) -> None:
        self.vfx = vfx

    def update(self, dt: float) -> None:
        """Advance all animations by delta time."""
        if self.vfx:
            self.vfx.update(dt)