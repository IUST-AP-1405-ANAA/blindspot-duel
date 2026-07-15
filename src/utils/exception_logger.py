"""
Custom logger.
"""
import logging
import sys

from src.config.settings import LOG_LEVEL, LOG_FORMAT, LOG_FILE_PATH

# Configure python standard logging
log_level_val = getattr(logging, LOG_LEVEL, logging.INFO)
logging.basicConfig(
    level=log_level_val,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

class ExceptionLogger:
    """
    Logs errors and events to terminal and game_errors.log.
    """

    @staticmethod
    def log_info(msg: str) -> None:
        logging.info(msg)

    @staticmethod
    def log_warning(msg: str) -> None:
        logging.warning(msg)

    @staticmethod
    def log_error(msg: str) -> None:
        logging.error(msg)
