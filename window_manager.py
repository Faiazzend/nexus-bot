import pygetwindow as gw
import time
import pyautogui

def setup_game_window():
    # Look for the window by title (Case sensitive)
    try:
        win = gw.getWindowsWithTitle('Poke Nexus')[0]
        
        # Bring to front and focus
        win.activate()
        win.restore() # In case it's minimized
        
        # Move to top-left and resize
        win.moveTo(0, 0)
        win.resizeTo(1024, 768)
        
        time.sleep(1) # Wait for resize to "settle"
        
        # Click the center of the window to ensure it's the active input
        pyautogui.click(512, 384)
        print("Game window found, resized, and focused.")
        return True
    except IndexError:
        print("Error: Poke Nexus window not found. Is the game running?")
        return False