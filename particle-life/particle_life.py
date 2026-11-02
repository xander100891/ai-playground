import os
import random
import math
import pygame
import imageio

WIDTH, HEIGHT = 1100, 750
NUM_PARTICLES = 300
NUM_COLORS = 5

RADIUS = 65
MIN_DIST = 14
MAX_SPEED = 3.8
FRICTION = 0.88
TRAIL_FADE = 18

# Recording
RECORDING = False
RECORD_FPS = 60
RECORD_SECONDS = 20
VIDEO_PATH = "videos/particle_life.mp4"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Life")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

trail_surface = pygame.Surface((WIDTH, HEIGHT))
trail_surface.set_alpha(TRAIL_FADE)

COLORS = [
    (255, 70, 100),
    (80, 190, 255),
    (120, 255, 160),
    (255, 220, 80),
    (220, 120, 255),
]

rules = [
    [random.uniform(-1.0, 1.0) for _ in range(NUM_COLORS)]
    for _ in range(NUM_COLORS)
]


class Particle:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.kind = random.randrange(NUM_COLORS)

    def update(self, particles, mouse_pos=None, mouse_mode=None):
        fx = 0
        fy = 0

        for other in particles:
            if other is self:
                continue

            dx = other.x - self.x
            dy = other.y - self.y

            if dx > WIDTH / 2:
                dx -= WIDTH
            elif dx < -WIDTH / 2:
                dx += WIDTH

            if dy > HEIGHT / 2:
                dy -= HEIGHT
            elif dy < -HEIGHT / 2:
                dy += HEIGHT

            dist = math.sqrt(dx * dx + dy * dy)

            if 0 < dist < RADIUS:
                force = rules[self.kind][other.kind]

                if dist < MIN_DIST:
                    force = -2.2

                strength = force * (1 - dist / RADIUS)

                fx += (dx / dist) * strength
                fy += (dy / dist) * strength

        if mouse_pos and mouse_mode:
            mx, my = mouse_pos
            dx = mx - self.x
            dy = my - self.y
            dist = math.sqrt(dx * dx + dy * dy)

            if 0 < dist < 220:
                direction = 1 if mouse_mode == "attract" else -1
                strength = direction * 2.2 * (1 - dist / 220)
                fx += (dx / dist) * strength
                fy += (dy / dist) * strength

        self.vx = (self.vx + fx) * FRICTION
        self.vy = (self.vy + fy) * FRICTION

        speed = math.sqrt(self.vx * self.vx + self.vy * self.vy)

        if speed > MAX_SPEED:
            self.vx = (self.vx / speed) * MAX_SPEED
            self.vy = (self.vy / speed) * MAX_SPEED

        self.x = (self.x + self.vx) % WIDTH
        self.y = (self.y + self.vy) % HEIGHT

    def draw(self):
        color = COLORS[self.kind]
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 3)


def reset_rules():
    global rules
    rules = [
        [random.uniform(-1.0, 1.0) for _ in range(NUM_COLORS)]
        for _ in range(NUM_COLORS)
    ]


def reset_particles():
    return [Particle() for _ in range(NUM_PARTICLES)]


def draw_ui(paused, mouse_mode):
    lines = [
        f"Particles: {len(particles)}",
        f"FPS: {int(clock.get_fps())}",
        f"Mouse: {mouse_mode or 'none'}",
        f"Recording: {'ON' if RECORDING else 'OFF'}",
        "N: new rules | R: reset | SPACE: pause",
        "Left click: attract | Right click: repel",
    ]

    y = 10
    for line in lines:
        text = font.render(line, True, (230, 230, 240))
        screen.blit(text, (10, y))
        y += 22

    if paused:
        text = font.render("PAUSED", True, (255, 180, 120))
        screen.blit(text, (WIDTH // 2 - 35, 12))


def setup_recorder():
    if not RECORDING:
        return None

    os.makedirs(os.path.dirname(VIDEO_PATH), exist_ok=True)
    return imageio.get_writer(VIDEO_PATH, fps=RECORD_FPS)


def record_frame(writer):
    frame = pygame.surfarray.array3d(screen)
    frame = frame.swapaxes(0, 1)
    writer.append_data(frame)


particles = reset_particles()
paused = False
running = True

writer = setup_recorder()
frame_count = 0

screen.fill((5, 6, 12))

while running:
    mouse_mode = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key == pygame.K_r:
                particles = reset_particles()
                screen.fill((5, 6, 12))

            if event.key == pygame.K_n:
                reset_rules()
                screen.fill((5, 6, 12))

    buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if buttons[0]:
        mouse_mode = "attract"
    elif buttons[2]:
        mouse_mode = "repel"

    trail_surface.fill((5, 6, 12))
    screen.blit(trail_surface, (0, 0))

    if not paused:
        for particle in particles:
            particle.update(particles, mouse_pos, mouse_mode)

    for particle in particles:
        particle.draw()

    if mouse_mode == "attract":
        pygame.draw.circle(screen, (80, 190, 255), mouse_pos, 24, 2)
    elif mouse_mode == "repel":
        pygame.draw.circle(screen, (255, 80, 100), mouse_pos, 24, 2)

    draw_ui(paused, mouse_mode)

    pygame.display.flip()

    if writer is not None:
        record_frame(writer)
        frame_count += 1

        if frame_count >= RECORD_FPS * RECORD_SECONDS:
            running = False

    clock.tick(60)

if writer is not None:
    writer.close()
    print(f"Video saved to {VIDEO_PATH}")

pygame.quit()