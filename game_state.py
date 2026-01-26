import json
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Player: 
    x: int = 0
    y: int = 0
    health: int = 100
    inventory: List[str] = field(default_factory=list)


@dataclass
class Item:
    id: str
    name: str
    x: int
    y: int
    picked: bool = False


@dataclass
class EnvironmentObject:
    id: str
    type: str  # "door" / "switch"
    state: str  # "open"/"closed" or "on"/"off"


@dataclass
class GameState:
    width: int = 10
    height: int = 10
    player: Player = field(default_factory=Player)
    items: Dict[str, Item] = field(default_factory=dict)
    env_objects: Dict[str, EnvironmentObject] = field(default_factory=dict)


def create_initial_state() -> GameState:
    # Rationale:
    # Centralized initial state creation keeps testing consistent and makes reset easy.
    # Adding new items/objects later is simple because all defaults are in one place.
    state = GameState()

    # Items in the world
    state.items["p1"] = Item(id="p1", name="Potion", x=2, y=2)
    state.items["k1"] = Item(id="k1", name="Key", x=5, y=5)

    # Environment objects
    state.env_objects["d1"] = EnvironmentObject(id="d1", type="door", state="closed")
    state.env_objects["s1"] = EnvironmentObject(id="s1", type="switch", state="off")

    return state


def reset_game_state() -> GameState:
    # Rationale:
    # Reset reuses create_initial_state() to avoid duplicate initialization logic.
    # This guarantees reset state is always identical to the initial game setup.
    return create_initial_state()


def move_player(state: GameState, new_x: int, new_y: int) -> bool:
    # Rationale:
    # Boundary validation is done before updating the player's coordinates to prevent invalid state.
    # This keeps the player always inside the playable world and avoids broken game logic later.

    # boundary check
    if new_x < 0 or new_x >= state.width or new_y < 0 or new_y >= state.height:
        print("Invalid move: out of bounds")
        return False

    state.player.x = new_x
    state.player.y = new_y
    print(f"Player moved to ({new_x}, {new_y})")
    return True


def pickup_item(state: GameState, item_id: str) -> bool:
    # Rationale:
    # Items are stored in a dictionary (hash-map) for O(1) lookup using item_id.
    # Pickup requires the player to be on the same tile as the item to keep the rule simple and deterministic.

    # item exists
    if item_id not in state.items:
        print("Invalid item id")
        return False

    item = state.items[item_id]

    # already picked
    if item.picked:
        print("Item already picked")
        return False

    # player near item  (same position check)
    if state.player.x != item.x or state.player.y != item.y:
        print("Player is not at the item location")
        return False

    # pick it
    item.picked = True
    state.player.inventory.append(item_id)
    print(f"Picked item: {item.name} ({item_id})")
    return True


def use_item(state: GameState, item_id: str) -> bool:
    # Rationale:
    # We only allow using items that exist in the player's inventory to prevent invalid actions.
    # Item effects are handled by item name/type, making it easy to extend with new items later.

    # check inventory
    if item_id not in state.player.inventory:
        print("You don't have this item")
        return False

    item = state.items.get(item_id)

    # item exists in world list
    if item is None:
        print("Item not found in game state")
        return False

    # apply effect based on item name
    if item.name == "Potion":
        state.player.health += 20
        if state.player.health > 100:
            state.player.health = 100

        # consume potion (remove from inventory)
        state.player.inventory.remove(item_id)
        print("Potion used. Health increased.")
        return True

    elif item.name == "Key":
        print("Key cannot be used directly. Try interacting with a door.")
        return False

    else:
        print("Unknown item. No effect.")
        return False


def interact_with_environment(state: GameState, object_id: str) -> bool:
    # Rationale:
    # Environment objects are stored by ID for fast interaction lookup.
    # Interactions are implemented as a toggle (open/close or on/off) because it's the simplest state transition model.

    if object_id not in state.env_objects:
        print("Environment object not found")
        return False

    obj = state.env_objects[object_id]

    # Door toggle
    if obj.type == "door":
        if obj.state == "closed":
            obj.state = "open"
        else:
            obj.state = "closed"

        print(f"Door {object_id} is now {obj.state}")
        return True

    # Switch toggle
    if obj.type == "switch":
        if obj.state == "off":
            obj.state = "on"
        else:
            obj.state = "off"

        print(f"Switch {object_id} is now {obj.state}")
        return True

    print("Unknown environment object type")
    return False


def save_game(state: GameState, filepath: str) -> None:
    # Rationale:
    # JSON is chosen because it is human-readable, easy to debug, and easy to serialize in Python.
    # Converting the game state into dictionaries ensures it can be stored and restored reliably.

    data = {
        "width": state.width,
        "height": state.height,
        "player": {
            "x": state.player.x,
            "y": state.player.y,
            "health": state.player.health,
            "inventory": state.player.inventory
        },
        "items": {
            item_id: {
                "id": item.id,
                "name": item.name,
                "x": item.x,
                "y": item.y,
                "picked": item.picked
            }
            for item_id, item in state.items.items()
        },
        "env_objects": {
            obj_id: {
                "id": obj.id,
                "type": obj.type,
                "state": obj.state
            }
            for obj_id, obj in state.env_objects.items()
        }
    }

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Game saved to {filepath}")


def load_game(filepath: str) -> GameState:
    # Rationale:
    # Loading reconstructs the GameState from JSON so gameplay can resume exactly from the saved state.
    # Keeping persistence separate from gameplay logic improves modularity and maintainability.

    with open(filepath, "r") as f:
        data = json.load(f)

    state = GameState()
    state.width = data["width"]
    state.height = data["height"]

    # load player
    state.player.x = data["player"]["x"]
    state.player.y = data["player"]["y"]
    state.player.health = data["player"]["health"]
    state.player.inventory = data["player"]["inventory"]

    # load items
    state.items = {}
    for item_id, item_data in data["items"].items():
        state.items[item_id] = Item(
            id=item_data["id"],
            name=item_data["name"],
            x=item_data["x"],
            y=item_data["y"],
            picked=item_data["picked"]
        )

    # load environment objects
    state.env_objects = {}
    for obj_id, obj_data in data["env_objects"].items():
        state.env_objects[obj_id] = EnvironmentObject(
            id=obj_data["id"],
            type=obj_data["type"],
            state=obj_data["state"]
        )

    print(f"Game loaded from {filepath}")
    return state
