class GameObject:
    def __init__(self, x: float, y: float, is_active: bool = False):
        self._check_coordinates(x, y)
        if not isinstance(is_active, bool):
            raise TypeError("is_active must be a boolean")
        self._x = x
        self._y = y
        self._is_active = is_active

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

    @property
    def y(self) -> float:
        return self._y

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