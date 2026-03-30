import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import time
import random

# ================= CONFIGURATION =================
TEMPLATE_FILE = 'fight_template.png'
pyautogui.PAUSE = 0.0       

# YOUR PERFECT MOVEMENT TIMING
BASE_HOLD = 0.08   
BASE_DELAY = 0.07           

# GRID BOUNDARIES (4 columns x 3 rows)
GRID_WIDTH = 4  
GRID_HEIGHT = 3 
TARGET_WINDOW_TITLE = 'Poke Nexus'
# =================================================

class PokeBot:
    def __init__(self, win):
        self.win = win
        # Start at Top-Left (0,0)
        self.curr_x = 0
        self.curr_y = 0
        self.last_move = None

    def is_in_battle(self):
        """High-Frequency Template Matching"""
        try:
            left, top = self.win.left + 350, self.win.top + 470
            right, bottom = self.win.left + 500, self.win.top + 580
            
            cap = ImageGrab.grab(bbox=(left, top, right, bottom))
            screen_gray = cv2.cvtColor(np.array(cap), cv2.COLOR_RGB2GRAY)
            
            template = cv2.imread(TEMPLATE_FILE, 0)
            if template is None: return False

            res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)

            print(f"[*] Scan Match: {max_val*100:.1f}% | Tile: ({self.curr_x}, {self.curr_y})", end="\r")
            return max_val > 0.75
        except:
            return False

    def combat_sequence(self):
        print("\n>>> BATTLE DETECTED - Locking Coordinates")
        # Perform your custom combat logic here
        time.sleep(random.uniform(0.3, 0.5))      
        pyautogui.press('1') 
        time.sleep(random.uniform(0.2, 0.3))      
        pyautogui.press('1') 
        time.sleep(4.0) 
        print(">>> Battle Finished. Resuming from last known tile.")

    def move(self):
        # 1. Release previous key and let screen settle
        if self.last_move:
            pyautogui.keyUp(self.last_move)
            time.sleep(0.02)

        # 2. Check for battle BEFORE deciding next move
        if self.is_in_battle():
            self.combat_sequence()
            self.last_move = None
            return

        # 3. Calculate valid moves based on 4x3 boundary
        possible_moves = []
        if self.curr_y > 0: possible_moves.append(('w', 0, -1))                   # Up
        if self.curr_y < (GRID_HEIGHT - 1): possible_moves.append(('s', 0, 1))   # Down
        if self.curr_x > 0: possible_moves.append(('a', -1, 0))                   # Left
        if self.curr_x < (GRID_WIDTH - 1): possible_moves.append(('d', 1, 0))    # Right

        if not possible_moves: return

        # 4. Execute Movement
        direction, dx, dy = random.choice(possible_moves)
        
        rand_hold = random.uniform(BASE_HOLD - 0.01, BASE_HOLD + 0.01)
        rand_delay = random.uniform(BASE_DELAY - 0.01, BASE_DELAY + 0.01)

        pyautogui.keyDown(direction)
        time.sleep(rand_hold)
        
        # 5. Update Memory ONLY after the key press is initiated
        self.last_move = direction
        self.curr_x += dx
        self.curr_y += dy

        time.sleep(rand_delay)

def setup_game_window():
    print(f"[*] Searching for '{TARGET_WINDOW_TITLE}'...")
    try:
        win = gw.getWindowsWithTitle(TARGET_WINDOW_TITLE)[0]
        win.restore()
        win.activate()
        win.moveTo(-7, 0)
        win.resizeTo(1024, 768)
        time.sleep(1.0)
        pyautogui.click(win.left + 512, win.top + 384)
        return win
    except Exception as e:
        print(f"[!] Error: {e}")
        return None

if __name__ == "__main__":
    window = setup_game_window()
    if window:
        bot = PokeBot(window)
        print("[*] BOT RUNNING. Starting at Top-Left (0,0).")
        try:
            while True:
                bot.move()
        except KeyboardInterrupt:
            if bot.last_move: pyautogui.keyUp(bot.last_move)
            print("\n[!] Bot stopped.")