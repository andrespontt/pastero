
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
        
        # Add line numbers frame
        self.line_numbers_frame = ctk.CTkFrame(self.text_container, fg_color="gray20")
        self.line_numbers_frame.pack(side="left", fill="y")
        
        # Add line numbers with tooltip frame
        self.tooltip = ctk.CTkLabel(
            self.main_frame,
            text="Click to copy line",
            fg_color="gray30",
            corner_radius=6,
            padx=10,
            pady=5
        )
        
        # Add line numbers
        self.line_numbers = ctk.CTkTextbox(
            self.line_numbers_frame,
            width=30,
            height=400,
            font=("Arial", 14),
            fg_color="gray20",
            border_width=0
        )
        self.line_numbers.pack(fill="both", expand=True)
        self.line_numbers.configure(state="disabled")
        
        # Bind line numbers for copy functionality
        self.line_numbers.bind("<Enter>", self.show_copy_cursor)
        self.line_numbers.bind("<Leave>", self.hide_copy_cursor)
        self.line_numbers.bind("<Button-1>", self.copy_line)
        
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
        
        # Add status bar
        self.status_bar = ctk.CTkLabel(
            self.main_frame,
            text="",
            height=25,
            font=("Arial", 12)
        )
        self.status_bar.pack(side="bottom", fill="x", pady=(10, 0))

    def show_status(self, message, duration=2000):
        self.status_bar.configure(text=message)
        self.after(duration, lambda: self.status_bar.configure(text=""))

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
    
    def show_copy_cursor(self, event):
        self.line_numbers.configure(cursor="hand2")
        self.tooltip.place(x=event.x_root - self.winfo_x() - 30, 
                         y=event.y_root - self.winfo_y() + 20)
    
    def hide_copy_cursor(self, event):
        self.line_numbers.configure(cursor="")
        self.tooltip.place_forget()
    
    def copy_line(self, event):
        # Get clicked line number
        index = self.line_numbers.index(f"@{event.x},{event.y}")
        line_num = int(index.split(".")[0])
        
        # Get and trim the corresponding line from text area
        line = self.text_area.get(f"{line_num}.0", f"{line_num}.end").strip()
        
        # Copy to clipboard
        self.clipboard_clear()
        self.clipboard_append(line)
        self.show_status(f"Copied: {line[:50]}{'...' if len(line) > 50 else ''}")

if __name__ == "__main__":
    app = PasteroApp()
    app.mainloop()
