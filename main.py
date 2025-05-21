
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
        
        # Create text container frame
        self.text_container = ctk.CTkFrame(self.main_frame)
        self.text_container.pack(pady=10)
        
        # Add line numbers
        self.line_numbers = ctk.CTkTextbox(
            self.text_container,
            width=30,
            height=400,
            font=("Arial", 14),
            fg_color="gray20",
            border_width=0
        )
        self.line_numbers.pack(side="left", fill="y")
        self.line_numbers.configure(state="disabled")
        
        # Add text area
        self.text_area = ctk.CTkTextbox(
            self.text_container,
            width=670,
            height=400,
            font=("Arial", 14)
        )
        self.text_area.pack(side="left")
        
        # Bind text changes to update line numbers
        self.text_area.bind("<KeyRelease>", self.update_line_numbers)
        self.text_area.bind("<MouseWheel>", self.sync_scroll)
        self.line_numbers.bind("<MouseWheel>", self.sync_scroll)
        
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
        self.update_line_numbers(None)
        
    def update_line_numbers(self, event=None):
        lines = self.text_area.get("1.0", "end-1c").count("\n") + 1
        line_numbers_text = "\n".join(str(i) for i in range(1, lines + 1))
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.configure(state="disabled")
        
    def sync_scroll(self, event):
        self.line_numbers.yview_moveto(self.text_area.yview()[0])

if __name__ == "__main__":
    app = PasteroApp()
    app.mainloop()
