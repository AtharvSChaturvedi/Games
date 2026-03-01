# Tic-Tac-Toe AI — Search Algorithms

A Tic-Tac-Toe game built with Pygame where the AI opponent uses three classic search algorithms: **BFS**, **DFS**, and **A\***. Switch between algorithms mid-game and watch the stats update in real time.

![Python](https://img.shields.io/badge/Python-3.7+-blue) ![Pygame](https://img.shields.io/badge/Pygame-2.0+-green)

---

## Features

- **Human vs AI** gameplay — you play as X, the AI plays as O
- **Three AI algorithms** selectable at any time:
  - **BFS** (Breadth-First Search) — explores the game tree level by level
  - **DFS** (Depth-First Search) — explores deeply using a minimax-style approach
  - **A\*** (A-Star) — uses a heuristic to prioritize promising game states
- **Live search stats** — nodes explored and computation time displayed after each AI move
- Clean, minimal UI with algorithm selector and reset button

---

## Requirements

- Python 3.7+
- Pygame

Install dependencies:

```bash
pip install pygame
```

---

## Running the Game

```bash
python tictactoe.py
```

---

## How to Play

1. Click any cell on the board to place your **X**
2. The AI will respond automatically as **O**
3. Use the **BFS / DFS / A\*** buttons (bottom-right) to switch the AI algorithm
4. Click **Reset Game** to start a new game at any time

---

## Algorithm Details

### BFS (Breadth-First Search)
Explores all immediate moves first, then expands level by level up to a depth of 3. Scores moves based on how quickly they lead to wins or losses. Good at finding short-term winning moves but less strategic at depth.

### DFS (Depth-First Search)
Uses a recursive minimax approach with a depth limit of 4. Maximizes the AI's score while minimizing the player's score. More strategically sound than BFS due to the alternating min/max evaluation.

### A* (A-Star Search)
Combines a path cost (depth) with a heuristic that scores board positions based on winning pattern potential. Uses a priority queue to explore the most promising states first, balancing speed and strategy.

---

## Project Structure

```
tictactoe.py   # Main game file — all logic, rendering, and AI in one script
README.md
```

---

## Controls

| Action | Input |
|---|---|
| Place X | Left-click on board cell |
| Switch AI algorithm | Click BFS / DFS / A* button |
| Reset game | Click Reset Game button |
| Quit | Close window |
