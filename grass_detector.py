import pygetwindow as gw
import cv2
import numpy as np
from PIL import ImageGrab

# ================= CONFIGURATION =================
TARGET_WINDOW_TITLE = 'Poke Nexus'
NORTH_TEMPLATE = 'north.png'
MIDDLE_TEMPLATE = 'middle.png'
THRESHOLD = 0.60 

# (Left, Top, Right, Bottom, Key_To_Press, Name)
LOCATIONS = [
    (566, 420, 584, 443, 'd', "East"),
    (567, 356, 584, 374, 'wd', "North East"),
    (440, 357, 456, 376, 'wa', "North West"),
    (440, 484, 455, 504, 'sa', "South West"),
    (506, 486, 521, 504, 's', "South"),
    (567, 486, 584, 506, 'sd', "South East"),
    (487, 326, 537, 347, 'w', "North") 
]
# =================================================

class GrassScanner:
    def __init__(self):
        self.tpl_north = cv2.imread(NORTH_TEMPLATE, 0)
        self.tpl_middle = cv2.imread(MIDDLE_TEMPLATE, 0)
        
        if self.tpl_north is None or self.tpl_middle is None:
            print("[!] Grass templates not found!")

    def get_available_grass(self, win):
        """
        Scans all locations and returns a list of keys 
        where grass is currently detected.
        """
        found_grass_keys = []
        
        if not win:
            return found_grass_keys

        for (x1, y1, x2, y2, key, name) in LOCATIONS:
            try:
                # 1. Determine template
                current_tpl = self.tpl_north if name == "North" else self.tpl_middle
                
                # 2. Grab Region
                bbox = (win.left + x1, win.top + y1, win.left + x2, win.top + y2)
                cap = ImageGrab.grab(bbox=bbox)
                screenshot = cv2.cvtColor(np.array(cap), cv2.COLOR_RGB2GRAY)

                # 3. Match
                res = cv2.matchTemplate(screenshot, current_tpl, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)

                # 4. Add to list if above threshold
                if max_val > THRESHOLD:
                    found_grass_keys.append(key)
            except Exception as e:
                continue
                
        return found_grass_keys

# Optional: keep the test logic if run directly
if __name__ == "__main__":
    import time
    scanner = GrassScanner()
    try:
        win = gw.getWindowsWithTitle(TARGET_WINDOW_TITLE)[0]
        while True:
            grass = scanner.get_available_grass(win)
            print(f"Grass found at: {grass}")
            time.sleep(1)
    except IndexError:
        print("Window not found.")