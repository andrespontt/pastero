
import customtkinter as ctk

class PasteroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Pastero")
        self.geometry("800x600")
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add title label
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Pastero",
            font=("Arial", 24, "bold")
        )
        self.title_label.pack(pady=20)
        
        # Add text area
        self.text_area = ctk.CTkTextbox(
            self.main_frame,
            width=700,
            height=400,
            font=("Arial", 14)
        )
        self.text_area.pack(pady=10)
        
        # Add buttons frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=10)
        
        # Add buttons
        self.trim_button = ctk.CTkButton(
            self.button_frame,
            text="Trim Text",
            command=self.trim_text
        )
        self.trim_button.pack(side="left", padx=5)
        
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            command=self.clear_text
        )
        self.clear_button.pack(side="left", padx=5)

    def trim_text(self):
        text = self.text_area.get("1.0", "end-1c")
        trimmed = text.strip()
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", trimmed)

    def clear_text(self):
        self.text_area.delete("1.0", "end")

if __name__ == "__main__":
    app = PasteroApp()
    app.mainloop()
