import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store data
DATA_FILE = 'data.json'

def load_data():
    """Load data from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_data(data_list):
    """Save data to the JSON file."""
    with open(DATA_FILE, 'w') as file:
        json.dump(data_list, file, indent=4)

def copy_to_clipboard(entry):
    """Copy the content of the entry to the clipboard and highlight it."""
    root.clipboard_clear()
    root.clipboard_append(entry.get())
    entry.select_range(0, tk.END)  # Highlight the text
    entry.focus_set()  # Set focus on the entry field

def add_new_data_row():
    """Add a new row for data entry."""
    create_data_row(data_frame, "")

def remove_data_row(frame, entry):
    """Remove a data row after confirmation."""
    entry_value = entry.get().strip()
    if messagebox.askyesno("Confirm", "Do you want to remove this entry?"):
        # Forcibly remove the entry by its index
        for idx, row_frame in enumerate(data_frame.winfo_children()):
            if row_frame == frame:
                if idx < len(data_list):
                    data_list.pop(idx)  # Remove the entry at the index
                save_data(data_list)
                frame.destroy()
                break

def update_data(entry, old_value):
    """Update data in the list and save it."""
    new_value = entry.get().strip()
    if old_value in data_list:
        if new_value:
            index = data_list.index(old_value)
            data_list[index] = new_value
        else:
            # If the new value is empty, remove the entry
            data_list.remove(old_value)
        save_data(data_list)

def on_closing():
    """Handle window closing event."""
    unsaved_changes = False
    for entry in data_frame.winfo_children():
        if isinstance(entry, tk.Frame):
            for widget in entry.winfo_children():
                if isinstance(widget, tk.Entry):
                    if widget.get().strip():
                        unsaved_changes = True
                        break
            if unsaved_changes:
                break

    if unsaved_changes:
        response = messagebox.askyesnocancel("Confirm", "Do you want to save changes before closing?")
        if response is True:
            save_data(data_list)
            root.destroy()
        elif response is False:
            root.destroy()
    else:
        root.destroy()

def save_button_clicked():
    """Handle save button click event."""
    # Get all current entries from the UI
    global data_list
    data_list = [entry.get().strip() for frame in data_frame.winfo_children()
                 if isinstance(frame, tk.Frame)
                 for entry in frame.winfo_children()
                 if isinstance(entry, tk.Entry)]
    # Remove duplicates and empty entries
    data_list = [data for data in data_list if data]
    save_data(data_list)
    messagebox.showinfo("Saved", "Data saved to file.")

def toggle_always_on_top():
    """Toggle the always on top functionality."""
    global always_on_top
    always_on_top = not always_on_top
    root.attributes("-topmost", always_on_top)
    top_button.config(relief=tk.SUNKEN if always_on_top else tk.RAISED)

# Create the main window
root = tk.Tk()
root.title("Copypad")

# Frame to hold all data rows
data_frame = tk.Frame(root)
data_frame.pack(fill="both", expand=True, pady=0)  # Set pady to 0

# Load data from file
data_list = load_data()

def create_data_row(parent, data):
    """Create a row for each data entry."""
    frame = tk.Frame(parent)
    
    # Create a simple remove button
    remove_button = tk.Button(frame, text="[-]", fg="red", font=("Arial", 8, "bold"),
                              width=2, height=1, command=lambda: remove_data_row(frame, entry))
    remove_button.pack(side="left", padx=0, pady=0)  # Set padding to 0
    
    # Create an editable entry for data
    entry = tk.Entry(frame, width=30)
    entry.insert(0, data)
    entry.pack(side="left", padx=0, pady=0)  # Set padding to 0
    entry.bind('<FocusOut>', lambda e: update_data(entry, data))  # Update data on focus out

    # Copy button with an icon
    copy_button = tk.Button(frame, text="[C]", font=("Arial", 10, "bold"), width=3, height=1, command=lambda: copy_to_clipboard(entry))
    copy_button.pack(side="right", padx=0, pady=0)  # Set padding to 0

    # Insert at the top of the parent frame
    frame.pack(fill="x", pady=0)  # Set pady to 0

# Create a row for each data entry
for data in data_list:
    create_data_row(data_frame, data)

# Frame for buttons at the bottom
bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", fill="x", pady=5)

# Button to add new data entries
add_button = tk.Button(bottom_frame, text="[+]", width=4, height=1, command=add_new_data_row)
add_button.pack(side="left", padx=5)

# Save button to explicitly save data
save_button = tk.Button(bottom_frame, text="Save", width=4, height=1, command=save_button_clicked)
save_button.pack(side="left", padx=5)

# Toggle always on top button
always_on_top = False
top_button = tk.Button(bottom_frame, text="On Top", width=6, height=1, command=toggle_always_on_top)
top_button.pack(side="left", padx=5)

# Bind the window close event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the application
root.mainloop()
