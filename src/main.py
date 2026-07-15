"""
Main entry point for BlindSpot Duel.
"""
import os
import sys

# Ensure the project root is in sys.path to resolve 'src' imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.bootstrap import initialize_app
from src.utils.exception_logger import ExceptionLogger

def main():
    """
    Initializes the bootstrap process and starts the game engine.
    """
    try:
        engine = initialize_app()
        engine.run()
    except Exception as e:
        ExceptionLogger.log_error(f"Global error occurred: {str(e)}")
        import traceback
        ExceptionLogger.log_error(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()
