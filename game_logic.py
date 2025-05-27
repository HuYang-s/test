# game_logic.py

# --- Data Structures ---

rooms = {
    "Cave Mouth": {
        "description": "You stand at the gaping maw of the Serpent's Coil. A chilling wind whistles through the entrance, carrying the scent of damp earth and something faintly reptilian. A narrow path disappears into the darkness to the east.",
        "exits": {"east": "Winding Tunnel"},
        "items": []
    },
    "Winding Tunnel": {
        "description": "The tunnel twists and turns, the walls slick with moisture. Strange phosphorescent fungi cast an eerie green glow, illuminating ancient, unreadable symbols carved into the rock. The path continues east, and a small fissure opens to the north.",
        "exits": {"east": "Glimmering Cavern", "north": "Fungus Grotto", "west": "Cave Mouth"},
        "items": ["Serpent's Eye Gem"]
    },
    "Fungus Grotto": {
        "description": "This small grotto is filled with a variety of glowing mushrooms. Their light dances on the damp walls, creating an almost magical atmosphere. A faint scratching sound can be heard from a pile of rocks in the corner.",
        "exits": {"south": "Winding Tunnel"},
        "items": ["Glowing Mushroom"]
    },
    "Glimmering Cavern": {
        "description": "This vast cavern glitters with thousands of tiny crystals embedded in the ceiling, reflecting the light from your torch (or the glowing fungi if you have one). In the center of the cavern, a rough-hewn stone pedestal stands empty. A narrow passage leads south.",
        "exits": {
            "west": "Winding Tunnel",
            "south": {"room": "Serpent's Lair", "required_item": "Serpent's Eye Gem"}
        },
        "items": []
    },
    "Serpent's Lair": {
        "description": "The air here is thick and heavy with a musky odor. Coiled upon a bed of old bones and discarded treasures is a colossal stone serpent, its eyes fixed upon you. The Amulet of Xylar rests on a small alcove behind the serpent.",
        "exits": {
            "north": {"room": "Glimmering Cavern", "required_item": "Amulet of Xylar"}
        },
        "items": ["Amulet of Xylar"]
    }
}

items = {
    "Glowing Mushroom": {
        "description": "A fist-sized mushroom that emits a soft, steady green light. It feels slightly warm to the touch.",
        "initial_location": "Fungus Grotto"
    },
    "Serpent's Eye Gem": {
        "description": "A smooth, fist-sized red gem that pulses with a faint inner light. It feels strangely warm.",
        "initial_location": "Winding Tunnel" # This item is initially in the room's item list
    },
    "Amulet of Xylar": {
        "description": "A heavy gold amulet shaped like a coiled serpent, with a large, empty socket in its center. It hums with a barely perceptible energy.",
        "initial_location": "Serpent's Lair"
    }
}

player = {
    "current_room": "Cave Mouth",
    "inventory": []
}

# --- Action Functions ---

def look(player_data, rooms_data):
    """
    Prints the description of the player's current room,
    lists available exits, and lists items visible in the room.
    """
    current_room_name = player_data["current_room"]
    room = rooms_data[current_room_name]

    print(f"\n{current_room_name}")
    print(room["description"])

    print("\nExits:")
    if room["exits"]:
        for direction in room["exits"]:
            print(f"- {direction}")
    else:
        print("There are no obvious exits.")

    print("\nItems in this room:")
    if room["items"]:
        for item_name in room["items"]:
            print(f"- {item_name}")
    else:
        print("You see no items here.")

def move(player_data, rooms_data, direction):
    """
    Moves the player to a new room if the direction is valid.
    Handles conditional exits based on required items.
    """
    current_room_name = player_data["current_room"]
    room = rooms_data[current_room_name]

    if direction in room["exits"]:
        exit_info = room["exits"][direction]

        if isinstance(exit_info, str): # Direct exit (no conditions)
            next_room_name = exit_info
            player_data["current_room"] = next_room_name
            print(f"You move {direction} to {next_room_name}.")
            look(player_data, rooms_data)
        elif isinstance(exit_info, dict): # Conditional exit
            required_item = exit_info.get("required_item")
            if required_item and required_item in player_data["inventory"]:
                next_room_name = exit_info["room"]
                player_data["current_room"] = next_room_name
                print(f"You use the {required_item} and move {direction} to {next_room_name}.")
                look(player_data, rooms_data)
            elif required_item:
                # Try to get item description for a more user-friendly message
                item_name_for_message = required_item
                if required_item in items: # Assuming 'items' global dict is accessible
                    item_name_for_message = items[required_item].get("description", required_item).lower()

                print(f"You try to go {direction}, but you are missing the {item_name_for_message}.")
            else: # Conditional exit without a required item specified (should not happen with current design)
                print(f"You can't go that way. The path seems blocked or incomplete.")
        else: # Should not happen with current data structure
             print("Error: Invalid exit definition.")
    else:
        print("You can't go that way.")

def take(player_data, rooms_data, items_data, item_name):
    """
    Allows the player to take an item from the current room.
    """
    current_room_name = player_data["current_room"]
    room = rooms_data[current_room_name]

    if item_name in room["items"]:
        # Check if item exists in the global items dictionary (it should)
        if item_name in items_data:
            player_data["inventory"].append(item_name)
            room["items"].remove(item_name)
            print(f"You take the {item_name}.")
        else:
            # This case should ideally not happen if data is consistent
            print(f"Error: {item_name} definition not found.")
    else:
        print(f"There is no {item_name} here.")

def inventory(player_data):
    """
    Prints the items in the player's inventory.
    """
    print("\nInventory:")
    if player_data["inventory"]:
        for item_name in player_data["inventory"]:
            print(f"- {item_name}")
    else:
        print("Your inventory is empty.")

def help_command(available_actions):
    """
    Prints a list of available commands.
    """
    print("\nAvailable commands:")
    for action in available_actions:
        print(f"- {action}")

# --- Available Actions (for help command) ---
available_actions = [
    "look",
    "move <direction>",
    "take <item_name>",
    "inventory",
    "help",
    "quit" # Will be handled in the main game loop
]

# --- Initialization (Example - can be expanded for a main game loop) ---
if __name__ == '__main__':
    # This is a simple demonstration of how functions might be called.
    # A proper game loop would be in a separate file (e.g., main.py).

    print("Welcome to the Serpent's Coil!")
    look(player, rooms)

    # Example sequence:
    # move(player, rooms, "east") # Move to Winding Tunnel
    # take(player, rooms, items, "Serpent's Eye Gem") # Try to take gem
    # inventory(player)
    # move(player, rooms, "north") # Move to Fungus Grotto
    # take(player, rooms, items, "Glowing Mushroom")
    # inventory(player)
    # move(player, rooms, "south") # Back to Winding Tunnel
    # move(player, rooms, "east") # To Glimmering Cavern
    # look(player, rooms)
    # move(player, rooms, "south") # Try to go to Serpent's Lair (will work for now)
    # take(player, rooms, items, "Amulet of Xylar")
    # inventory(player)
    # help_command(available_actions)
    pass
```
