# 🐦 Boids Flocking Simulation (Pygame)

A real-time 2D bird flocking simulation using the classic Boids algorithm.

## 🚀 Features

- Separation, alignment, and cohesion behaviors
- Smooth flocking movement
- Mouse attraction and repulsion
- Pause and reset controls
- Adjustable number of birds
- Efficient spatial grid for better performance
- Optional MP4 recording

## 📦 Installation

```bash
pipenv sync
```

## ▶️ Run

```bash
pipenv run python flock.py
```

## 🎮 Controls

```text
Left click  → attract birds
Right click → repel birds
SPACE       → pause
R           → reset flock
UP          → add birds
DOWN        → remove birds
```

## 🎥 Recording

Recording is disabled by default.

To enable it, open `flock.py` and change:

```python
RECORDING = False
```

to:

```python
RECORDING = True
```

Then run:

```bash
pipenv run python flock.py
```

The video will be saved to:

```text
videos/boids_flocking.mp4
```

You can change the duration here:

```python
RECORD_SECONDS = 20
```

## 🧠 How It Works

Each bird follows three local rules:

- **Separation** — avoid crowding nearby birds
- **Alignment** — match direction with nearby birds
- **Cohesion** — move toward the local group center

Together, these simple rules create emergent flocking behavior.

## ⚡ Performance

The simulation uses spatial partitioning so birds only check nearby neighbors.

```text
Naive approach: O(n²)
Grid approach:  near O(n)
```

## 📁 Project Structure

```text
.
├── flock.py
├── Pipfile
└── videos/
```

## 🛠️ Tech Stack

- Python
- Pygame
- ImageIO
- Pipenv

## 📌 Future Improvements

- Predator bird behavior
- Sliders for live parameter tuning
- Export GIFs for GitHub previews
- Different flock species / colors
