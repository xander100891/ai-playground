# ✨ Particle Life Simulation (Pygame)

Interactive particle system where simple attraction and repulsion rules create complex, organic, and lifelike patterns.

## 🚀 Features

- Emergent particle behavior based on simple rules
- Multiple particle types with different interactions
- Smooth trails and fading effect
- Mouse interaction (attract / repel)
- Real-time simulation at 60 FPS
- Optional video recording

## 📦 Installation

```bash
pipenv sync
```

## ▶️ Run

```bash
pipenv run python particle_life.py
```

## 🎮 Controls

```text
Left click  → attract particles  
Right click → repel particles  
SPACE       → pause simulation  
R           → reset particles  
N           → generate new interaction rules  
```

## 🎥 Recording

Recording is disabled by default.

To enable it, open `particle_life.py` and change:

```python
RECORDING = False
```

to:

```python
RECORDING = True
```

Then run:

```bash
pipenv run python particle_life.py
```

The video will be saved to:

```text
videos/particle_life.mp4
```

You can change the duration here:

```python
RECORD_SECONDS = 20
```

## 🧠 How It Works

Each particle:

- has a type (color)
- interacts with nearby particles
- applies attraction or repulsion forces

The interaction is defined by a rule matrix:

```text
rules[type_a][type_b]
```

Simple local interactions create:

- swarms  
- clusters  
- rotating structures  
- flowing patterns  
- chaotic / stable ecosystems  

## ⚡ Performance

Current implementation:

```text
O(n²) interactions (each particle checks all others)
```

Recommended for best performance:

```text
200–400 particles
```

## 📁 Project Structure

```text
.
├── particle_life.py  
├── Pipfile  
└── videos/  
```

## 🛠️ Tech Stack

- Python  
- Pygame  
- ImageIO  
- Pipenv  

## 📌 Future Improvements

- Spatial grid optimization (O(n) instead of O(n²))  
- Glow / neon rendering  
- Adjustable parameters (UI sliders)  
- GIF export for GitHub preview  
- Rule presets for stable patterns  
