"""
State manager for consecutive hits.
"""

class ComboTracker:
    """
    Tracks consecutive successful hits and manages multipliers.
    """

    def __init__(self):
        self.combo = 0
        self.max_combo = 0

    def record_hit(self) -> int:
        """Increment combo counter."""
        self.combo += 1
        if self.combo > self.max_combo:
            self.max_combo = self.combo
        return self.combo

    def reset_combo(self) -> None:
        """Reset combo counter after a miss."""
        self.combo = 0
