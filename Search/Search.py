import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess

# Global stop event
stop_event = threading.Event()

def search_files():
    query = entry.get().strip()
    extension = extension_var.get().strip()
    recursive = recursive_var.get()
    root_dir = os.path.expanduser("~")

    if not query:
        messagebox.showwarning("Input Error", "Please enter a file name.")
        return

    results_list.delete(0, tk.END)
    progress_bar.start()
    stop_event.clear()

    def run_search():
        for foldername, subfolders, filenames in os.walk(root_dir):
            if stop_event.is_set():
                break
            for filename in filenames:
                if stop_event.is_set():
                    break
                if query.lower() in filename.lower():
                    if extension and not filename.lower().endswith(extension.lower()):
                        continue
                    full_path = os.path.join(foldername, filename)
                    results_list.insert(tk.END, full_path)
            if not recursive:
                break
        progress_bar.stop()

    threading.Thread(target=run_search, daemon=True).start()

def stop_search():
    stop_event.set()

def open_in_explorer(event):
    selection = results_list.curselection()
    if selection:
        file_path = results_list.get(selection[0])
        if os.path.exists(file_path):
            subprocess.run(f'explorer /select,"{file_path}"')

# === GUI Setup ===
root = tk.Tk()
root.title("Modern File Search Tool")
root.geometry("900x600")

# === Colors and Fonts ===
bg_color = "#1e1e1e"
fg_color = "#ffffff"
entry_bg = "#2d2d2d"
entry_fg = "#ffffff"
highlight = "#3e8ef7"
font_main = ("Segoe UI", 11)

root.configure(bg=bg_color)

# === Style Setup ===
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TFrame", background=bg_color)
style.configure("TLabel", background=bg_color, foreground=fg_color, font=font_main)
style.configure("TEntry", fieldbackground=entry_bg, foreground=entry_fg, font=font_main)
style.configure("TButton", background=highlight, foreground="#ffffff", font=font_main, padding=6)
style.map("TButton", background=[("active", "#5a9bfc")])
style.configure("TCheckbutton", background=bg_color, foreground=fg_color, font=font_main)
style.configure("TProgressbar", background=highlight, troughcolor="#2d2d2d", thickness=8)

# === Main Frame ===
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

# Widgets
ttk.Label(main_frame, text="Search for file:").grid(row=0, column=0, sticky="w", pady=5)
entry = ttk.Entry(main_frame, width=45)
entry.grid(row=0, column=1, sticky="ew", padx=10)

ttk.Label(main_frame, text="Filter by extension (optional):").grid(row=1, column=0, sticky="w", pady=5)
extension_var = tk.StringVar()
extension_entry = ttk.Entry(main_frame, textvariable=extension_var, width=20)
extension_entry.grid(row=1, column=1, sticky="w", padx=10)

recursive_var = tk.BooleanVar(value=True)
recursive_check = ttk.Checkbutton(main_frame, text="Include subfolders", variable=recursive_var)
recursive_check.grid(row=2, column=1, sticky="w", pady=5)

search_button = ttk.Button(main_frame, text="Search", command=search_files)
search_button.grid(row=3, column=1, sticky="w", pady=10)

stop_button = ttk.Button(main_frame, text="Stop", command=stop_search)
stop_button.grid(row=3, column=1, sticky="e", pady=10)

progress_bar = ttk.Progressbar(main_frame, mode="indeterminate", length=300)
progress_bar.grid(row=4, column=0, columnspan=2, pady=10)

ttk.Label(main_frame, text="Search Results:").grid(row=5, column=0, sticky="w", pady=(15, 5))

# === Listbox with Dark Scrollbar ===
results_list = tk.Listbox(main_frame,
                          height=18, width=100,
                          bg=entry_bg, fg=fg_color,
                          selectbackground=highlight,
                          selectforeground="#ffffff",
                          font=font_main,
                          highlightthickness=1,
                          relief="flat",
                          highlightbackground="#444")
results_list.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=(0, 5))
results_list.bind("<Double-Button-1>", open_in_explorer)

scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=results_list.yview,
                         bg=bg_color, activebackground=bg_color, troughcolor=entry_bg)
scrollbar.grid(row=6, column=2, sticky="ns")
results_list.config(yscrollcommand=scrollbar.set)

# === Resize Config ===
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(6, weight=1)

# === Run ===
root.mainloop()
