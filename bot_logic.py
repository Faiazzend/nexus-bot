import pyautogui
import time
import random

class PokeBot:
    def __init__(self, width, height):
        self.w_limit = width * 65
        self.h_limit = height * 65
        self.curr_x = 0
        self.curr_y = 0
        self.is_running = False

    def random_move(self):
        # Pick a random direction
        move = random.choice([('w', 0, -1), ('s', 0, 1), ('a', -1, 0), ('d', 1, 0)])
        key, dx, dy = move

        # Boundary Check: Ensure we stay in the 3x4 area
        new_x = self.curr_x + (dx * 65)
        new_y = self.curr_y + (dy * 65)

        if 0 <= new_x <= self.w_limit and 0 <= new_y <= self.h_limit:
            # Perform the move
            pyautogui.keyDown(key)
            time.sleep(random.uniform(0.15, 0.25)) # Human-like key press duration
            pyautogui.keyUp(key)
            
            self.curr_x = new_x
            self.curr_y = new_y
            
            # Random "human" pause between steps
            time.sleep(random.uniform(0.4, 0.9))
        else:
            # If we hit a boundary, just wait a second (looks like thinking)
            time.sleep(0.3)