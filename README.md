# Othello-Engine


>  **Visuals Under Construction** – Game UI and board visualizations will be added soon!

## Overview

This project implements a search-based Othello (Reversi) engine using classical AI techniques. The core logic relies on **minimax** and **negamax** algorithms enhanced with **alpha-beta pruning** to optimize move selection and computational efficiency.

The engine evaluates possible future board states using a custom heuristic function that considers **positional advantage**, **disc parity**, **corner control**, and **mobility**.

## Features

- **Minimax & Negamax** search algorithms  
- **Alpha-beta pruning** for pruning unpromising branches  
- **Heuristic evaluation** using game-specific board weights  
- Tested over 500 matches with a **73% win rate** against human players and baseline bots  
- Efficient depth-limited search with optional iterative deepening

## Future Work

- Add interactive board and game visualizations (in progress)  
- Integrate with benchmarking suite for strategy comparison  
- Optional multiplayer support via socket or REST endpoints

## Usage

```bash
python3 othello_engine.py

