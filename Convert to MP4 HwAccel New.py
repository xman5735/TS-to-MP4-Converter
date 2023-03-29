import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


def select_input_folder():
    input_folder_path = filedialog.askdirectory()
    input_folder_label.configure(text=f"Input Folder: {input_folder_path}")


def get_input_files(input_folder_path):
    input_files = []
    for dirpath, dirnames, filenames in os.walk(input_folder_path):
        for filename in filenames:
            if filename.endswith(('.avi', '.mkv', '.flv', '.mov', '.ts')):
                input_files.append(os.path.join(dirpath, filename))
    return input_files


def convert_file(input_file, output_file, output_format):
    subprocess.call([
        'ffmpeg', '-y', '-hwaccel', 'auto', '-i', input_file,
        '-c:v', 'h264_nvenc', '-c:a', 'copy', output_file
    ])


def convert_files():
    input_folder_path = input_folder_label.cget("text").replace("Input Folder: ", "")
    output_format = output_format_var.get()

    input_files = get_input_files(input_folder_path)

    for i, input_file in enumerate(input_files):
        output_folder_path = os.path.dirname(input_file)
        output_file = os.path.join(output_folder_path, f"{os.path.splitext(os.path.basename(input_file))[0]}.{output_format}")

        progress_bar["value"] = (i + 1) * 100 / len(input_files)
        progress_label.configure(text=f"Converting file {i + 1} of {len(input_files)}")
        window.update()

        convert_file(input_file, output_file, output_format)

    progress_bar["value"] = 0
    progress_label.configure(text="Conversion complete!")


window = tk.Tk()
window.title("Video Converter")

input_folder_label = tk.Label(window, text="Input Folder:")
input_folder_label.grid(column=0, row=0)

progress_label = tk.Label(window, text="")
progress_label.grid(column=0, row=4)

progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(column=0, row=3, pady=10)

output_format_label = tk.Label(window, text="Output Format:")
output_format_label.grid(column=0, row=1)
output_format_var = tk.StringVar(window)
output_format_var.set("mp4")
output_formats = ["mp4", "avi", "mkv", "flv", "mov"]
output_format_dropdown = tk.OptionMenu(window, output_format_var, *output_formats)
output_format_dropdown.grid(column=1, row=1)

select_input_folder_button = tk.Button(window, text="Select Input Folder", command=select_input_folder)
select_input_folder_button.grid(column=1, row=0)

convert_button = tk.Button(window, text="Convert", command=convert_files)
convert_button.grid(column=0, row=5, pady=10)

# Run the tkinter event loop
window.mainloop()
