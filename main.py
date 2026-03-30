from window_manager import setup_game_window
from bot_logic import PokeBot
import threading

def on_start():
    # 1. Prepare the game window
    success = setup_game_window()
    
    if success:
        # 2. If window is ready, start the bot logic
        global bot
        bot = PokeBot(width=3, height=4) 
        thread = threading.Thread(target=bot.start_loop, daemon=True)
        thread.start()
    else:
        print("Bot failed to start: Window not ready.")