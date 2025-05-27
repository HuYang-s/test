# adventure_game.py
from game_logic import player, rooms, items, look, move, take, inventory, help_command

def game_loop():
    # Initialize game (e.g., print welcome message)
    print("Welcome to the Serpent's Coil!")
    
    # Initial player and item setup
    player["current_room"] = "Cave Mouth"
    player["inventory"] = []

    # Reset items in rooms to their initial designed state
    # This ensures that if the game is run multiple times, items are where they should be.
    rooms["Cave Mouth"]["items"] = []
    rooms["Winding Tunnel"]["items"] = ["Serpent's Eye Gem"] 
    rooms["Fungus Grotto"]["items"] = ["Glowing Mushroom"]
    rooms["Glimmering Cavern"]["items"] = []
    # Amulet is in Serpent's Lair, but might be conditional later based on serpent
    rooms["Serpent's Lair"]["items"] = ["Amulet of Xylar"] 

    # Initial look around
    look(player, rooms)

    available_actions = ["look", "move <direction>", "take <item_name>", "inventory", "help", "quit"]

    while True:
        user_input = input("What do you do? ").strip().lower()
        if not user_input: # Handle empty input
            continue

        parts = user_input.split()
        command = parts[0]
        
        argument = None
        if len(parts) > 1:
            argument = " ".join(parts[1:]) # Handle multi-word arguments correctly

        if command == "quit":
            print("Thanks for playing! Goodbye.")
            break
        elif command == "look":
            look(player, rooms)
        elif command == "move":
            if argument:
                move(player, rooms, argument)
                # game_logic.move() calls look() on successful move.
            else:
                print("Move where? (e.g., 'move north')")
        elif command == "take":
            if argument:
                # We need to ensure the item name taken from input matches an item key in 'items'
                # or an item name present in the room's item list.
                # The current 'take' function in game_logic.py handles this by checking item_name in room["items"].
                take(player, rooms, items, argument)
                # Check for win condition after taking an item
                if "Amulet of Xylar" in player['inventory']:
                    print("\nCongratulations! You have retrieved the Amulet of Xylar from the Serpent's Lair!")
                    print("The ground trembles as the ancient magic of the amulet courses through you.")
                    print("You have proven your worth as a true treasure hunter!")
                    print("Your quest is complete. Thanks for playing!")
                    break
            else:
                print("Take what? (e.g., 'take glowing mushroom')")
        elif command == "inventory":
            inventory(player)
        elif command == "help":
            help_command(available_actions)
        else:
            print("Invalid command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    # The game_loop() function now handles its own state initialization.
    game_loop()
```
