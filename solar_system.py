"""Solar system simulator: real n-body gravity with pygame.

Controls
  Click + drag   launch a new planet (drag direction and length set its velocity)
  SPACE          pause / resume
  UP / DOWN      speed up / slow down time
  T              toggle trails
  C              clear trails
  R              reset the system
  ESC            quit
"""
import math
import random
from collections import deque

import pygame
from pygame import Vector2

WIDTH, HEIGHT = 1000, 700
CENTER = Vector2(WIDTH / 2, HEIGHT / 2)

G = 1.0               # gravitational constant (sim units)
SUN_MASS = 20000.0
SOFTENING = 5.0       # avoids huge forces when two bodies get very close
BASE_DT = 0.02        # simulation time per substep
SUBSTEPS = 10         # physics steps per drawn frame
TRAIL_LENGTH = 300
LAUNCH_SCALE = 0.1    # drag length -> launch speed


class Body:
    def __init__(self, pos, vel, mass, radius, color, is_sun=False):
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.mass = mass
        self.radius = radius
        self.color = color
        self.is_sun = is_sun
        self.trail = deque(maxlen=TRAIL_LENGTH)

    def draw(self, screen, show_trail):
        if show_trail and len(self.trail) > 2:
            pygame.draw.lines(screen, self.color, False, list(self.trail), 1)
        if self.is_sun:
            # simple glow
            for r, alpha in ((self.radius * 2.2, 30), (self.radius * 1.6, 60)):
                glow = pygame.Surface((int(r * 2), int(r * 2)), pygame.SRCALPHA)
                pygame.draw.circle(glow, (*self.color, alpha), (int(r), int(r)), int(r))
                screen.blit(glow, (self.pos.x - r, self.pos.y - r))
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), int(self.radius))


def accelerations(bodies):
    """Newtonian gravity between every pair of bodies."""
    acc = [Vector2() for _ in bodies]
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            a, b = bodies[i], bodies[j]
            d = b.pos - a.pos
            dist_sq = d.length_squared() + SOFTENING ** 2
            inv_dist = 1.0 / math.sqrt(dist_sq)
            force_dir = d * inv_dist
            f = G / dist_sq
            acc[i] += force_dir * (f * b.mass)
            acc[j] -= force_dir * (f * a.mass)
    return acc


def step(bodies, dt):
    """Velocity Verlet integration: stable for orbits."""
    acc = accelerations(bodies)
    for body, a in zip(bodies, acc):
        body.vel += a * (dt / 2)
        body.pos += body.vel * dt
    acc = accelerations(bodies)
    for body, a in zip(bodies, acc):
        body.vel += a * (dt / 2)


def circular_orbit(radius, angle, mass, body_radius, color):
    pos = CENTER + Vector2(math.cos(angle), math.sin(angle)) * radius
    speed = math.sqrt(G * SUN_MASS / radius)
    vel = Vector2(-math.sin(angle), math.cos(angle)) * speed
    return Body(pos, vel, mass, body_radius, color)


def build_system():
    sun = Body(CENTER, (0, 0), SUN_MASS, 22, (255, 200, 60), is_sun=True)
    planets = [
        circular_orbit(80, random.uniform(0, math.tau), 2, 4, (180, 180, 180)),
        circular_orbit(130, random.uniform(0, math.tau), 4, 6, (230, 170, 90)),
        circular_orbit(190, random.uniform(0, math.tau), 5, 7, (70, 140, 255)),
        circular_orbit(260, random.uniform(0, math.tau), 3, 5, (220, 90, 70)),
    ]
    return [sun] + planets


def main(max_frames=None):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Solar System Simulator")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    stars = [(random.randrange(WIDTH), random.randrange(HEIGHT), random.randint(80, 200))
             for _ in range(150)]

    bodies = build_system()
    paused = False
    show_trails = True
    time_scale = 1.0
    drag_start = None
    frames = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_UP:
                    time_scale = min(time_scale * 1.5, 16)
                elif event.key == pygame.K_DOWN:
                    time_scale = max(time_scale / 1.5, 0.1)
                elif event.key == pygame.K_t:
                    show_trails = not show_trails
                elif event.key == pygame.K_c:
                    for b in bodies:
                        b.trail.clear()
                elif event.key == pygame.K_r:
                    bodies = build_system()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                drag_start = Vector2(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drag_start:
                vel = (Vector2(event.pos) - drag_start) * LAUNCH_SCALE
                color = tuple(random.randint(100, 255) for _ in range(3))
                bodies.append(Body(drag_start, vel, random.uniform(2, 6), random.randint(4, 7), color))
                drag_start = None

        if not paused:
            dt = BASE_DT * time_scale
            for _ in range(SUBSTEPS):
                step(bodies, dt)

            sun = bodies[0]
            survivors = [sun]
            for b in bodies[1:]:
                swallowed = b.pos.distance_to(sun.pos) < sun.radius
                escaped = b.pos.distance_to(CENTER) > 3000
                if not (swallowed or escaped):
                    survivors.append(b)
            bodies = survivors

            for b in bodies:
                b.trail.append((int(b.pos.x), int(b.pos.y)))

        # draw
        screen.fill((5, 5, 15))
        for x, y, c in stars:
            screen.set_at((x, y), (c, c, c))
        for b in bodies:
            b.draw(screen, show_trails)

        if drag_start:
            mouse = Vector2(pygame.mouse.get_pos())
            pygame.draw.line(screen, (255, 255, 255), drag_start, mouse, 2)
            pygame.draw.circle(screen, (255, 255, 255), (int(drag_start.x), int(drag_start.y)), 4)

        hud = (f"planets: {len(bodies) - 1}   speed: x{time_scale:.1f}"
               f"{'   [PAUSED]' if paused else ''}")
        screen.blit(font.render(hud, True, (200, 200, 200)), (10, 10))
        screen.blit(font.render("drag: launch  space: pause  up/down: speed  t: trails  c: clear  r: reset",
                                True, (120, 120, 120)), (10, HEIGHT - 24))

        pygame.display.flip()
        clock.tick(60)

        frames += 1
        if max_frames and frames >= max_frames:
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
