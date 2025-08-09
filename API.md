# The Serpent's Coil — API Reference

This document describes the public modules, functions, and data structures exposed by the game. It also provides examples for common usage patterns and guidance for extending the game.

- Project language: Python 3
- Entry point: `adventure_game.py`
- Core game logic: `game_logic.py`

## Quick Start

- Run the interactive game:

```bash
python adventure_game.py
```

- Import and use the APIs programmatically from another Python script:

```python
from game_logic import player, rooms, items, look, move, take, inventory, help_command

# Reset state (a minimal reset, mirroring what the game loop does)
player["current_room"] = "Cave Mouth"
player["inventory"] = []

rooms["Cave Mouth"]["items"] = []
rooms["Winding Tunnel"]["items"] = ["Serpent's Eye Gem"]
rooms["Fungus Grotto"]["items"] = ["Glowing Mushroom"]
rooms["Glimmering Cavern"]["items"] = []
rooms["Serpent's Lair"]["items"] = ["Amulet of Xylar"]

look(player, rooms)              # Prints the current room state
move(player, rooms, "east")     # Attempt to move east
take(player, rooms, items, "Serpent's Eye Gem")
inventory(player)
```

---

## Module: `game_logic`

This module holds the canonical game state (mutable dictionaries) and the functions that implement player actions.

### Data Structures

- `rooms: dict[str, dict]`
  - Maps room names to room definitions.
  - A room definition includes:
    - `description: str`
    - `exits: dict[str, str | dict]`
      - Example direct exit: `{ "east": "Winding Tunnel" }`
      - Example conditional exit: `{ "south": { "room": "Serpent's Lair", "required_item": "Serpent's Eye Gem" } }`
    - `items: list[str]` — names of items present in the room.

- `items: dict[str, dict]`
  - Maps item names to item definitions.
  - An item definition includes:
    - `description: str`
    - `initial_location: str`

- `player: dict`
  - The mutable player state used by the action functions.
  - Keys:
    - `current_room: str`
    - `inventory: list[str]`

- `available_actions: list[str]`
  - Canonical list of supported player commands, used by `help_command`.

Important: All of the above structures are mutable and passed by reference to the functions below. The action functions mutate these structures (e.g., moving rooms, adding/removing items).

### Functions

- `look(player_data: dict, rooms_data: dict) -> None`
  - Prints the current room name, description, visible exits, and items present.
  - Side effects: None beyond printing.
  - Example:

```python
from game_logic import player, rooms, look
look(player, rooms)
```

- `move(player_data: dict, rooms_data: dict, direction: str) -> None`
  - Attempts to move the player along `direction` from `player_data["current_room"]`.
  - Supports both direct exits and conditional exits requiring a specific item.
  - On a successful move, it also calls `look(...)` to describe the new room.
  - Prints user-friendly messages for invalid directions or missing required items.
  - Example (direct and conditional):

```python
from game_logic import player, rooms, move, take, items, look

# Start in Cave Mouth, go east to Winding Tunnel
move(player, rooms, "east")

# The southern exit from Glimmering Cavern requires the Serpent's Eye Gem
move(player, rooms, "east")   # to Glimmering Cavern
move(player, rooms, "south")  # will print a message about the missing required item

# Acquire the gem, then try again
move(player, rooms, "west")
take(player, rooms, items, "Serpent's Eye Gem")
move(player, rooms, "east")
move(player, rooms, "south")
```

- `take(player_data: dict, rooms_data: dict, items_data: dict, item_name: str) -> None`
  - If `item_name` is present in the current room, adds it to the player's inventory and removes it from the room.
  - Validates the item exists in `items_data`.
  - Example:

```python
from game_logic import player, rooms, items, take

take(player, rooms, items, "Glowing Mushroom")
```

- `inventory(player_data: dict) -> None`
  - Prints the list of item names in the player inventory.
  - Example:

```python
from game_logic import player, inventory
inventory(player)
```

- `help_command(available_actions: list[str]) -> None`
  - Prints a simple list of supported commands.
  - Example:

```python
from game_logic import available_actions, help_command
help_command(available_actions)
```

### Error Handling Notes

- `move(...)` prints informative messages for invalid directions or when a required item is missing.
- `take(...)` prints an error if the item is not in the room or if the item is not defined in `items_data`.
- The functions are designed for interactive console output and do not raise exceptions for user errors.

### Extending the World

- Add a room:

```python
rooms["Hidden Alcove"] = {
    "description": "A cramped alcove tucked behind a curtain of stalactites.",
    "exits": {"west": "Glimmering Cavern"},
    "items": ["Ancient Coin"],
}
```

- Add a conditional exit:

```python
rooms["Glimmering Cavern"]["exits"]["south"] = {"room": "Serpent's Lair", "required_item": "Serpent's Eye Gem"}
```

- Add an item:

```python
items["Ancient Coin"] = {
    "description": "A coin minted with an unfamiliar crest.",
    "initial_location": "Hidden Alcove",
}
```

---

## Module: `adventure_game`

This module contains the interactive loop that wires user input to the action functions.

- `game_loop() -> None`
  - Initializes canonical game state for a fresh session.
  - Greets the player, prints the initial room via `look(...)`, and continuously prompts for input.
  - Commands supported: `look`, `move <direction>`, `take <item_name>`, `inventory`, `help`, `quit`.
  - Win condition: picking up the `Amulet of Xylar` prints a victory message and ends the loop.

### Running the Loop Programmatically

```python
from adventure_game import game_loop

game_loop()
```

The loop manages its own state resets, so it is safe to call as the main entry point when embedding into a larger application.

---

## Command Reference (Player-Facing)

- `look`
  - Prints the current room and visible details.
- `move <direction>`
  - Attempts to move in one of: `north`, `south`, `east`, `west` (as defined by the current room's exits).
- `take <item_name>`
  - Picks up a visible item from the room and adds it to your inventory.
- `inventory`
  - Lists your items.
- `help`
  - Shows available commands.
- `quit`
  - Exits the game.

---

## Notes on State and Purity

- The APIs in `game_logic` are intentionally stateful and perform printing side effects.
- If you need to test without printing, consider capturing stdout or refactoring by introducing pure functions that return data structures representing the view model (not included in this version).