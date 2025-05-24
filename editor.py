import tkinter as tk
from tkinter import filedialog, messagebox

_modified_flag = False

def update_line_numbers(text_area, line_numbers_widget):
    global _modified_flag
    if not _modified_flag:
        return

    line_numbers_widget.config(state='normal')
    line_numbers_widget.delete('1.0', 'end')

    # Get number of lines from text_area
    # The index 'end-1c' gives the position of the last character,
    # and its line number is the total number of lines.
    # If the text_area is empty, index 'end-1c' is '1.0', so lines will be 1.
    # We need to handle the truly empty case or single line case carefully.
    
    content = text_area.get("1.0", "end-1c") # Get all content except the final newline
    if not content:
        num_lines = 0
    else:
        num_lines = content.count('\n') + 1

    if num_lines == 0: # Handles if content was empty string
        line_numbers_text = ""
    else:
        line_numbers_text = "\n".join(str(i) for i in range(1, num_lines + 1))
    
    line_numbers_widget.insert('1.0', line_numbers_text)
    line_numbers_widget.config(state='disabled')
    _modified_flag = False
    # text_area.edit_modified(False) # Reset the text_area's own modified flag


def on_text_modified(event, text_area, line_numbers_widget):
    global _modified_flag
    _modified_flag = True
    # Using after_idle to ensure the text widget has fully processed the modification
    # before we try to count lines. This also helps break potential recursive loops.
    text_area.after_idle(lambda: update_line_numbers(text_area, line_numbers_widget))
    # It's also good practice to reset the widget's internal modified flag
    # if the event system requires it, though for <<Modified>> and after_idle,
    # the main concern is re-entrancy into update_line_numbers.
    # The provided solution uses a global _modified_flag, which is one way.
    # A more encapsulated way is to use widget attributes or a class.
    # For now, let's stick to the logic that update_line_numbers clears its own global flag.
    # For <<Modified>> to re-trigger, we must call edit_modified(True) or text changes.
    # The critical part is that update_line_numbers itself should not cause <<Modified>> on text_area.
    # And it doesn't.
    # However, the <<Modified>> event itself needs to be reset on the text_area
    # so it can fire again for subsequent changes.
    text_area.edit_modified(False)


def main():
    root = tk.Tk()
    root.title("Line Click Copy Editor")

    # Scrollbar for the text_area
    text_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
    
    # Line numbers Text widget
    line_numbers = tk.Text(
        root, 
        width=4, 
        padx=4, 
        takefocus=0, 
        border=0, 
        background='lightgrey', 
        state='disabled',
        font=('TkFixedFont', 10) # Monospaced font helps alignment
    )
    line_numbers.pack(side=tk.LEFT, fill=tk.Y)

    # Main Text widget
    text_area = tk.Text(
        root, 
        wrap=tk.WORD, 
        undo=True,
        font=('TkFixedFont', 10) # Monospaced font
    )
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure scrolling synchronization
    # When text_area is scrolled (by mouse wheel, arrow keys, etc.),
    # its yscrollcommand is called. We use this to update the scrollbar's position
    # AND to scroll the line_numbers widget.
    def on_text_scroll(*args):
        text_scrollbar.set(*args)
        line_numbers.yview_moveto(args[0])

    # When the scrollbar is dragged, its command is called.
    # We use this to scroll both the text_area AND the line_numbers widget.
    def on_scrollbar_drag(*args):
        text_area.yview(*args)
        line_numbers.yview(*args)

    text_area.config(yscrollcommand=on_text_scroll)
    text_scrollbar.config(command=on_scrollbar_drag)
    text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    # Insert some default multi-line text
    default_text = "Line 1\nLine 2\nLine 3\n\nLine 5\n"
    for i in range(6, 26):
        default_text += f"Line {i}\n"
    text_area.insert('1.0', default_text)

    # Bind modification event to update line numbers
    # The lambda takes the event object (which we don't strictly need here but is passed by bind)
    text_area.bind('<<Modified>>', lambda event: on_text_modified(event, text_area, line_numbers))

    # Initial population of line numbers
    # We need to set the flag true once before the first call, then call update_line_numbers
    # or rather, simulate a modification event context.
    global _modified_flag
    _modified_flag = True 
    update_line_numbers(text_area, line_numbers)
    text_area.edit_modified(False) # Clear flag after initial update

    # Bind click event to line_numbers widget for copying line content
    line_numbers.bind("<Button-1>", lambda event: on_line_number_click(event, text_area, line_numbers, root))

    # Setup Menubar
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=lambda: load_file(text_area, line_numbers, root))
    # Add more file operations here later (Save, Exit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    root.mainloop()

# Function to load a file into the text_area
def load_file(text_area_widget, line_numbers_widget, root_window):
    filepath = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")]
    )
    if not filepath: # User cancelled dialog
        return

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        text_area_widget.delete("1.0", tk.END)
        text_area_widget.insert("1.0", content)
        
        # Programmatic insertion triggers <<Modified>>, which calls on_text_modified.
        # on_text_modified sets _modified_flag = True, schedules update_line_numbers,
        # and then calls text_area_widget.edit_modified(False).
        # This sequence should correctly update the line numbers.
        # If any issues, one might need to manually manage the _modified_flag
        # and call update_line_numbers, e.g.:
        # global _modified_flag
        # _modified_flag = True
        # update_line_numbers(text_area_widget, line_numbers_widget)
        # text_area_widget.edit_modified(False) 
        # But relying on the existing event mechanism is cleaner if it works.

    except FileNotFoundError:
        messagebox.showerror("Error Opening File", f"File not found:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error Opening File", f"Failed to read file:\n{filepath}\n\nError: {e}")


# Function to handle clicks on the line number widget
def on_line_number_click(event, text_area_widget, line_numbers_widget, root_window):
    original_state = line_numbers_widget.cget('state')
    try:
        line_numbers_widget.config(state='normal')
        
        # Get the text index at the click position (e.g., "3.0")
        clicked_index_str = line_numbers_widget.index(f"@0,{event.y}")
        
        # Extract the line part of the index (e.g., "3")
        line_num_from_index = clicked_index_str.split('.')[0]

        # Get the actual content of that line in the line_numbers_widget (e.g., "3\n")
        # and strip whitespace to get the pure number string.
        actual_line_num_text = line_numbers_widget.get(f"{line_num_from_index}.0", f"{line_num_from_index}.end").strip()

        # If the retrieved text is not a digit, it means we clicked in an empty area
        # (e.g., below the last line number or on padding).
        if not actual_line_num_text.isdigit():
            return # Do nothing

        # Convert the validated line number string to an integer
        target_line_num = int(actual_line_num_text)

        # Define start and end indices for the text_area_widget
        start_index = f"{target_line_num}.0"
        end_index = f"{target_line_num}.end" # .end includes the newline

        # Retrieve the line content from the text_area_widget
        line_content = text_area_widget.get(start_index, end_index)
        
        # If the line_content ends with a newline, and the task implies copying *just* the visible content
        # one might strip it. However, copying the full line usually includes the newline.
        # The prompt says "copy the line as is", so we keep the newline.

        # Copy to clipboard
        root_window.clipboard_clear()
        root_window.clipboard_append(line_content)
        
    except tk.TclError:
        # This can happen if the click is completely outside any valid text index
        # or other widget-specific issues.
        pass # Gracefully handle by doing nothing
    except Exception:
        # Catch any other unexpected error during the process
        pass # Gracefully handle
    finally:
        line_numbers_widget.config(state=original_state)


if __name__ == "__main__":
    main()
