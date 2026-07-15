"""
Base class for all entities.
"""


class GameObject:
    """
    Fundamental data class for entities on screen.
    """

    def __init__(self, x: float, y: float):
        self._check_coordinates(x, y)
        self._x = x
        self._y = y
        self._is_active = True

    def _check_coordinates(self, x: float, y: float) -> None:
        if not isinstance(x, (int, float)):
            raise TypeError("x must be a number")

        if not isinstance(y, (int, float)):
            raise TypeError("y must be a number")

        if x < 0:
            raise ValueError("x must be non-negative")

        if y < 0:
            raise ValueError("y must be non-negative")

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    @property
    def coordinates(self) -> tuple[float, float]:
        return (self._x, self._y)

    @property
    def is_active(self) -> bool:
        return self._is_active

    def set_position(self, x: float, y: float) -> None:
        self._check_coordinates(x, y)
        self._x = x
        self._y = y

    def activate(self) -> None:
        self._is_active = True

    def deactivate(self) -> None:
        self._is_active = False