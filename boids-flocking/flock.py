import math
import random
import pygame
from collections import defaultdict

WIDTH, HEIGHT = 1000, 700
NUM_BIRDS = 180

MAX_SPEED = 4
MAX_FORCE = 0.08
PERCEPTION = 65
SEPARATION_DIST = 28
CELL_SIZE = PERCEPTION

BG_COLOR = (15, 18, 28)
BIRD_COLOR = (235, 240, 255)
TRAIL_COLOR = (40, 45, 65)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids Flocking Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)


class Bird:
    def __init__(self):
        self.pos = pygame.Vector2(random.randrange(WIDTH), random.randrange(HEIGHT))
        self.vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))

        if self.vel.length() == 0:
            self.vel = pygame.Vector2(1, 0)

        self.acc = pygame.Vector2()
        self.trail = []

    def update(self):
        self.vel += self.acc

        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.pos += self.vel
        self.acc *= 0

        self.trail.append(self.pos.copy())
        if len(self.trail) > 18:
            self.trail.pop(0)

    def edges(self):
        if self.pos.x > WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = WIDTH

        if self.pos.y > HEIGHT:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = HEIGHT

    def flock(self, nearby, mouse_pos=None, mouse_mode=None):
        alignment = pygame.Vector2()
        cohesion = pygame.Vector2()
        separation = pygame.Vector2()
        total = 0

        for other in nearby:
            if other is self:
                continue

            distance = self.pos.distance_to(other.pos)

            if distance < PERCEPTION:
                alignment += other.vel
                cohesion += other.pos
                total += 1

                if distance < SEPARATION_DIST and distance > 0:
                    diff = self.pos - other.pos
                    diff /= distance
                    separation += diff

        if total > 0:
            alignment /= total
            alignment = self._steer(alignment)

            cohesion /= total
            cohesion = self._steer(cohesion - self.pos)

            separation /= total
            separation = self._steer(separation)

            self.acc += alignment * 1.0
            self.acc += cohesion * 0.75
            self.acc += separation * 1.8

        if mouse_pos is not None and mouse_mode is not None:
            mouse_vec = pygame.Vector2(mouse_pos)
            distance = self.pos.distance_to(mouse_vec)

            if distance < 180 and distance > 0:
                direction = mouse_vec - self.pos

                if mouse_mode == "repel":
                    direction *= -1

                mouse_force = self._steer(direction)
                strength = 1 - (distance / 180)
                self.acc += mouse_force * strength * 2.5

    def _steer(self, vector):
        if vector.length() == 0:
            return pygame.Vector2()

        desired = vector.normalize() * MAX_SPEED
        steer = desired - self.vel

        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)

        return steer

    def draw(self):
        if len(self.trail) > 1:
            for i, p in enumerate(self.trail):
                alpha = i / len(self.trail)
                color = (
                    int(TRAIL_COLOR[0] * alpha),
                    int(TRAIL_COLOR[1] * alpha),
                    int(TRAIL_COLOR[2] * alpha),
                )
                pygame.draw.circle(screen, color, p, 2)

        angle = math.atan2(self.vel.y, self.vel.x)

        points = [
            pygame.Vector2(13, 0),
            pygame.Vector2(-9, 6),
            pygame.Vector2(-6, 0),
            pygame.Vector2(-9, -6),
        ]

        rotated = []
        for p in points:
            x = p.x * math.cos(angle) - p.y * math.sin(angle)
            y = p.x * math.sin(angle) + p.y * math.cos(angle)
            rotated.append((self.pos.x + x, self.pos.y + y))

        speed_ratio = min(self.vel.length() / MAX_SPEED, 1)
        color = (
            int(120 + 115 * speed_ratio),
            int(180 + 60 * speed_ratio),
            255,
        )

        pygame.draw.polygon(screen, color, rotated)


def build_grid(birds):
    grid = defaultdict(list)

    for bird in birds:
        cell = (
            int(bird.pos.x // CELL_SIZE),
            int(bird.pos.y // CELL_SIZE),
        )
        grid[cell].append(bird)

    return grid


def get_nearby(bird, grid):
    cell_x = int(bird.pos.x // CELL_SIZE)
    cell_y = int(bird.pos.y // CELL_SIZE)

    nearby = []

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            nearby.extend(grid[(cell_x + dx, cell_y + dy)])

    return nearby


def draw_obstacles(obstacles):
    for center, radius in obstacles:
        pygame.draw.circle(screen, (80, 55, 75), center, radius)
        pygame.draw.circle(screen, (150, 90, 120), center, radius, 2)


def draw_ui(birds, paused, mouse_mode):
    text = [
        f"Birds: {len(birds)}",
        f"FPS: {int(clock.get_fps())}",
        f"Mouse: {mouse_mode or 'none'}",
        "Left click: attract | Right click: repel",
        "SPACE: pause | R: reset | UP/DOWN: birds",
    ]

    y = 10
    for line in text:
        surface = font.render(line, True, (220, 220, 230))
        screen.blit(surface, (10, y))
        y += 22

    if paused:
        pause_text = font.render("PAUSED", True, (255, 180, 120))
        screen.blit(pause_text, (WIDTH // 2 - 40, 15))


def reset_birds(count):
    return [Bird() for _ in range(count)]


birds = reset_birds(NUM_BIRDS)

paused = False
running = True

while running:
    mouse_mode = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key == pygame.K_r:
                birds = reset_birds(len(birds))

            if event.key == pygame.K_UP:
                birds.extend(reset_birds(20))

            if event.key == pygame.K_DOWN:
                birds = birds[:-20] if len(birds) > 20 else birds

    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if mouse_buttons[0]:
        mouse_mode = "attract"
    elif mouse_buttons[2]:
        mouse_mode = "repel"

    screen.fill(BG_COLOR)

    if not paused:
        grid = build_grid(birds)

        for bird in birds:
            nearby = get_nearby(bird, grid)
            bird.edges()
            bird.flock(nearby, mouse_pos, mouse_mode)
            bird.update()

    for bird in birds:
        bird.draw()

    if mouse_mode == "attract":
        pygame.draw.circle(screen, (80, 180, 255), mouse_pos, 18, 2)
    elif mouse_mode == "repel":
        pygame.draw.circle(screen, (255, 90, 90), mouse_pos, 18, 2)

    draw_ui(birds, paused, mouse_mode)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()