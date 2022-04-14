"""
ICS3U
Paul Chen
This file holds the code for the `Player` class, which contains all the information about the player.
"""

from interface import Interface
from random import randint
from time import time


class Player:
    """Class that represents the player and their stats.

    Attributes:
        hp (int): the player's remaining HP.
        atk (int): the player's ATK.
        tl (int): the time limit for the battle.
        difficulty (int): a number representing the player's chosen difficulty.
        items (int): the player's items.
        io (Interface): the class that deals with io.
    """
    def __init__(self, diff):
        """
        Inits location class.
        Args
            diff (int): the difficulty chosen by the player. It is a number from 1 to 3.
        """
        self.hp = 80
        self.atk = 6
        self.tl = 9 - diff
        self.difficulty = diff * 4
        self.items = []
        self.io = Interface()

    def attack(self, seq_len: int) -> int:
        """
        Allows the player to attack and returns the number of hits that the players has landed.
        Args
            seq_len (int): the length of the random sequence.
        Returns
            int: the number of hits that the player has landed.
        """
        self.io.input("It's your turn, type anything to begin! ")
        self.io.push("Type the letters that appear on screen: ")

        # Lambda function that generates a random string of characters that has a length of `seq_len`.
        generate_string = lambda : "".join(chr(97 + randint(0, 25)) for i in range(seq_len))

        hits = 0 # number of hits.
        start_time = time() # start time

        # Keeps looping until the time elapses.
        while time() - start_time < self.tl:
            # Generate and display the string.
            given_str = generate_string()
            self.io.push(given_str, delay=False)

            # Get the user's input.
            user_str = self.io.timed_input(self.tl - (time() - start_time),
                                           delay=False)

            # Check if the user's input is the same as the one displayed.
            if user_str[0] == given_str:
                hits += 1

            # Erase the lines.
            self.io.pop()
            self.io.pop()
        self.io.pop()
        self.io.pop()
        return hits

    def __bool__(self):
        """
        Checks if the game is still ongoing or not.
        Args
            None
        Returns
            bool: True if the game is still ongoing else False.
        """
        return bool(self.hp)
