"""
Player data encapsulation.
"""

class Player:
    """
    Encapsulates abstract player information (ammo, time, score).
    """

    def __init__(self, username: str, initial_ammo: int, initial_time: float):
        self._username = username
        self._ammo = initial_ammo
        self._time_remaining = initial_time
        self._score = 0
        self._combo = 0
        self._max_combo = 0
        self._is_crosshair_revealed = False
        self.glitch_timer = 0.0

    @property
    def username(self) -> str:
        return self._username

    @property
    def ammo(self) -> int:
        return self._ammo

    @property
    def time_remaining(self) -> float:
        return self._time_remaining

    @property
    def score(self) -> int:
        return self._score

    @property
    def combo(self) -> int:
        return self._combo

    @property
    def max_combo(self) -> int:
        return self._max_combo

    @property
    def is_crosshair_revealed(self) -> bool:
        return self._is_crosshair_revealed

    @property
    def is_locked_out(self) -> bool:
        return self._ammo <= 0 or self._time_remaining <= 0.0

    def fire_shot(self) -> bool:
        """Decrease ammo and reveal crosshair on success."""
        if self.is_locked_out:
            return False
        self._ammo -= 1
        if not self._is_crosshair_revealed:
            self._is_crosshair_revealed = True
        return True

    def add_ammo(self, amount: int) -> None:
        self._ammo += amount

    def add_time(self, amount: float) -> None:
        self._time_remaining += amount

    def add_score(self, amount: int) -> None:
        self._score += amount

    def increment_combo(self) -> None:
        self._combo += 1
        if self._combo > self._max_combo:
            self._max_combo = self._combo

    def reset_combo(self) -> None:
        self._combo = 0

    def set_glitch_timer(self, seconds: float) -> None:
        self.glitch_timer = seconds

    def update_time(self, dt: float) -> None:
        """Decrease time limits when playing."""
        if not self.is_locked_out:
            self._time_remaining = max(0.0, self._time_remaining - dt)
        if self.glitch_timer > 0:
            self.glitch_timer = max(0.0, self.glitch_timer - dt)
