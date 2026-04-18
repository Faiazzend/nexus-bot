import pyautogui
import pygetwindow as gw
import time
import os

TARGET_WINDOW_TITLE = 'Poke Nexus'

def show_coords():
    print("--- Mouse Coordinate Tracker ---")
    print("Move your mouse to the desired spot in the game.")
    print("Press Ctrl+C to exit.\n")

    try:
        while True:
            # Get global mouse position
            x, y = pyautogui.position()
            
            # Try to get game window position
            try:
                win = gw.getWindowsWithTitle(TARGET_WINDOW_TITLE)[0]
                # Calculate coordinates relative to the TOP-LEFT of the game window
                rel_x = x - win.left
                rel_y = y - win.top
                
                window_data = f" | Relative to Game: ({rel_x}, {rel_y})"
            except:
                window_data = " | [!] Game window not found"

            # Print coordinates on a single line that updates
            print(f"Global: ({x}, {y}){window_data}      ", end="\r")
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nTracker stopped.")

if __name__ == "__main__":
    show_coords()