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

# KEEPING YOUR PERFECT TIMING
BASE_HOLD = 0.08   
BASE_DELAY = 0.07           

# UPDATED GRID SETTINGS (4x3)
GRID_WIDTH = 4  
GRID_HEIGHT = 3 
TARGET_WINDOW_TITLE = 'Poke Nexus'
# =================================================

def setup_game_window():
    print(f"[*] Searching for '{TARGET_WINDOW_TITLE}'...")
    try:
        win = gw.getWindowsWithTitle(TARGET_WINDOW_TITLE)[0]
        win.restore()
        win.activate()
        win.moveTo(-7, 0)
        win.resizeTo(1024, 768)
        time.sleep(1.5)
        pyautogui.click(win.left + 512, win.top + 384)
        return win
    except Exception as e:
        print(f"[!] Error: {e}")
        return None

def is_in_battle(win):
    """High-Frequency Template Matching"""
    try:
        left, top = win.left + 350, win.top + 470
        right, bottom = win.left + 500, win.top + 580
        
        cap = ImageGrab.grab(bbox=(left, top, right, bottom))
        screen_bgr = cv2.cvtColor(np.array(cap), cv2.COLOR_RGB2BGR)
        screen_gray = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)
        
        cv2.imwrite("last_scan.png", screen_bgr)

        template = cv2.imread(TEMPLATE_FILE, 0)
        if template is None: return False

        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        print(f"[*] Scan Match: {max_val*100:.1f}%", end="\r")
        return max_val > 0.75
    except:
        return False

def combat_sequence():
    # Using your current working logic (place your custom 4s fix here if needed)
    print("\n>>> BATTLE DETECTED")
    time.sleep(random.uniform(0.3, 0.5))      
    pyautogui.press('1') 
    time.sleep(random.uniform(0.2, 0.3))      
    pyautogui.press('1') 
    time.sleep(4.0)      

def start_bot():
    win = setup_game_window()
    if not win: return

    print(f"[*] BOT ACTIVE. Boundary: 4x3 units. Origin: Top-Left.")
    
    # Starting at (0,0) - Top Left
    pos_x, pos_y = 0, 0
    last_move = None  
    
    try:
        while True:
            # --- 1. RELEASE & SCAN ---
            if last_move:
                pyautogui.keyUp(last_move)
                time.sleep(0.02) 
            
            if is_in_battle(win):
                combat_sequence()
                last_move = None 
                continue

            # --- 2. 4x3 DIRECTION LOGIC ---
            possible_moves = []
            if pos_y > 0: possible_moves.append('w')                   # Up
            if pos_y < (GRID_HEIGHT - 1): possible_moves.append('s')   # Down (Max 2)
            if pos_x > 0: possible_moves.append('a')                   # Left
            if pos_x < (GRID_WIDTH - 1): possible_moves.append('d')    # Right (Max 3)

            current_move = random.choice(possible_moves)
            
            # Update internal tracking
            if current_move == 'w': pos_y -= 1
            elif current_move == 's': pos_y += 1
            elif current_move == 'a': pos_x -= 1
            elif current_move == 'd': pos_x += 1

            # --- 3. EXECUTION (Using your perfect 0.15s settings) ---
            rand_hold = random.uniform(BASE_HOLD - 0.01, BASE_HOLD + 0.01)
            rand_delay = random.uniform(BASE_DELAY - 0.01, BASE_DELAY + 0.01)

            pyautogui.keyDown(current_move)
            time.sleep(rand_hold)
            last_move = current_move
            time.sleep(rand_delay)
            
            print(f"Grid Position: ({pos_x}, {pos_y})", end="\r")

    except KeyboardInterrupt:
        if last_move: pyautogui.keyUp(last_move)
        print("\n[!] Bot stopped.")

if __name__ == "__main__":
    start_bot()