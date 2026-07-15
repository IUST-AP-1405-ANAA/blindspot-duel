import pygame
import random
import math
from blindspot_duel.contracts.i_state import IState
from blindspot_duel.contracts.i_renderable import IRenderable

from blindspot_duel.config.settings import (
    WIDTH, HEIGHT, MENU_PARTICLE_COUNT, MENU_PARTICLE_VX_RANGE,
    MENU_PARTICLE_VY_RANGE, MENU_PARTICLE_RADIUS_RANGE, MENU_PULSE_SPEED,
    MENU_PULSE_AMPLITUDE, MENU_OPTIONS_Y_START, MENU_OPTIONS_Y_SPACING,
    MENU_BTN_WIDTH, MENU_BTN_HEIGHT, MENU_BTN_BORDER_RADIUS
)
from blindspot_duel.config.colors import (
    MENU_TITLE_COLOR, MENU_SUBTITLE_COLOR, MENU_SELECT_BORDER_COLOR,
    MENU_ACTIVE_TEXT_COLOR, MENU_INACTIVE_TEXT_COLOR, MENU_PLAYER_INFO_COLOR,
    MENU_FOOTER_COLOR, MENU_PARTICLE_COLORS
)
from blindspot_duel.config.messages import (
    MENU_TITLE, MENU_SUBTITLE, MENU_OPTIONS, MENU_FOOTER_NAV
)


class MenuParticle:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(MENU_PARTICLE_VX_RANGE[0], MENU_PARTICLE_VX_RANGE[1])
        self.vy = random.uniform(MENU_PARTICLE_VY_RANGE[0], MENU_PARTICLE_VY_RANGE[1])
        self.radius = random.uniform(MENU_PARTICLE_RADIUS_RANGE[0], MENU_PARTICLE_RADIUS_RANGE[1])
        self.color = random.choice(MENU_PARTICLE_COLORS)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.y < 0:
            self.y = HEIGHT
            self.x = random.uniform(0, WIDTH)


class StartMenuScreen(IState):
    """
    Beautiful Cyber Menu state.
    """

    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.options = MENU_OPTIONS
        self.selected = 0
        self.particles = [MenuParticle() for _ in range(MENU_PARTICLE_COUNT)]

    def enter(self) -> None:
        pass

    def update(self, dt: float, commands: dict) -> None:
        # Update particles
        for p in self.particles:
            p.update(dt)

        for event in commands["raw_events"]:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    self.selected = (self.selected - 1) % len(self.options)
                    self.state_manager.engine.audio.play_sfx("shoot")  # selection sound
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.selected = (self.selected + 1) % len(self.options)
                    self.state_manager.engine.audio.play_sfx("shoot")
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    self.state_manager.engine.audio.play_sfx("hit")  # activate sound
                    self.trigger_action()
                # Direct option selects
                elif event.key == pygame.K_1:
                    self.state_manager.change_state("PLAYING")
                elif event.key == pygame.K_2:
                    self.state_manager.change_state("LEADERBOARD")
                elif event.key == pygame.K_3:
                    self.state_manager.change_state("SETTINGS")
                elif event.key == pygame.K_4:
                    self.state_manager.is_running = False

    def trigger_action(self):
        if self.selected == 0:
            self.state_manager.change_state("PLAYING")
        elif self.selected == 1:
            self.state_manager.change_state("LEADERBOARD")
        elif self.selected == 2:
            self.state_manager.change_state("SETTINGS")
        elif self.selected == 3:
            self.state_manager.is_running = False

    def render(self, renderer: IRenderable) -> None:
        # Draw background floating particles
        for p in self.particles:
            p_surf = pygame.Surface((int(p.radius * 2), int(p.radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, p.color, (int(p.radius), int(p.radius)), int(p.radius))
            renderer.screen.blit(p_surf, (int(p.x - p.radius), int(p.y - p.radius)))

        # Neon Pulsing Title
        ticks = pygame.time.get_ticks()
        pulse = int(math.sin(ticks * MENU_PULSE_SPEED) * MENU_PULSE_AMPLITUDE)
        title_color = MENU_TITLE_COLOR

        renderer.draw_ui_text(MENU_TITLE, 400, 140, color=title_color, size=48 + int(pulse / 4), align="center")

        # Subtitle
        renderer.draw_ui_text(MENU_SUBTITLE, 400, 190, color=MENU_SUBTITLE_COLOR, size=14, align="center")

        # Display menu options
        for i, opt in enumerate(self.options):
            y_pos = MENU_OPTIONS_Y_START + i * MENU_OPTIONS_Y_SPACING
            is_active = (self.selected == i)
            opt_color = MENU_ACTIVE_TEXT_COLOR if is_active else MENU_INACTIVE_TEXT_COLOR

            # Draw buttons border outline when selected
            if is_active:
                btn_w = MENU_BTN_WIDTH
                btn_h = MENU_BTN_HEIGHT
                pygame.draw.rect(renderer.screen, MENU_SELECT_BORDER_COLOR, (400 - btn_w // 2, y_pos - btn_h // 2, btn_w, btn_h), 1, border_radius=MENU_BTN_BORDER_RADIUS)
                renderer.draw_ui_text("> " + opt + " <", 400, y_pos - 8, color=opt_color, size=22, align="center")
            else:
                renderer.draw_ui_text(opt, 400, y_pos - 8, color=MENU_INACTIVE_TEXT_COLOR, size=20, align="center")

        # Player names displaying
        p_info = f"P1: {self.state_manager.p1_username}   |   P2: {self.state_manager.p2_username}"
        renderer.draw_ui_text(p_info, 400, 520, color=MENU_PLAYER_INFO_COLOR, size=14, align="center")

        # Footer hints
        renderer.draw_ui_text(MENU_FOOTER_NAV, 400, 560, color=MENU_FOOTER_COLOR, size=12, align="center")

    def exit(self) -> None:
        pass