import customtkinter as ctk

class BotGUI(ctk.CTk):
    def __init__(self, start_callback, stop_callback):
        super().__init__()
        self.title("Poke-Nexus Bot")
        self.geometry("350x500")

        # UI elements: Width/Height Entries
        self.w_entry = ctk.CTkEntry(self, placeholder_text="Width")
        self.w_entry.pack(pady=10)
        self.h_entry = ctk.CTkEntry(self, placeholder_text="Height")
        self.h_entry.pack(pady=10)

        # Buttons
        self.draw_btn = ctk.CTkButton(self, text="Draw an Area", command=self.draw_area)
        self.draw_btn.pack(pady=10)
        
        self.start_btn = ctk.CTkButton(self, text="Start", command=start_callback)
        self.start_btn.pack(pady=10)

        self.stop_btn = ctk.CTkButton(self, text="Stop", command=stop_callback)
        self.stop_btn.pack(pady=10)

    def draw_area(self):
        # Implementation for the transparent overlay goes here
        print("Selection mode active...")