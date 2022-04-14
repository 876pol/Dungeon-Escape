"""
ICS3U
Paul Chen
This file holds the `Interface` class, which helps to make IO neater.
"""

from os import name, system
from pytimedinput import timedInput
from time import time
from sys import stdout


class Interface:
    """Class that deals with IO. The terminal is seperated into two parts: one showing general information
    and another showing the list of events. I wanted both these components to always show on screen, so it 
    only shows the last ten events that have occurred so that the description doesn't scroll off screen. 
    The event history is implemented as a stack where you can push and pop messages to the stacks.

    Attributes:
        room_info (str): the description of the current room. Shows a description of the room, player stats, and a list of enemies in the room.
        history (list[str]): message list.
        nl (int): the number of newlines that are currently being shown in the event history.
        default_ignore (int): the number of seconds to pause after every event.
        lines (int): the number of events to show on screen at a time.
    """
    def __init__(self):
        """
        Inits interface class.
        Args
            None
        """
        self.clear()
        self.room_info = ""
        self.history = []
        self.nl = 0
        self.default_ignore = 0.2
        self.lines = 10

    def set_room_info(self, info) -> None:
        """
        Updates the information about the current room and player and redraws the screen.
        Args
            info (str): the new description.
        Returns
            None
        """
        self.room_info = info
        self.display()

    def push(self, message, delay=True) -> None:
        """
        Pushes an event into the message stack and redraws the event history.
        Args
            info (str): message to add.
            delay (bool): True if we add a pause before showing a message else False.
        Returns
            None
        """
        if delay:
            self.ignore(self.default_ignore)
        for line in message.split("\n"):
            self.history.append(line)
        self.update()

    def pop(self):
        """
        Removes the most recent element added to the stack.
        Args
            None
        Returns
            None
        """
        self.history.pop()
        self.update()

    def input(self, message, delay=True) -> str:
        """
        Takes in input, pushes said info into the message stack, and redraws the event history.
        Args
            info (str): the input query.
            delay (bool): True if we add a pause before showing a message else False.
        Returns
            str: return value of `input()`
        """
        # Delays and ignores input.
        if delay:
            self.ignore(self.default_ignore)

        # Takes in input.
        inp = input(message)
        if delay:
            stdout.write("\033[F")
            stdout.write("\033[K")

        # Inserts the message and input into the message stack.
        self.push(message + inp, delay=delay)
        return inp

    def timed_input(self, tm, delay=True) -> tuple:
        """
        Takes in input with a timeout, pushes said info into the message stack, 
        and redraws the event history. The input stops if the timeout elapses.
        Args
            tm (int): length of timeout in seconds.
            delay (bool): True if we add a pause before showing a message else False.
        Returns
            tuple[str, int]: the string taken in through `input()` and a boolean 
            that represents whether the input timed out or not.
        """
        # Delays and ignores input.
        if delay:
            self.ignore(self.default_ignore)

        # Takes in timed input.
        inp = timedInput(timeout=tm, resetOnInput=False)
        self.push(inp[0], delay=delay)
        stdout.write("\033[F")
        stdout.write("\033[K")

        # Updates screen.
        self.update()
        return inp

    def ignore(self, tm) -> None:
        """
        Pauses the program for a certain amount of time and ignores all user input. This function 
        is used to prevent the user from accidentally typing after the battle timed out.
        Args
            tm (int): length of timeout in seconds.
        Returns
            None
        """
        # Keeps looping until the timeout elapses.
        start = time()
        while time() - start < tm:
            timedInput(timeout=float(tm) - (time() - start),
                       resetOnInput=False)
            # If the user types anything during this time, erase it and redraw the screen.
            stdout.write("\033[F")
            stdout.write("\033[K")
            self.update()

    def clear(self) -> None:
        """
        Clears the screen.
        Args
            None
        Returns
            None
        """
        if name == "posix":
            system("clear")
        else:
            system("cls")

    def display(self):
        """
        Fully redraws the screen.
        Args
            None
        Returns
            None
        """
        # Clears screen.
        self.clear()

        # Prints room_info.
        print(self.room_info)

        # Prints seperator.
        print("_" * 50 + "\n")

        # Prints the required number of lines and stores the number of lines in `nl`.
        self.nl = len(self.history) - max(len(self.history) - self.lines, 0)
        print("\n".join(self.history[-self.nl:]))

    def update(self):
        """
        Redraws the event list.
        Args
            None
        Returns
            None
        """
        # Clears the message history.
        for i in range(self.nl):
            stdout.write("\033[F")
            stdout.write("\033[K")

        # Prints the required number of lines and stores the number of lines in `nl`.
        self.nl = len(self.history) - max(len(self.history) - self.lines, 0)
        print("\n".join(self.history[-self.nl:]))
