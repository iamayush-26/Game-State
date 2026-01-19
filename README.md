# 2D Game State Management (Python)

## Overview
This project implements a simple 2D game state management system using Python. The main goal of the project is to demonstrate how a game’s internal data (state) can be represented, updated through player actions, and saved/loaded using a human-readable format like JSON. This assignment focuses on state handling and logic design rather than graphics, rendering, or using a game engine.

---

## What this project includes
The game state is designed to store the most important information required to run a basic game simulation. It includes player information such as position, health, and inventory. It also tracks items placed in the world, their locations, and whether they have been picked up or not. In addition, it supports basic environment objects such as doors and switches, where the state can change (open/closed or on/off). The project also supports saving the full game state into a JSON file and loading it back to continue gameplay from the same point.

---

## How to run
To run the project, open the project folder in a terminal and execute the following command:

```bash
python main.py
Running the file demonstrates the complete flow of the system, including movement, picking up an item, using an item, interacting with the environment, saving/loading, and resetting the game state.
```

## Game State Design (State Representation)
The game state is represented using Python dataclasses to keep the code clean, readable, and structured.

The Player dataclass stores the player's position using (x, y) coordinates, the current health value, and an inventory list to hold picked item IDs.

The Item dataclass represents objects in the world and stores fields like unique ID, item name, location, and whether the item has already been picked.

The EnvironmentObject dataclass stores interactive world objects such as doors and switches with a unique ID, a type field, and the current state value.

All of these are combined inside the GameState dataclass, which stores the map boundaries (width and height), the player object, a dictionary of items, and a dictionary of environment objects.

Storing items and environment objects in dictionaries makes lookup by ID fast and simple.

## State Transition Functions (Game Actions)
The project supports multiple basic game actions through dedicated state transition functions.

The move_player() function updates the player’s coordinates only if the new position stays inside the map boundaries.

The pickup_item() function allows the player to pick an item only if the item exists, has not already been picked up, and the player is standing on the same location as the item.

The use_item() function allows the player to consume an item from the inventory. In the current implementation, a Potion increases the player's health (capped at 100) and is removed from the inventory after use.

The interact_with_environment() function supports basic interactions with environment objects such as toggling a door between open/closed and toggling a switch between on/off.

These state transition functions are kept separate from the data structures to maintain a clear separation of concerns and improve maintainability.

## Edge Cases and Validation
This project includes basic validation and edge case handling to prevent invalid state changes.

The player cannot move outside the world boundaries.

Picking up an item is not allowed if the item ID is invalid, the item has already been picked, or the player is not at the item’s position.

Using an item is not allowed if the item is not present in the inventory.

Health is capped at 100 to prevent unrealistic values.

Interactions with environment objects are validated to ensure the target object exists before attempting to modify its state.

## Save and Load System (Persistence)
The game state can be saved into a JSON file using save_game(). JSON was chosen because it is human-readable, easy to debug, and convenient to generate in Python.

The entire state (player details, item states, environment states, and world size) is written into a structured JSON file. The state can later be restored using load_game(), which reads the JSON file and reconstructs the same GameState objects so gameplay can continue from the exact saved state.

## Extensibility
The design is intended to be easily extendable.

New items can be added by inserting them into the items dictionary and extending the item logic inside use_item() if needed.

New environment objects can be added by introducing new type values and handling them inside interact_with_environment().

New player attributes such as stamina, experience, or level can also be added inside the Player dataclass without affecting the rest of the system.

As an example, adding a new item like a Shield would only require defining it and adding its effect in the use_item() function.

## Assumptions
This project assumes a simple 2D grid-based world with fixed boundaries (default 10×10). Item pickup is only possible when the player is on the exact same location as the item. The maximum player health is assumed to be 100.

The Key item is included for demonstration purposes but is not directly usable in the current implementation. The save and load functionality assumes the JSON file format is valid.

Usage in a Larger Game
In a more complex game, this state system can serve as the single source of truth for all systems.

Rendering systems can read the state to draw the player and world.

Input systems can modify state through controlled action functions.

AI systems and physics systems can also update state in a structured order to prevent conflicts.

The save/load system can be expanded to support multiple save slots, versioning, and stronger corrupted-file handling.

## Reflection and Rationale
### Design Choices
The main focus of the design was to keep the implementation simple, modular, and easy to understand. Python dataclasses were used to create readable state containers, and dictionaries were chosen for items and environment objects to allow fast lookup using IDs. State transition functions were kept separate from data structures to maintain clean separation of concerns and avoid mixing representation with logic.

### Trade-offs
The implementation prioritizes clarity and correctness over extreme optimization. Error handling is intentionally basic to match the scope of the assignment, while still preventing common invalid state transitions. Some mechanics are kept intentionally simple (such as exact-position pickup) to keep the system deterministic and easy to test.

### Areas of Uncertainty
Handling corrupted save files has been kept minimal in this version. In a production system, additional validation, error recovery, and backward compatibility strategies would be added to ensure safe loading of game state even if files are incomplete or damaged.

### AI Assistance
I used ChatGPT as a support tool during development to help structure and improve documentation clarity.  However, I reviewed all suggestions, tested the code thoroughly, and modified the implementation to handle important edge cases such as invalid movement, invalid item interactions, inventory validation, and health limits. The final code reflects my own understanding and decisions, with AI used mainly to speed up development and improve readability.

### Setup / Testing Instructions
Clone the repository.

Open the project folder in a terminal.

Run the demo using:
python main.py
