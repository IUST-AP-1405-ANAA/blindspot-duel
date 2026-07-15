import json
import os
from src.utils.exception_logger import ExceptionLogger

class ConfigManager:
    """
    Handles reading and writing user_settings.json and applying them dynamically
    to src.config.settings.
    """
    CONFIG_FILE = "user_settings.json"
    
    @classmethod
    def apply_settings(cls, settings_data: dict):
        import src.config.settings as settings_module
        count = 0
        for key, value in settings_data.items():
            if hasattr(settings_module, key):
                setattr(settings_module, key, value)
                count += 1
                
        return count
        
    @classmethod
    def load_settings(cls):
        """Load settings from JSON and inject them into settings.py attributes."""
        if not os.path.exists(cls.CONFIG_FILE):
            return
            
        try:
            with open(cls.CONFIG_FILE, 'r') as f:
                settings_data = json.load(f)
                
            count = cls.apply_settings(settings_data)
            ExceptionLogger.log_info(f"Loaded {count} custom settings and hot-patched modules from {cls.CONFIG_FILE}")
        except Exception as e:
            ExceptionLogger.log_error(f"Failed to load user settings: {e}")
            
    @classmethod
    def save_settings(cls, new_settings: dict):
        """Save dictionary of settings to JSON and hot-patch."""
        try:
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump(new_settings, f, indent=4)
            cls.apply_settings(new_settings)
            ExceptionLogger.log_info(f"Saved custom settings to {cls.CONFIG_FILE}")
        except Exception as e:
            ExceptionLogger.log_error(f"Failed to save user settings: {e}")
