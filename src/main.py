"""
ICS3U
Paul Chen
This program is an adventure game called Dungeon Escape.
This file is the main entry point into the rest of the code.
"""

from os import name, system
from player import Player
from locations import Entrance, generate_enemies, generate_graph


def logo() -> None:
    """
	This function prints the logo of the game.
	Args
		None
	Returns
		None
	"""
    print("""
·▄▄▄▄  ▄• ▄▌ ▐ ▄  ▄▄ • ▄▄▄ .       ▐ ▄   ▄▄▄ ..▄▄ ·  ▄▄·  ▄▄▄·  ▄▄▄·▄▄▄ .
██· ██ █▪██▌•█▌▐█▐█ ▀ ▪▀▄.▀· ▄█▀▄ •█▌▐█  ▀▄.▀·▐█ ▀. ▐█ ▌▪▐█ ▀█ ▐█ ▄█▀▄.▀·
▐█▪ ▐█▌█▌▐█▌▐█▐▐▌▄█ ▀█▄▐▀▀▪▄▐█▌.▐▌▐█▐▐▌  ▐▀▀▪▄▄▀▀▀█▄██ ▄▄▄█▀▀█  ██▀·▐▀▀▪▄
██. ██ ▐█▄█▌██▐█▌▐█▄▪▐█▐█▄▄▌▐█▌.▐▌██▐█▌  ▐█▄▄▌▐█▄▪▐█▐███▌▐█▪ ▐▌▐█▪·•▐█▄▄▌
▀▀▀▀▀•  ▀▀▀ ▀▀ █▪·▀▀▀▀  ▀▀▀  ▀█▄▀▪▀▀ █▪   ▀▀▀  ▀▀▀▀ ·▀▀▀  ▀  ▀ .▀    ▀▀▀ 
""")


def menu() -> int:
    """
	This function prints the main menu, asks the user to choose an option, and returns the user's choice.
	Args
		None
	Returns
        int: 1 if play, 2 if tutorial, 3 if quit.
	"""
    # Prints the menu.
    print("""Select an option:
    1. Play
    2. Tutorial
    3. Quit
""")

    # Keeps taking in input until it is valid.
    inp = input("Your choice: ")
    while not inp.isdigit() or int(inp) < 1 or int(inp) > 3:
        print("Invalid Input")
        inp = input("Your choice: ")
    print()

    # Returns the result.
    return int(inp)


def difficulty() -> int:
    """
	This function prints a menu for difficulty, asks the user to choose an option, and returns the user's choice.
	Args
		None
	Returns
		int: 1 if easy, 2 if medium, 3 if hard.
	"""

    # Prints the menu.
    print("""Select a game mode:
    1. Easy
    2. Medium
    3. Hard
""")

    # Keeps taking in input until it is valid.
    inp = input("Your choice: ")
    while not inp.isdigit() or int(inp) < 1 or int(inp) > 3:
        print("Invalid Input")
        inp = input("Your choice: ")
    print()

    # Returns the result.
    return int(inp)


def tutorial() -> None:
    """
	This function prints the tutorial.
	Args
		None
	Returns
		None
	"""

    # Prints the tutorial.
    print("""
Welcome to Dungeon Escape! This game is a short adventure game where you are
a knight that must search through a dungeon for the hidden treasure. 

Goal: You must find the treasure and make it out of the dungeon.

Player: You have 2 stats: your HP and ATK. Your HP is the amount of health 
that you have. If this value drops to zero, you lose! Your ATK is the amount of
damage that your sword does with each hit. You also have a items that you can pick
up and store in your inventory

Combat: You may run into monsters in the dungeon that you have to fight. To fight
an enemy, you would be asked to type out multiple short, random sequences of letters.
The amount of damage that you deal is equal to the number of hits that you strike
(the number of times you type a sequence in a short span of time) multiplied by your ATK.

""")
    pass


def main() -> None:
    """
	This function is the main entry point to the code and contains the main game loop.
	Args
		None
	Returns
		None
	"""
    logo()

    # Keeps running until the user chooses to quit.
    menu_choice = menu()
    while menu_choice != 3:
        if menu_choice == 1: # Play
            # Gets difficulty
            mode = difficulty()

            # Sets up game
            player = Player(mode)
            generate_enemies(player.difficulty)
            generate_graph()
            curr = Entrance

            # Main game loop
            while (player):
                curr = curr(player).run()
        elif menu_choice == 2: # Tutorial
            tutorial()
        input("Type anything to continue... ")

        # Clears the screen
        if name == "posix":
            system("clear")
        else:
            system("cls")

        logo()
        menu_choice = menu()


if __name__ == "__main__":
    main()
