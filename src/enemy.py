"""
ICS3U
Paul Chen
This file holds the `Enemy` class as well as a list of classes that inherit from it.
It holds all the code for the enemies that the player will have to fight.
"""

from random import randint


class Enemy:
    """Class that represents an enemy. This is the parent class of other enemy classes.

    Attributes:
        name (str): the name of the enemy.
        hp (int): the amount of HP that an enemy has.
        atk (int): the amount of ATK that an enemy has.
        num_hits (tuple[int, int]): range of the number of hits that an enemy can hit on each turn.
        difficulty (int): the difficulty of each enemy. Used to calculate the enemies in each room and 
            the length of the sequence that the user has to type.
    """
    name = ""

    def __init__(self, hp: int, atk: int, num_hits: tuple):
        """
        Inits enemy class.
        Args
            hp (int): the amount of HP that an enemy has.
            atk (int): the amount of ATK that an enemy has.
            num_hits (tuple[int, int]): the range of the number of hits that an enemy can hit on each turn.
            difficulty (int): the difficulty of each enemy. This should be a number between 1 and 5 and it
                is used as the length of the random sequence the player has to type and is also used when
                randomly generating the enemies located in each room.
        """
        self.hp = hp
        self.atk = atk
        self.num_hits = num_hits
        self.difficulty = max(1, min(
            5, int((hp + atk * (num_hits[0] + num_hits[1])) // 15))) # Calculates the difficulty of each enemy.

    def attack(self) -> int:
        """
        Calculates the number of hits that an enemy makes. Number of
        hits is based to a random number with in the range of `num_hits`.
        Args
            None
        Returns
            int: number of hits.
        """
        return randint(self.num_hits[0], self.num_hits[1])


# The following lines of code are a list of classes of all the enemies present in the game.


class Guard(Enemy):
    """Class that represents a guard. This enemy is a normal enemy that isn't too special. Inherits from `Enemy`."""
    name = "Guard"

    def __init__(self):
        super().__init__(24, 5, (1, 3))


class Goblin(Enemy):
    """Class that represents a goblin. This enemy has low HP but high damage. Inherits from `Enemy`."""
    name = "Goblin"

    def __init__(self):
        super().__init__(20, 4, (3, 5))


class Ogre(Enemy):
    """Class that represents an ogre. This enemy has high HP and high damage. Inherits from `Enemy`."""
    name = "Ogre"

    def __init__(self):
        super().__init__(40, 10, (1, 2))


class Witch(Enemy):
    """Class that represents a witch. This enemy has medium HP and medium damage. Inherits from `Enemy`."""
    name = "Witch"

    def __init__(self):
        super().__init__(30, 5, (2, 3))


class Ghost(Enemy):
    """Class that represents a ghost. This enemy has low HP and low damage. Inherits from `Enemy`."""
    name = "Ghost"

    def __init__(self):
        super().__init__(5, 5, (1, 1))


class DragonHatchling(Enemy):
    """Class that represents a dragon hatchling. This enemy has medium HP and medium damage. Inherits from `Enemy`."""
    name = "Dragon Hatchling"

    def __init__(self):
        super().__init__(30, 5, (2, 4))


class Dragon(Enemy):
    """Class that represents a dragon. This enemy has high HP and high damage 
    and is the final boss of the game. Inherits from `Enemy`."""
    name = "Dragon"

    def __init__(self):
        super().__init__(75, 6, (2, 3))
