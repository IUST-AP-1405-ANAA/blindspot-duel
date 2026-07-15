import logging
from pathlib import Path
from typing import Optional


class Logger:

    _logger: Optional[logging.Logger] = None
    _initialized: bool = False

    @classmethod
    def _initialize(cls):

        if cls._initialized:
            return

        cls._logger = logging.getLogger("BlindSpot")
        cls._logger.setLevel(logging.DEBUG)

        if cls._logger.handlers:
            return

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        cls._logger.addHandler(console_handler)

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "game.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        cls._logger.addHandler(file_handler)

        cls._initialized = True

    @classmethod
    def info(cls, message: str):
        cls._initialize()
        cls._logger.info(message)

    @classmethod
    def warning(cls, message: str):
        cls._initialize()
        cls._logger.warning(message)

    @classmethod
    def error(cls, message: str):
        cls._initialize()
        cls._logger.error(message)

    @classmethod
    def debug(cls, message: str):
        cls._initialize()
        cls._logger.debug(message)
