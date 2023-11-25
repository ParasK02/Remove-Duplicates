import sys
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from tkinter import ttk
import tkinter as tk
import os
import hashlib
from pathlib import Path
import send2trash  # Install send2trash for use
from tkinter.messagebox import showinfo


# File delete logic
excluded_file_types = ['.exe', '.dll']


def choose_directory():
    folder_path = filedialog.askdirectory(title="Select a folder")
    if folder_path:
        delete_duplicates(folder_path)


def delete_duplicates(root_folder):
    """Delete duplicate files in the specified folder."""
    unique_files = dict()
    total_files = sum(len(files) for _, _, files in os.walk(root_folder))
    deleted_files = 0

    for root, _, files in os.walk(root_folder):
        for file in files:
            file_path = Path(os.path.join(root, file))
            file_hash = get_file_hash(file_path)
            if file_path.suffix.lower() in excluded_file_types:
                continue

            if file_hash not in unique_files:
                unique_files[file_hash] = file_path
            else:
                send2trash.send2trash(file_path)
                deleted_files += 1
                progress(total_files, deleted_files)
                print(f"{file_path} has been deleted")

    # Ensure that the progress bar reaches 100% at the end
    progress(total_files, total_files)


def get_file_hash(file_path):
    """Calculate the MD5 hash of a file."""
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


# GUI logic

def update_progress_label(total, current):
    return f"Current Progress: {int((current / total) * 100)}%"


def progress(total, current):
    pb['value'] = (current / total) * 100
    value_label['text'] = update_progress_label(total, current)
    window.update_idletasks()  # Update the GUI immediately

    if current == total:
        showinfo(message='The progress completed!')


window = tk.Tk()
window.geometry("450x300")
window.title("Remove Duplicates")

title_label = tk.Label(window, text="Remove Duplicates", font=("Helvetica", 16, "bold"))
title_label.grid(column=0, row=0, columnspan=2, pady=10)

description_label = tk.Label(window, text="This is a simple script that will remove any duplicates in the selected directory")
description_label.grid(column=0, row=1, columnspan=2, pady=20, padx=20)

button = tk.Button(window, text="Select Directory", command=choose_directory)
button.grid(column=0, row=6, columnspan=2, pady=10)

pb = ttk.Progressbar(
    window,
    orient='horizontal',
    mode='determinate',
    length=280
)
pb.grid(column=0, row=3, columnspan=2, padx=10, pady=20)

# Label
value_label = ttk.Label(window, text="")
value_label.grid(column=0, row=4, columnspan=2)

window.mainloop()
