import pygame
import random
import math

from src.config.settings import (
    VFX_SHOCKWAVE_MAX_RADIUS, VFX_SHOCKWAVE_SPEED, VFX_SHOCKWAVE_START_RADIUS,
    VFX_SHOCKWAVE_WIDTH, VFX_SPAWN_SPEED, VFX_SPAWN_DURATION, VFX_FONT_SIZE,
    VFX_SHADOW_OFFSET, VFX_EXPLOSION_COUNT, VFX_EXPLOSION_SPEED_RANGE,
    VFX_EXPLOSION_SIZE_RANGE, VFX_EXPLOSION_LIFETIME_RANGE
)
from src.config.colors import VFX_FLOATING_TEXT_COLOR, SHADOW_COLOR


class Particle:
    def __init__(self, x, y, dx, dy, color, size=4.0, lifetime=0.4):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.age = 0.0

    def update(self, dt) -> bool:
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.age += dt
        return self.age < self.lifetime


class Shockwave:
    def __init__(self, x, y, color, max_radius=VFX_SHOCKWAVE_MAX_RADIUS, speed=VFX_SHOCKWAVE_SPEED):
        self.x = x
        self.y = y
        self.color = color
        self.max_radius = max_radius
        self.speed = speed
        self.radius = VFX_SHOCKWAVE_START_RADIUS

    def update(self, dt) -> bool:
        self.radius += self.speed * dt
        return self.radius < self.max_radius


class FloatingTextVFX:
    """
    Manages floating texts, particles, and shockwaves.
    """

    def __init__(self):
        from src.ui.components.floating_number import FloatingNumber
        self.effects = []
        self.particles = []
        self.shockwaves = []

    def spawn(self, text: str, x: float, y: float, color=None) -> None:
        from src.ui.components.floating_number import FloatingNumber
        if color is None:
            color = VFX_FLOATING_TEXT_COLOR
        self.effects.append(FloatingNumber(text, x, y, color, speed=VFX_SPAWN_SPEED, duration=VFX_SPAWN_DURATION))

    def spawn_explosion(self, x: float, y: float, color: tuple, count=None) -> None:
        if count is None:
            count = VFX_EXPLOSION_COUNT
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(VFX_EXPLOSION_SPEED_RANGE[0], VFX_EXPLOSION_SPEED_RANGE[1])
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            size = random.uniform(VFX_EXPLOSION_SIZE_RANGE[0], VFX_EXPLOSION_SIZE_RANGE[1])
            lifetime = random.uniform(VFX_EXPLOSION_LIFETIME_RANGE[0], VFX_EXPLOSION_LIFETIME_RANGE[1])
            self.particles.append(Particle(x, y, dx, dy, color, size, lifetime))

    def spawn_shockwave(self, x: float, y: float, color: tuple) -> None:
        self.shockwaves.append(Shockwave(x, y, color))

    def update(self, dt: float) -> None:
        self.effects = [e for e in self.effects if e.update(dt)]
        self.particles = [p for p in self.particles if p.update(dt)]
        self.shockwaves = [s for s in self.shockwaves if s.update(dt)]

    def render(self, renderer) -> None:
        # 1. Render Shockwaves
        for s in self.shockwaves:
            alpha = int(255 * (1.0 - s.radius / s.max_radius))
            # We draw concentric rings with faded color
            surf = pygame.Surface((int(s.radius * 2 + 4), int(s.radius * 2 + 4)), pygame.SRCALPHA)
            pygame.draw.circle(surf, (s.color[0], s.color[1], s.color[2], alpha), (int(s.radius + 2), int(s.radius + 2)), int(s.radius), VFX_SHOCKWAVE_WIDTH)
            renderer.screen.blit(surf, (int(s.x - s.radius - 2), int(s.y - s.radius - 2)))

        # 2. Render Particles
        for p in self.particles:
            alpha = int(255 * (1.0 - p.age / p.lifetime))
            p_surf = pygame.Surface((int(p.size * 2), int(p.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (p.color[0], p.color[1], p.color[2], alpha), (int(p.size), int(p.size)), int(p.size))
            renderer.screen.blit(p_surf, (int(p.x - p.size), int(p.y - p.size)))

        # 3. Render Floating texts
        for e in self.effects:
            alpha = int(255 * (1.0 - e.age / e.duration))
            font = renderer.text_renderer._get_font(VFX_FONT_SIZE)
            text_surf = font.render(e.text, True, e.color)

            # create transparent temp surf
            temp_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
            # Render black shadow inside temp surf
            shadow_surf = font.render(e.text, True, SHADOW_COLOR)
            temp_surf.blit(shadow_surf, (VFX_SHADOW_OFFSET[0], VFX_SHADOW_OFFSET[1]))
            temp_surf.blit(text_surf, (0, 0))
            temp_surf.set_alpha(alpha)

            renderer.screen.blit(temp_surf, (int(e.x), int(e.y)))