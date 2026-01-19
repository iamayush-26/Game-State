# 2D Game State Management (Python)

## What this project does
This project implements a simple 2D game state system:
- Player state (position, health, inventory)
- Items in the world (location, picked/not picked)
- Environment objects (door/switch states)
- Save and Load game state using JSON

## How to run
```bash
python main.py
```
## Features
- Player movement with boundary checks
- Item pickup and inventory management
- Item usage (Potion increases health)
- Environment interaction (door/switch toggle)
- Game state save to JSON
- Game state load from JSON
- Reset game state to initial configuration

## Core Functions
- `move_player()` – Moves player within map boundaries
- `pickup_item()` – Picks item if player is at item location
- `use_item()` – Uses item from inventory
- `interact_with_environment()` – Toggles door or switch state
- `save_game()` – Saves game state to JSON file
- `load_game()` – Loads game state from JSON file
- `reset_game_state()` – Resets game to initial state


## Edge Cases Handled
- Prevents player from moving outside the world boundaries
- Prevents picking up an item if:
  - item id is invalid
  - item is already picked
  - player is not at the item location
- Prevents using an item if it is not in inventory
- Health is capped at 100 when using a Potion
- Prevents interacting with environment objects that do not exist

## Reflection and Rationale

### Design Choices
- Used `dataclasses` for clean and readable state representation.
- Used dictionaries (`items`, `env_objects`) to allow fast lookup using IDs.
- Kept state update logic in separate functions to maintain separation of concerns.

### Trade-offs
- Focused on simplicity and clarity over extreme optimization.
- Used basic validations instead of very complex error handling to match the assignment scope.

### Areas of Uncertainty
- Save file corruption handling is kept minimal (can be improved with try/except and defaults).

### AI Assistance (If Any)
- I used ChatGPT to get guidance on structuring the code and writing the README.
- I reviewed and edited the code to ensure it matches the assignment requirements and handles edge cases.
