"""
ICS3U
Paul Chen
This file holds the code for the `Location` class as well as all the classes that inherit
from it. It holds all the information about the locations present in the game.
"""

import enemy
from player import Player
from random import choice, randint


class Location:
    """Class that represents a location. Each location represents a node in the tree that 
    represents the map. These locations would be connected together at random at game start.

    Attributes:
        rooms (list[Location]): the rooms that are adjacent to the current location.
        enemies (list[Enemy]): the enemies present in a location.
        possible_enemies (list[Enemy]): the enemies that can appear in a room. Used when enemies 
            are generated. This list is left empty if the enemies in the room aren't generated at random.
        name (str): the name of the location.
        visited (bool): True if the room as been visited else False.
        player (Player): the player.
    """
    rooms: list
    enemies: list
    possible_enemies: list
    name: str
    visited: bool

    def __init__(self, player: Player):
        """
        Inits location class.
        Args
            player (Player): the player.
        """
        self.player = player

    def on_enter(self) -> None:
        """
        Runs after a the player enters a room. By default it adds a message saying that you have entered a room.
        Args
            None
        Returns
            None
        """
        self.player.io.push(f"You entered the {self.name}.")

    def description(self) -> str:
        """
        Returns the description of the room.
        Args
            None
        Returns
            str: the description of the room.
        """
        pass

    def display(self) -> None:
        """
        Updates the display with the new info in the room.
        Args
            None
        Returns
            None
        """
        # Adds the location description, name; the player's HP, ATK, and items; and the enemies present in the room.
        self.player.io.set_room_info(f"""{self.description()}

    Location: {self.name}
    HP: {self.player.hp}
    ATK: {self.player.atk}
    Items: [{", ".join(self.player.items)}]

{"Enemies in this room: [" + (", ".join(e.name for e in reversed(self.enemies))) + "]"}
""")

    def battle(self) -> None:
        """
        Function that runs the battle between the player and the enemies.
        Args
            None
        Returns
            None
        """
        # If there are no enemies exit.
        if len(self.enemies) == 0:
            return

        # Lambda function to generate the determiner that precedes a word.
        determiner = lambda next: "An" if next[0].lower() in "aeiou" else "A"

        # Main battle loop, keeps running until all the enemies in the room have been defeated.
        while len(self.enemies) and self.player:
            enemy_name = self.enemies[-1].name  # Enemy's name
            enemy_inst = self.enemies[-1]()  # Instance of Enemy's class

            # Add message.
            self.player.io.push(
                f"""{determiner(enemy_name)} {enemy_name} walks up to you...
    HP: {enemy_inst.hp}
    ATK: {enemy_inst.atk}""")

            # Loop that keeps running until either the current enemy or the player dies.
            while enemy_inst.hp > 0 and self.player:
                # The player's attack
                num_hits = self.player.attack(
                    enemy_inst.difficulty)  # Number of hits
                dmg_dealt = num_hits * self.player.atk  # Damage dealt
                self.player.io.push(
                    f"You have hit {num_hits} times dealing {dmg_dealt} damage."
                )
                enemy_inst.hp = max(0, enemy_inst.hp - dmg_dealt)
                self.player.io.push(
                    f"The {enemy_name} is left with {enemy_inst.hp} HP.")

                # Checks if the enemy is has been defeated, if so, break out of the loop.
                if enemy_inst.hp == 0:
                    self.player.io.push(
                        f"The {enemy_name} has been defeated! You win!")
                    self.enemies.pop()
                    self.display(
                    )  # We popped an enemy from the list, so we redraw the screen.
                    break

                # The enemy's attack
                enemy_hits = enemy_inst.attack()  # Number of hits
                enemy_dmg = enemy_hits * enemy_inst.atk  # Damage dealt
                self.player.io.push(
                    f"The {enemy_name} has hit you {enemy_hits} times dealing {enemy_dmg} damage."
                )
                self.player.hp = max(0, self.player.hp - enemy_dmg)
                self.display(
                )  # The player's HP would've changed, so we redraw the screen.
        if self.player.hp == 0:  # Player loses.
            self.player.io.push(f"Your HP has dropped to 0.\nGame Over")
        else:  # Player wins.
            self.player.io.push("You have defeated every monster in the room!")

    def on_battle_finish(self) -> None:
        """
        Runs after a the player exits a room.
        Args
            None
        Returns
            None
        """
        pass

    def choose_room(self) -> "Location":
        """
        Code that allows the user to choose the next room they visit.
        Args
            None
        Returns
            Location: next location to visit.
        """
        # Displays the list of rooms that can be travelled to.
        self.player.io.push("Choose one of the following rooms to go to: " + "".join(
            f"\n    {i + 1}. {self.rooms[i].name}"
            for i in range(len(self.rooms))))

        # Keeps taking in input until it is valid.
        inp = self.player.io.input("Where would you like to go: ")
        while not inp.isdigit() or int(inp) < 1 or int(inp) > len(self.rooms):
            self.player.io.push("Invalid Input")
            inp = self.player.io.input("Where would you like to go: ")
        return self.rooms[int(inp) - 1]

    def run(self) -> "Location":
        """
        Runs the events that happen at a location.
        Args
            None
        Returns
            Location: next location to visit.
        """
        self.on_enter()
        self.display()
        self.battle()
        # If the player dies, exit.
        if not self.player:
            return None
        self.on_battle_finish()
        # The player could still die here if they are in the witch's hut and drink a potion that kills them.
        if not self.player:
            return None
        self.enemies.clear()
        return self.choose_room()


class Entrance(Location):
    """Class for the entrance of the dungeon. This location serves as the beginning of the game
    as well as the location of the boss fight.

    Attributes:
        rooms (list[Location]): the rooms that are adjacent to the current location. This list 
            isn't randomly generated and should only contain `Stairway`.
        enemies (list[Enemy]): the enemies present in a location. This list should be empty at the beginning of 
            the game and should contain one `Dragon` at the end which also serves as the final boss of the game.
        possible_enemies (list[Enemy]): the enemies that can appear in a room. This list should always be empty.
        name (str): the name of the location.
        visited (bool): True if the room as been visited else False.
    """
    rooms = []
    enemies = []
    possible_enemies = []
    name = "Entrance"
    visited = False

    def on_enter(self) -> None:
        """
        Adds a dragon to the list of enemies when you revisit this room at the end.
        Args
            None
        Returns
            None
        """
        super().on_enter()
        if Entrance.visited:
            Entrance.enemies.append(enemy.Dragon)

    def description(self) -> str:
        """
        Returns the description for the room. Returns an introduction the first time this 
        room is visited, and a boss battle message the second time.
        Args
            None
        Returns
            str: the description.
        """
        if Entrance.visited:
            return """Just as you think that you have made it out alive, a dragon flies down 
from the sky and lands next to you!"""
        return """You are a knight looking for a treasure chest hidden in the DUNGEON OF DOOM.
Search through the dungeon to find it!"""

    def on_battle_finish(self) -> None:
        """
        Does nothing the first time the player passes through the room, ends the game 
        when the player defeats the dragon.
        Args
            None
        Returns
            None
        """
        if Entrance.visited:
            self.player.io.push(
                "You have found the treasure and defeated the dragon! You Win!"
            )
            self.player.hp = 0
        Entrance.visited = True


class Stairway(Location):
    """Class for a stairway connecting the entrance and the rest of the dungeon. This location
    serves as an introduction for the player where they figure out how the battle mechanic works.

    Attributes:
        rooms (list[Location]): the rooms that are adjacent to the current location. This list 
            isn't randomly generated and should only contain `Entrance` and `Hall`. After the player
            enters this room, `Entrance` is taken off of this list until the player finds the key
            and the treasure.
        enemies (list[Enemy]): the enemies present in a location. This list should only contain one `Guard`.
        possible_enemies (list[Enemy]): the enemies that can appear in a room. This list should always be empty.
        name (str): the name of the location.
        visited (bool): True if the room as been visited else False.
    """
    rooms = []
    enemies = [enemy.Guard]
    possible_enemies = []
    name = "Narrow Stairway"
    visited = False

    def on_enter(self) -> None:
        """
        Adds `Entrance` to the list of availible rooms if the player has the key and the treasure.
        Args
            None
        Returns
            None
        """
        super().on_enter()
        # Append `Entrance` to the rooms that can be visited if the player has the key and the treasure.
        if all(e in self.player.items for e in
               ["Key", "Treasure"]) and not Stairway.rooms.count(Entrance):
            Stairway.rooms.append(Entrance)

    def description(self) -> str:
        """
        Returns the description for the room. Returns a message saying that the path to `Entrance`
        is blocked the first time the player enters this room, and other messages depending on the
        items the player has in their inventory.
        Args
            None
        Returns
            str: the description.
        """
        if not Stairway.visited: # First visit
            return """You enter through the stairway as the doors suddenly shut and lock behind you.
You're trapped unless you find the key to the door!"""
        if all(e in self.player.items for e in ["Key", "Treasure"]): # Player has key and treasure
            return """You enter back into the narrow stairway with the keys and
the treasure. The door is open and you can head out!"""
        if "Key" in self.player.items: # Player needs key
            return """You enter back into the narrow stairway. The key that you
found fits, but you still haven't found the treasure!"""
        if "Treasure" in self.player.items: # Player needs treasure
            return """You enter back into the narrow stairway. You have the treasure,
but you just need a way to unlock the door!"""
        return "You enter back into the narrow stairway. The doors going outside are locked." # Player needs both

    def on_battle_finish(self) -> None:
        """
        Marks the room as visited.
        Args
            None
        Returns
            None
        """
        Stairway.visited = True


class Hall(Location):
    """Class for the main hall of the dungeon. When the rooms are randomly generated, this room will 
    serve as the root node for a tree that connects all the other rooms. The structure of the dungeon will
    be `Entrance` -> `Stairway` -> tree with `Hall` as its root node. For more information check `generateGraph()`.

    Attributes:
        rooms (list[Location]): the rooms that are adjacent to the current location. This list will contain `Stairway`
        but the rest of the contents will be randomized.
        enemies (list[Enemy]): the enemies present in a location. This list will be generated randomly.
        possible_enemies (list[Enemy]): the enemies that can appear in a room.
        name (str): the name of the location.
        visited (bool): True if the room as been visited else False.
    """
    rooms = []
    enemies = []
    possible_enemies = [enemy.Guard, enemy.Goblin]
    name = "Main Hall"
    visited = False

    def description(self) -> str:
        """
        Returns the description for the room.
        Args
            None
        Returns
            str: the description.
        """
        return "You enter through a grand hallway. It seems nearly endless."

    def on_battle_finish(self) -> None:
        """
        Marks the room as visited.
        Args
            None
        Returns
            None
        """
        Hall.visited = True


class WitchsHut(Location):
    """Room in the dungeon the represents a witch's hut. After the player clears all the enemies in the room,
    the player has the option to drink a potion that can increase or decrease the player's HP or ATK.

    Attributes:
        rooms (list[Location]): the rooms that are adjacent to the current location. This list will be generated randomly.
        enemies (list[Enemy]): the enemies present in a location. This list will be generated randomly.
        possible_enemies (list[Enemy]): the enemies that can appear in a room.
        name (str): the name of the location.
        visited (bool): True if the room as been visited else False.
    """
    rooms = []
    enemies = []
    possible_enemies = [enemy.Witch, enemy.Guard, enemy.Ghost]
    name = "Witch's Hut"
    visited = False

    def description(self) -> str:
        """
        Returns the description for the room.
        Args
            None
        Returns
            str: the description.
        """
        return "You find a room filled with potions containing mysterious liquids and bubbling cauldrons."

    def on_battle_finish(self) -> None:
        """
        Marks the room as visited. It also gives the player an option to drink a potion that 
        can increase or decrease the player's HP or ATK.
        Args
            None
        Returns
            None
        """
        if WitchsHut.visited:
            return
        WitchsHut.visited = True
        # Asks the user if they want to drink the potion.
        self.player.io.push("You find a glass containing a mysterious liquid.")
        choice = self.player.io.input("Do you want to drink it [Y/n]? ")
        # Check if the player wants to drink the potion, and return if not.
        if len(choice) == 0 or choice[0].lower() != "y":
            return
        if randint(0, 1): # Change HP if True
            change_val = randint(-10, 15) # Amount that your HP will change by.
            if change_val < 0: # HP goes down
                self.player.io.push(
                    f"Oh No! Your HP has decreased by {-change_val}")
            elif change_val > 0: # HP goes up
                self.player.io.push(
                    f"Your HP has increased by {change_val}!")
            else: # HP stays the same
                self.player.io.push("Nothing has happened...")

            # Update player HP.
            self.player.hp = min(max(0, self.player.hp + change_val), 80)
            
            # Redraw the screen because the player's HP may have changed.
            self.display()
            
            # Runs if the player dies from the potion.
            if self.player.hp == 0:
                self.player.io.push(f"Your HP has dropped to 0.\nGame Over")
                return
        else: # Change ATK if False
            change_val = randint(-1, 2) # Amount that your ATK will change by.
            if change_val < 0: # ATK goes down
                self.player.io.push(
                    f"Oh No! Your ATK has decreased by {-change_val}!")
            elif change_val > 0: # ATK goes up
                self.player.io.push(
                    f"Your ATK has increased by {change_val}!")
            else: # ATK stays the same
                self.player.io.push("Nothing has happened...")

            # Update player ATK.
            self.player.atk = max(0, self.player.atk + change_val)

            # Redraw the screen because the player's ATK may have changed.
            self.display()


class Armoury(Location):
    """Room in the dungeon the represents an armoury. After the player has finished clearing all
    the enemies, the player's ATK will be increased by 2.

    Attributes:
        rooms (list[Location]): the rooms that are adjacent to the current location. This list will be generated randomly.
        enemies (list[Enemy]): the enemies present in a location. This list will be generated randomly.
        possible_enemies (list[Enemy]): the enemies that can appear in a room.
        name (str): the name of the location.
        visited (bool): True if the room as been visited else False.
    """
    name = "Armoury"
    enemies = []
    possible_enemies = [enemy.Guard, enemy.Ogre]
    rooms = []
    visited = False

    def description(self) -> str:
        """
        Returns the description for the room.
        Args
            None
        Returns
            str: the description.
        """
        return "You find a room filled with weapons and armour."

    def on_battle_finish(self) -> None:
        """
        Marks the room as visited. It also increases the player's ATK by 2.
        Args
            None
        Returns
            None
        """
        if Armoury.visited:
            return
        Armoury.visited = True
        self.player.io.push("You find a new sword!") # Sends message.
        self.player.io.push("Your ATK has increased by 2.")
        self.player.atk += 2 # Update player ATK.
        self.display() # Redraw screen with new stats.


class Prison(Location):
    """Room in the dungeon the represents a prison. The player will find the key that is needed to unlock the door here.

    Attributes:
        rooms (list[Location]): the rooms that are adjacent to the current location. This list will be generated randomly.
        enemies (list[Enemy]): the enemies present in a location. This list will be generated randomly.
        possible_enemies (list[Enemy]): the enemies that can appear in a room.
        name (str): the name of the location.
        visited (bool): True if the room as been visited else False.
    """
    name = "Prison"
    enemies = []
    possible_enemies = [enemy.Guard, enemy.Ghost, enemy.Ogre]
    rooms = []
    visited = False

    def description(self) -> str:
        """
        Returns the description for the room.
        Args
            None
        Returns
            str: the description.
        """
        return "You enter a large room containing rows of prison cells."

    def on_battle_finish(self) -> None:
        """
        Marks the room as visited. It also add the key to the player's inventory if it isn't already there.
        Args
            None
        Returns
            None
        """
        if Prison.visited:
            return
        Prison.visited = True
        self.player.io.push( # Send message.
            "You found a key lying on the ground! Will this open the front door?"
        )
        self.player.items.append("Key") # Add key to inventory.
        self.display() # Redraw screen with new info.


class Hatchery(Location):
    """Room in the dungeon the represents a hatchery with a dragon egg. This room doesn't really do anything
    other than hint that the player will fight a dragon later on.

    Attributes:
        rooms (list[Location]): the rooms that are adjacent to the current location. This list will be generated randomly.
        enemies (list[Enemy]): the enemies present in a location. This list will be generated randomly.
        possible_enemies (list[Enemy]): the enemies that can appear in a room.
        name (str): the name of the location.
        visited (bool): True if the room as been visited else False.
    """
    rooms = []
    enemies = [enemy.DragonHatchling, enemy.Guard, enemy.Guard]
    possible_enemies = []
    name = "Hatchery"
    visited = False

    def description(self) -> str:
        """
        Returns the description for the room.
        Args
            None
        Returns
            str: the description.
        """
        return "You have found a small, heavily guarded room with one single egg in the middle."

    def on_battle_finish(self) -> None:
        """
        Marks the room as visited.
        Args
            None
        Returns
            None
        """
        Hatchery.visited = True


class Hospital(Location):
    """Room in the dungeon the represents a hospital. This room heals the player by 20 HP after the player
    clears all the enemies.

    Attributes:
        rooms (list[Location]): the rooms that are adjacent to the current location. This list will be generated randomly.
        enemies (list[Enemy]): the enemies present in a location. This list will be generated randomly.
        possible_enemies (list[Enemy]): the enemies that can appear in a room.
        name (str): the name of the location.
        visited (bool): True if the room as been visited else False.
    """
    name = "Hospital"
    enemies = []
    possible_enemies = [enemy.Guard, enemy.Ghost, enemy.Goblin, enemy.Witch]
    rooms = []
    visited = False

    def description(self) -> str:
        """
        Returns the description for the room.
        Args
            None
        Returns
            str: the description.
        """
        return "You enter a room that contains a couple beds. There are medical supplies scattered throughout."

    def on_battle_finish(self) -> None:
        """
        Marks the room as visited. It also increases the player's HP by 20.
        Args
            None
        Returns
            None
        """
        if Hospital.visited:
            return
        Hospital.visited = True
        self.player.io.push( # Send message
            "You find some bandages lying around and cover up your wounds.")
        self.player.io.push(f"Your HP has increased by 20!")
        self.player.hp = min(self.player.hp + 20, 80) # Update player HP, make sure that it is capped at 80.
        self.display() # Redraw screen because of new stats.


class TreasureRoom(Location):
    """Room in the dungeon the represents a prison. The player will find the treasure here.

    Attributes:
        rooms (list[Location]): the rooms that are adjacent to the current location. This list will be generated randomly.
        enemies (list[Enemy]): the enemies present in a location. This list will be generated randomly.
        possible_enemies (list[Enemy]): the enemies that can appear in a room.
        name (str): the name of the location.
        visited (bool): True if the room as been visited else False.
    """
    rooms = []
    enemies = []
    possible_enemies = [enemy.Guard, enemy.Goblin, enemy.Ogre]
    name = "Treasure Room"
    visited = False

    def description(self) -> str:
        """
        Returns the description for the room. States that you have found the treasure the first time 
        that you visit this room, otherwise states that you have already collected all the treasure.
        Args
            None
        Returns
            str: the description.
        """
        if not TreasureRoom.visited:
            return "You enter a room filled with gold. You have found the room containing the treasure in the dungeon!"
        return "You enter the treasure room that you have already collected."

    def on_battle_finish(self) -> None:
        """
        Marks the room as visited. It also add the treasure to the player's inventory if it isn't already there.
        Args
            None
        Returns
            None
        """
        if TreasureRoom.visited:
            return
        TreasureRoom.visited = True
        self.player.io.push("You picked up all the treasure in the room.") # Send message
        self.player.items.append("Treasure") # Update inventory
        self.display() # Redraw screen with new info


def generate_enemies(difficulty: int) -> None:
    """
    Randomly generate enemies to put into each room of the dungeon.
    Args
        difficulty (int): number of enemies is based on difficulty.
    Returns
        None
    """
    # Go through all Locations.
    for room in Location.__subclasses__():
        # If there are no possible enemies, we don't need to add any enemies to the room.
        if len(room.possible_enemies) == 0:
            continue
        
        # Until the sum of the difficulty of the enemies in a room is greater than 
        # `difficulty`, add a random enemy into the room
        room_diff = 0 # Sum of difficulties in the room.
        while room_diff < difficulty and len(room.enemies) < 4:
            e = choice(room.possible_enemies)
            room_diff += e().difficulty
            room.enemies.append(e)


def generate_graph() -> None:
    """
    Connects all the rooms in the dungeon randomly. 
    Args
        None
    Returns
        None
    """
    # Connect `Entrance`, `Stairway`, and `Hall`.
    Entrance.rooms.append(Stairway) 
    # We don't want to connect `Entrance` and `Stairway` because the player can't re-enter
    # the entrance until they find the key and the treasure.
    Stairway.rooms.append(Hall)
    Hall.rooms.append(Stairway)

    # Gets a list of all rooms that connect randomly. These are all the rooms that inherit from `Location`.
    other_rooms = list(filter(lambda l : l not in [Entrance, Stairway], Location.__subclasses__()))

    # Uses a randomly generated Prufer sequence generate a tree of all the rooms.
    # Source: https://www.geeksforgeeks.org/random-tree-generator-using-prufer-sequence-with-examples/
    # In the following code, each room is represented by an integer, corresponding to the index of the room's
    # occurence in `other_rooms`

    # number of rooms.
    n = len(other_rooms)

    # Generate Prufer sequence.
    prufer = [randint(0, n - 1) for i in range(n - 2)]

    # Number of occurences of each room.
    vertex_set = [prufer.count(i) for i in range(n)]

    # List of all the edges in the graph.
    edges = []
    
    # Add the first n - 2 edges.
    for i in range(n - 2): # Iterate through each room
        for j in range(n): # Find a that doesn't appear in `prufer`
            if vertex_set[j] == 0:
                vertex_set[j] = -1
                edges.append((j, prufer[i])) # Add the edge
                vertex_set[prufer[i]] -= 1
                break

    # Add the final edge.
    j = 0
    for i in range(n):
        # Find the two rooms that are remaining and connect them.
        if vertex_set[i] == 0 and j == 0:
            nl = i
            j += 1
        elif vertex_set[i] == 0 and j == 1:
            nr = i
    edges.append((nl, nr))

    # Connect the rooms in the graph.
    for edge in edges:
        other_rooms[edge[0]].rooms.append(other_rooms[edge[1]])
        other_rooms[edge[1]].rooms.append(other_rooms[edge[0]])
