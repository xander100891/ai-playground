# Ant Colony Optimization Simulation

A cinematic ant colony optimization simulation built with **Python** and **Pygame**.

This project simulates emergent swarm behavior inspired by real ant colonies:
- pheromone trail routing
- procedural food generation
- dynamic harvesting
- obstacle navigation
- cinematic glowing visuals
- real-time controls
- MP4 recording support

---

## Features

- Emergent ant swarm behavior
- Real-time pheromone path formation
- Procedural food structures
- Dynamic food depletion + respawn
- Obstacle painting system
- Pause / play controls
- Add / remove ants live
- MP4 video recording
- Cinematic neon visual style

---

## Installation

Install dependencies:

```bash
pip install pygame numpy imageio imageio-ffmpeg
```

---

## Run

```bash
python ants.py
```

---

## Controls

| Key | Action |
|---|---|
| SPACE | Pause / Play |
| + / - | Add / Remove ants |
| C | Clear pheromone trails |
| V | Start / Stop MP4 recording |
| H | Toggle help menu |
| ESC | Quit |

### Mouse

| Mouse | Action |
|---|---|
| Left Click | Spawn food |
| Right Hold | Draw obstacles |

---

## Recording

Press:

```text
V
```

to start/stop MP4 recording.

Videos are automatically saved as:

```text
ants_recording.mp4
```

---

## Visual Style

The simulation uses:
- glowing pheromone trails
- cinematic dark-blue palette
- procedural pixel food clusters
- organic cave-like obstacles
- micro-scale glowing ants

Designed for:
- YouTube visuals
- AI simulation showcases
- generative art
- emergent behavior experiments

---

## Project Structure

```text
ants.py
README.md
ants_recording.mp4
```

---

## License

MIT License
