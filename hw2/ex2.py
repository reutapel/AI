import time
import random

ids = ["201316346", "201110376"]
# aTeam
class Controller:
    "This class is a controller for a Bomberman game."
    
    def __init__(self, board, steps):
        """Initialize controller for given game board and number of steps.
        This method MUST terminate within the specified timeout."""
        self.BMx = None
        self.BMy = None
        self.N = len(board)
        self.M = len(board[1])
        self.steps = steps

    
    def choose_next_move(self, board, n, reward):
        "Choose next action for Bomberman given the current state of the board."
        
