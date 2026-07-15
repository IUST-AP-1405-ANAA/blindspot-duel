import pygame
import math
from src.contracts.i_state import IState
from src.contracts.i_renderable import IRenderable
import src.config.settings as settings_module
from src.config.config_manager import ConfigManager
from src.config.settings import WIDTH, HEIGHT
from src.config.messages import SETTINGS_TITLE, SETTINGS_SUBTITLE, SETTINGS_FOOTER
from src.config.colors import (
    MENU_TITLE_COLOR, MENU_SUBTITLE_COLOR, MENU_SELECT_BORDER_COLOR,
    MENU_ACTIVE_TEXT_COLOR, MENU_INACTIVE_TEXT_COLOR, MENU_FOOTER_COLOR, BG_COLOR
)

CONFIGURABLE_ITEMS = [
    {"key": "MASTER_VOLUME", "label": "Master Volume", "min": 0.0, "max": 1.0, "step": 0.1, "type": "float"},
    {"key": "DEFAULT_TIME", "label": "Match Duration (s)", "min": 10.0, "max": 300.0, "step": 10.0, "type": "float"},
    {"key": "MAX_TARGETS_ON_SCREEN", "label": "Max Targets", "min": 1, "max": 10, "step": 1, "type": "int"},
    {"key": "DEFAULT_AMMO", "label": "Starting Ammo", "min": 5, "max": 50, "step": 5, "type": "int"},
    {"key": "TARGET_RADIUS", "label": "Target Size", "min": 10.0, "max": 50.0, "step": 5.0, "type": "float"},
    {"key": "CROSSHAIR_SPEED", "label": "Crosshair Speed", "min": 100.0, "max": 600.0, "step": 25.0, "type": "float"},
    {"key": "DEFAULT_BASE_SCORE", "label": "Base Score", "min": 1, "max": 10, "step": 1, "type": "int"},
    {"key": "ITEM_RADIUS", "label": "Item Size", "min": 10.0, "max": 40.0, "step": 5.0, "type": "float"},
    {"key": "AMMO_BOX_BONUS", "label": "Ammo Box Bonus", "min": 1, "max": 20, "step": 1, "type": "int"},
    {"key": "TIME_BOOST_BONUS", "label": "Time Boost (s)", "min": 1.0, "max": 15.0, "step": 1.0, "type": "float"},
    {"key": "FPS", "label": "FPS Limit", "min": 30, "max": 240, "step": 10, "type": "int"},
]


class SettingsScreen(IState):
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.selected = 0
        self.scroll_offset = 0
        self.values = {}

    def enter(self) -> None:
        # Load current values from settings_module
        for item in CONFIGURABLE_ITEMS:
            key = item["key"]
            if hasattr(settings_module, key):
                self.values[key] = getattr(settings_module, key)
            else:
                self.values[key] = item["min"]

    def update(self, dt: float, commands: dict) -> None:
        for event in commands["raw_events"]:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    self.selected = max(0, self.selected - 1)
                    self.state_manager.engine.audio.play_sfx("shoot")
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.selected = min(len(CONFIGURABLE_ITEMS) - 1, self.selected + 1)
                    self.state_manager.engine.audio.play_sfx("shoot")
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.adjust_value(-1)
                    self.state_manager.engine.audio.play_sfx("hit")
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.adjust_value(1)
                    self.state_manager.engine.audio.play_sfx("hit")
                elif event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                    self.save_and_exit()

        # Update scroll offset to keep selected item in view
        target_offset = max(0, self.selected - 5)
        self.scroll_offset += (target_offset - self.scroll_offset) * 10 * dt

    def adjust_value(self, direction: int):
        item = CONFIGURABLE_ITEMS[self.selected]
        key = item["key"]
        val = self.values[key]
        val += direction * item["step"]
        val = max(item["min"], min(item["max"], val))

        if item["type"] == "int":
            val = int(val)
        else:
            val = round(val, 2)

        self.values[key] = val

        # Real-time update for volume
        if key == "MASTER_VOLUME":
            setattr(settings_module, "MASTER_VOLUME", val)
            self.state_manager.engine.audio.set_volume(val)

    def save_and_exit(self):
        # Save to ConfigManager
        ConfigManager.save_settings(self.values)
        # Apply to running module
        for key, val in self.values.items():
            setattr(settings_module, key, val)
        # Also re-apply volume in case it was changed
        if "MASTER_VOLUME" in self.values:
            self.state_manager.engine.audio.set_volume(self.values["MASTER_VOLUME"])

        self.state_manager.change_state("MAIN_MENU")

    def render(self, renderer: IRenderable) -> None:
        renderer.clear_screen(BG_COLOR)

        # Title
        renderer.draw_ui_text(SETTINGS_TITLE, WIDTH // 2, 80, color=MENU_TITLE_COLOR, size=36, align="center")
        renderer.draw_ui_text(SETTINGS_SUBTITLE, WIDTH // 2, 120, color=MENU_SUBTITLE_COLOR, size=14, align="center")

        # List items
        start_y = 180
        spacing = 45

        for i, item in enumerate(CONFIGURABLE_ITEMS):
            y_pos = start_y + (i - self.scroll_offset) * spacing

            # Hide items outside view
            if y_pos < 150 or y_pos > HEIGHT - 100:
                continue

            is_active = (self.selected == i)
            color = MENU_ACTIVE_TEXT_COLOR if is_active else MENU_INACTIVE_TEXT_COLOR

            label_str = item["label"]
            val_str = str(self.values[item["key"]])

            if item["type"] == "float" and item["key"] != "MASTER_VOLUME":
                val_str = f"{self.values[item['key']]:.1f}"
            if item["key"] == "MASTER_VOLUME":
                val_str = f"{int(self.values[item['key']] * 100)}%"

            display_str = f"{label_str}: < {val_str} >" if is_active else f"{label_str}:   {val_str}  "

            if is_active:
                pygame.draw.rect(renderer.screen, MENU_SELECT_BORDER_COLOR, (WIDTH // 2 - 200, y_pos - 20, 400, 40), 1, border_radius=4)

            renderer.draw_ui_text(display_str, WIDTH // 2, y_pos - 8, color=color, size=20, align="center")

        # Footer
        renderer.draw_ui_text(SETTINGS_FOOTER, WIDTH // 2, HEIGHT - 40, color=MENU_FOOTER_COLOR, size=12, align="center")

    def exit(self) -> None:
        pass