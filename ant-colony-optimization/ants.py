import imageio
import pygame, random
import numpy as np

W, H = 1100, 720
CELL = 6
GW, GH = W // CELL, H // CELL

ANTS_START = 520
FPS = 120
ANT_SPEED = 0.45

EVAPORATION = 0.985
DIFFUSION = 0.035
SENSOR_DISTANCE = 5
RANDOMNESS = 0.42

FOOD_COUNT = 14

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ant Colony Optimization")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 16)

nest = np.array([GW // 2, GH // 2])

pheromone_food = np.zeros((GH, GW), dtype=np.float32)
walls = np.zeros((GH, GW), dtype=bool)

paused = False
recording = False
show_help = False
video_writer = None
video_name = "ants_recording.mp4"

dirs = np.array([
    [1, 0], [1, 1], [0, 1], [-1, 1],
    [-1, 0], [-1, -1], [0, -1], [1, -1]
], dtype=float)

def add_obstacle(cx, cy, size=18):
    x, y = cx, cy

    for _ in range(size):
        walls[y, x] = True

        if random.random() < 0.75:
            walls[min(GH - 2, y + 1), x] = True

        if random.random() < 0.75:
            walls[y, min(GW - 2, x + 1)] = True

        x += random.choice([-1, 0, 1])
        y += random.choice([-1, 0, 1])

        x = max(2, min(GW - 3, x))
        y = max(2, min(GH - 3, y))

for _ in range(115):
    add_obstacle(
        random.randint(8, GW - 8),
        random.randint(6, GH - 6),
        random.randint(7, 18)
    )

walls[nest[1]-8:nest[1]+8, nest[0]-8:nest[0]+8] = False

def make_food_shape():
    cells = set()
    x, y = 0, 0
    cells.add((x, y))

    for _ in range(random.randint(8, 28)):
        dx, dy = random.choice([
            (1, 0), (-1, 0),
            (0, 1), (0, -1),
            (1, 1), (-1, -1),
            (1, -1), (-1, 1)
        ])

        x += dx
        y += dy

        x = max(-5, min(5, x))
        y = max(-5, min(5, y))

        cells.add((x, y))

        if random.random() < 0.28:
            cells.add((x + random.randint(-1, 1), y + random.randint(-1, 1)))

    cells = list(cells)
    random.shuffle(cells)
    return cells

def spawn_food(pos=None):
    while True:
        if pos is None:
            p = np.array([
                random.randint(8, GW - 8),
                random.randint(8, GH - 8)
            ])
        else:
            p = np.array(pos)

        if not walls[p[1], p[0]] and np.linalg.norm(p - nest) > 30:
            cells = make_food_shape()
            amount = max(30, len(cells) * 16)

            return {
                "pos": p,
                "amount": amount,
                "max_amount": amount,
                "cells": cells
            }

foods = [spawn_food() for _ in range(FOOD_COUNT)]

class Ant:
    def __init__(self):
        angle = random.random() * np.pi * 2
        radius = random.uniform(6, 16)

        self.pos = nest.astype(float) + np.array([
            np.cos(angle),
            np.sin(angle)
        ]) * radius

        self.dir = random.randrange(8)
        self.has_food = False
        self.life = 0
        self.target_food = random.choice(foods)

    def valid(self, p):
        x, y = int(p[0]), int(p[1])
        return 1 <= x < GW - 1 and 1 <= y < GH - 1 and not walls[y, x]

    def choose_food(self):
        available = [f for f in foods if f["amount"] > 0]

        if available:
            self.target_food = random.choice(available)

    def choose_direction(self):
        goal = nest if self.has_food else self.target_food["pos"]

        options = []
        weights = []

        for turn in [-2, -1, 0, 1, 2]:
            nd = (self.dir + turn) % 8
            step = dirs[nd]
            next_pos = self.pos + step * ANT_SPEED

            if not self.valid(next_pos):
                continue

            probe = self.pos + step * SENSOR_DISTANCE

            x = int(np.clip(probe[0], 0, GW - 1))
            y = int(np.clip(probe[1], 0, GH - 1))

            pher = pheromone_food[y, x]
            dist_score = 1.0 / (np.linalg.norm(goal - probe) + 1.0)
            forward = 1.6 if turn == 0 else 1.0

            if self.has_food:
                weight = 1.0 + dist_score * 90
            else:
                weight = 1.0 + pher * 2.0 + dist_score * 10

            weight *= forward

            options.append(nd)
            weights.append(weight)

        if not options or random.random() < RANDOMNESS:
            self.dir = (self.dir + random.choice([-1, 0, 1])) % 8
        else:
            weights = np.array(weights, dtype=float)
            weights /= weights.sum()
            self.dir = np.random.choice(options, p=weights)

    def update(self):
        self.life += 1

        if not self.has_food and random.random() < 0.015:
            self.choose_food()

        self.choose_direction()

        step = dirs[self.dir] * ANT_SPEED
        new_pos = self.pos + step

        if self.valid(new_pos):
            self.pos = new_pos
        else:
            self.dir = random.randrange(8)

        x, y = int(self.pos[0]), int(self.pos[1])

        if self.has_food:
            pheromone_food[y, x] += 3.2

        if not self.has_food:
            for f in foods[:]:
                if f["amount"] > 0 and np.linalg.norm(self.pos - f["pos"]) < 6:
                    self.has_food = True
                    self.target_food = f
                    f["amount"] -= 1
                    self.dir = (self.dir + 4) % 8

                    if f["amount"] <= 0:
                        foods[:] = [food for food in foods if food is not f]
                        foods.append(spawn_food())

                    break

        if self.has_food and np.linalg.norm(self.pos - nest) < 6:
            self.has_food = False
            self.target_food = random.choice(foods)
            self.dir = (self.dir + 4) % 8
            self.life = 0

        if self.life > 3500:
            self.__init__()

    def draw(self):
        px = int(self.pos[0] * CELL)
        py = int(self.pos[1] * CELL)

        if self.has_food:
            color = (255, 225, 90)
            glow = (255, 170, 50)
        else:
            color = (235, 245, 255)
            glow = (110, 180, 255)

        if 1 <= px < W - 1 and 1 <= py < H - 1:
            screen.set_at((px, py), color)
            screen.set_at((px + 1, py), glow)

def diffuse(field):
    blurred = (
        np.roll(field, 1, 0) +
        np.roll(field, -1, 0) +
        np.roll(field, 1, 1) +
        np.roll(field, -1, 1)
    ) * 0.25

    field[:] = field * (1 - DIFFUSION) + blurred * DIFFUSION
    field[walls] = 0

def draw_help():
    lines = [
        "SPACE   pause / play",
        "+ / -   add / remove ants",
        "C       clear trails",
        "V       record video",
        "LMB     add food",
        "RMB     draw walls",
        "H       hide help",
        "ESC     quit"
    ]

    panel = pygame.Surface((275, 205), pygame.SRCALPHA)
    panel.fill((5, 10, 20, 155))
    screen.blit(panel, (18, 18))

    pygame.draw.rect(screen, (80, 160, 255), (18, 18, 275, 205), 1)

    for i, line in enumerate(lines):
        text = font.render(line, True, (220, 235, 255))
        screen.blit(text, (35, 35 + i * 21))

def render_scene():
    screen.fill((18, 24, 38))

    food_map = np.clip(pheromone_food * 20, 0, 255).astype(np.uint8)

    rgb = np.zeros((GH, GW, 3), dtype=np.uint8)
    rgb[..., 0] = 8
    rgb[..., 1] = 18
    rgb[..., 2] = 35

    rgb[..., 0] += food_map // 10
    rgb[..., 1] += food_map
    rgb[..., 2] += food_map

    trail = pygame.surfarray.make_surface(np.swapaxes(rgb, 0, 1))
    trail = pygame.transform.scale(trail, (W, H))
    trail.set_alpha(55)
    screen.blit(trail, (0, 0))

    ys, xs = np.where(walls)

    for x, y in zip(xs, ys):
        rect = (x * CELL, y * CELL, CELL - 1, CELL - 1)
        pygame.draw.rect(screen, (120, 135, 160), rect)
        pygame.draw.rect(screen, (55, 65, 85), rect, 1)

    for f in foods:
        center_x = int(f["pos"][0] * CELL)
        center_y = int(f["pos"][1] * CELL)

        remaining = f["amount"] / f["max_amount"]
        visible_cells = max(1, int(len(f["cells"]) * remaining))

        for dx, dy in f["cells"][:visible_cells]:
            x = center_x + dx * CELL
            y = center_y + dy * CELL

            pygame.draw.rect(screen, (245, 190, 60), (x, y, CELL - 1, CELL - 1))
            pygame.draw.rect(screen, (130, 85, 20), (x, y, CELL - 1, CELL - 1), 1)

    nest_pos = (int(nest[0] * CELL), int(nest[1] * CELL))

    for dy in range(-5, 6):
        for dx in range(-5, 6):
            d = abs(dx) + abs(dy)

            if d < 7:
                x = nest_pos[0] + dx * CELL
                y = nest_pos[1] + dy * CELL

                color = (92, 64, 38) if d > 3 else (130, 86, 45)

                pygame.draw.rect(screen, color, (x, y, CELL - 1, CELL - 1))
                pygame.draw.rect(screen, (45, 28, 15), (x, y, CELL - 1, CELL - 1), 1)

    pygame.draw.circle(screen, (35, 22, 12), nest_pos, 11)

    for ant in ants:
        ant.draw()

    if show_help:
        draw_help()

ants = [Ant() for _ in range(ANTS_START)]

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                for _ in range(50):
                    ants.append(Ant())

            if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                remove_count = min(50, len(ants))
                del ants[-remove_count:]

            if event.key == pygame.K_c:
                pheromone_food[:] = 0

            if event.key == pygame.K_h:
                show_help = not show_help

            if event.key == pygame.K_v:
                recording = not recording

                if recording:
                    video_writer = imageio.get_writer(video_name, fps=60)
                    print("Recording started:", video_name)
                else:
                    if video_writer:
                        video_writer.close()
                        video_writer = None
                    print("Recording saved:", video_name)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            gx, gy = mx // CELL, my // CELL

            if 0 <= gx < GW and 0 <= gy < GH and not walls[gy, gx]:
                foods.append(spawn_food((gx, gy)))

    if pygame.mouse.get_pressed()[2]:
        mx, my = pygame.mouse.get_pos()
        gx, gy = mx // CELL, my // CELL

        if 0 <= gx < GW and 0 <= gy < GH:
            walls[max(0, gy-2):min(GH, gy+3), max(0, gx-2):min(GW, gx+3)] = True

    if not paused:
        pheromone_food *= EVAPORATION
        diffuse(pheromone_food)

        for ant in ants:
            ant.update()

    render_scene()

    if recording and video_writer:
        frame = pygame.surfarray.array3d(screen)
        frame = np.transpose(frame, (1, 0, 2))
        video_writer.append_data(frame)

    pygame.display.flip()

if video_writer:
    video_writer.close()

pygame.quit()