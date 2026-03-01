# 🏍️ TRON Light Cycle

A terminal-free, neon-lit **Tron Light Cycle** game built with Python and Pygame — featuring an enemy AI powered by **A\* Search** with a flood-fill survival fallback.

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Pygame](https://img.shields.io/badge/Pygame-required-green)

---

## Gameplay

You pilot a cyan light cycle across a grid. Every cell you pass through leaves a permanent trail — ride into any trail (including your own) or the wall and you crash. The red enemy AI does everything it can to cut you off. Last cycle moving wins.

---

## Features

- **A\* pathfinding enemy** — re-plans every 3 frames to intercept your predicted future position
- **Flood-fill survival fallback** — when A\* can't find a path, the AI picks the direction with the most open space to stay alive as long as possible
- **Neon glow rendering** — glowing cycle heads, coloured trails, dark grid
- **Win/lose/draw detection** — including simultaneous head-on collisions
- **Score tracking** across rounds

---

## Controls

| Key | Action |
|---|---|
| `↑ W` | Move up |
| `↓ S` | Move down |
| `← A` | Move left |
| `→ D` | Move right |
| `R` | Restart after game over |
| `ESC` | Quit |

---

## Installation & Running

**1. Clone or download the project**

```bash
git clone <repo-url>
cd tron-light-cycle
```

**2. Install the dependency**

```bash
pip install pygame
```

**3. Run the game**

```bash
python tron.py
```

---

## How the AI Works

The enemy uses an **agentic perceive → plan → act loop** on every game tick:

1. **Perceive** — builds a set of all blocked cells (both trails)
2. **Plan (A\*)** — searches for the optimal path to the player's *predicted* position 5 steps ahead; falls back to the player's current position if the predicted one is unreachable
3. **Act** — follows the planned path one step at a time, replanning every 3 frames

If no path exists at all, the AI switches to a **flood-fill survival strategy** — scoring each available direction by how many cells are reachable from it and picking the most open one.

The A\* heuristic is **Manhattan distance**, which is admissible (never overestimates) and consistent, guaranteeing the shortest path is found.

---

## Requirements

- Python 3.8+
- pygame
