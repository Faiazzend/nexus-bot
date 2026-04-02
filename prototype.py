import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import time
import random

# ================= CONFIGURATION =================
TEMPLATE_FILE = 'fight_template.png'
ENCOUNTER_TEMPLATE = 'encounter_start.png' 

pyautogui.PAUSE = 0.0       

# MOVEMENT TIMING
BASE_HOLD = 0.15   
BASE_DELAY = 0.05 

# GRID BOUNDARIES
GRID_WIDTH = 5
GRID_HEIGHT = 1
TARGET_WINDOW_TITLE = 'Poke Nexus'

# COORDINATE BOX FOR ENCOUNTER DETECTION
OCR_BOX = (630, 134, 670, 170)
# =================================================

class PokeBot:
    def __init__(self, win):
        self.win = win
        self.last_direction = None 
        self.curr_x = 0  
        self.curr_y = 0
        
        self.fight_tpl = cv2.imread(TEMPLATE_FILE, 0)
        self.enc_tpl = cv2.imread(ENCOUNTER_TEMPLATE, 0)

    def stop_moving(self):
        if self.last_direction:
            pyautogui.keyUp(self.last_direction)
            self.last_direction = None

    def check_for_encounter(self):
        try:
            bbox = (self.win.left + OCR_BOX[0], self.win.top + OCR_BOX[1], 
                    self.win.left + OCR_BOX[2], self.win.top + OCR_BOX[3])
            cap = ImageGrab.grab(bbox=bbox)
            gray_frame = cv2.cvtColor(np.array(cap), cv2.COLOR_RGB2GRAY)

            if self.enc_tpl is not None:
                res = cv2.matchTemplate(gray_frame, self.enc_tpl, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                return max_val > 0.85 
            return False
        except:
            return False

    def wait_for_fight_menu(self):
        self.stop_moving()
        print("\n[!] Encounter detected! Confirming menu...")
        for _ in range(12):
            time.sleep(0.5) 
            try:
                cap = ImageGrab.grab(bbox=(self.win.left + 200, self.win.top + 200, 
                                           self.win.left + 800, self.win.top + 650))
                gray_fight = cv2.cvtColor(np.array(cap), cv2.COLOR_RGB2GRAY)
                if self.fight_tpl is not None:
                    res = cv2.matchTemplate(gray_fight, self.fight_tpl, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(res)
                    if max_val > 0.75:
                        return True
            except:
                continue
        return False

    def combat_sequence(self):
        print(">>> COMBAT SEQUENCE")
        time.sleep(random.uniform(0.1, 0.2))
        pyautogui.press('1') 
        time.sleep(random.uniform(0.4, 0.6))
        pyautogui.press('1') 
        time.sleep(4.5) 
        print(">>> Battle ended. Resuming...")

    def move(self):
        valid_keys = []
        if self.curr_y > 0: valid_keys.append(('w', 0, -1))
        if self.curr_y < (GRID_HEIGHT - 1): valid_keys.append(('s', 0, 1))
        if self.curr_x > 0: valid_keys.append(('a', -1, 0))
        if self.curr_x < (GRID_WIDTH - 1): valid_keys.append(('d', 1, 0))

        if not valid_keys: return
        new_direction, dx, dy = random.choice(valid_keys)

        # Update coordinates BEFORE movement to represent where we are GOING
        self.curr_x += dx
        self.curr_y += dy

        if new_direction != self.last_direction:
            self.stop_moving()
            pyautogui.keyDown(new_direction)
            self.last_direction = new_direction
        
        time.sleep(BASE_HOLD + random.uniform(-0.005, 0.005))

        # Check for encounter
        if self.check_for_encounter():
            # DESYNC CORRECTION: 
            # We already updated the coords. Since a battle happened, 
            # the game "ate" the move or triggered it on this tile.
            # We subtract the move back to stay on the previous grid logic.
            self.curr_x -= dx
            self.curr_y -= dy
            
            self.stop_moving()
            if self.wait_for_fight_menu():
                self.combat_sequence()
        else:
            print(f"[*] Tile: ({self.curr_x}, {self.curr_y}) | Key: {new_direction} ", end="\r")
            time.sleep(BASE_DELAY)

def setup_game_window():
    try:
        win = gw.getWindowsWithTitle(TARGET_WINDOW_TITLE)[0]
        win.restore(); win.activate()
        win.moveTo(-7, 0); win.resizeTo(1024, 768)
        time.sleep(1.0)
        pyautogui.click(win.left + 512, win.top + 384)
        return win
    except Exception as e:
        print(f"[!] Window Error: {e}"); return None

if __name__ == "__main__":
    window = setup_game_window()
    if window:
        bot = PokeBot(window)
        try:
            while True:
                bot.move()
        except KeyboardInterrupt:
            bot.stop_moving()
            print("\n[!] Bot stopped.")