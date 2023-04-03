import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

class VideoConverterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Converter")
        self.master.resizable(False, False)
        self.master.geometry("400x200")

        self.source_folder_path = tk.StringVar()
        self.convert_var = tk.BooleanVar()
        self.progress_var = tk.DoubleVar()

        self.source_folder_label = ttk.Label(self.master, text="Select a folder:")
        self.source_folder_label.pack(padx=10, pady=(10, 0))

        self.source_folder_entry = ttk.Entry(self.master, textvariable=self.source_folder_path, width=40)
        self.source_folder_entry.pack(padx=10, pady=(0, 10))

        self.source_folder_button = ttk.Button(self.master, text="Browse", command=self.browse_folder)
        self.source_folder_button.pack(padx=10, pady=(0, 10))

        self.convert_checkbox = ttk.Checkbutton(self.master, text="Delete source file after conversion", variable=self.convert_var)
        self.convert_checkbox.pack(padx=10, pady=(0, 10))

        self.progress_bar = ttk.Progressbar(self.master, orient="horizontal", length=300, mode="determinate", variable=self.progress_var)
        self.progress_bar.pack(padx=10, pady=(0, 10))

        self.convert_button = ttk.Button(self.master, text="Convert", command=self.convert_files)
        self.convert_button.pack(padx=10, pady=(0, 10))

        self.quit_button = ttk.Button(self.master, text="Quit", command=self.quit_app)
        self.quit_button.pack(padx=10, pady=(0, 10))

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.source_folder_path.set(folder_path)

    def convert_files(self):
        folder_path = self.source_folder_path.get()
        if not folder_path:
            messagebox.showwarning("Warning", "Please select a folder")
            return
        self.convert_button.config(state="disabled")
        self.quit_button.config(state="disabled")
        t = threading.Thread(target=self.convert_files_thread, args=(folder_path,))
        t.start()

    def convert_files_thread(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".ts"):
                    input_file = os.path.join(root, file)
                    output_file = os.path.splitext(input_file)[0] + ".mp4"
                    cmd = f'ffmpeg -y -i "{input_file}" -c:v libx264 -c:a aac -strict -2 "{output_file}"'
                    subprocess.run(cmd, shell=True)
                    if self.convert_var.get():
                        os.remove(input_file)
                    self.progress_var.set((files.index(file)+1)/len(files)*100)
                    self.master.update()
        self.convert_button.config(state="enabled")
        self.quit_button.config(state="enabled")
        messagebox.showinfo("Information", "Conversion completed")

    def quit_app(self):
        self.master.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()
