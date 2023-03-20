import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

# Create a tkinter window
window = tk.Tk()
window.title("TS to MP4 Converter")

# Create a label to display the input folder path
input_folder_label = tk.Label(window, text="Input Folder:")
input_folder_label.grid(column=0, row=0)

# Create a label to display the progress
progress_label = tk.Label(window, text="")
progress_label.grid(column=0, row=1)

varDelete = tk.IntVar()
delete_checkbox = tk.Checkbutton(window, text="Delete Source File?", variable=varDelete, onvalue=1, offvalue=0)
delete_checkbox.grid(column=0, row=3)

# Create a progress bar
progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(column=0, row=2, pady=10)

# Define a function to handle the "Select Input Folder" button click event
def select_input_folder():
    # Ask the user to select the input folder and update the input folder label
    input_folder_path = filedialog.askdirectory()
    input_folder_label.configure(text="Input Folder: " + input_folder_path)

# Define a function to handle the "Convert" button click event
def convert_files():
    # Get the input folder path from the label
    input_folder_path = input_folder_label.cget("text")[len("Input Folder: "):]


    # Get a list of all video files in the input folder and its subdirectories except .raw
    input_files = []
    for dirpath, dirnames, filenames in os.walk(input_folder_path):
        for filename in filenames:
            if filename.endswith(('.avi', '.mkv', '.flv', '.mov', '.ts')) and not filename.endswith('.raw'):
                input_files.append(os.path.join(dirpath, filename))

    # Loop through each input file and convert it to an mp4 file
    for i, input_file in enumerate(input_files):
        # Create the output file name by replacing the file extension with .mp4
        output_file = os.path.splitext(input_file)[0] + '.mp4'

        # Update the progress bar and label
        progress_bar["value"] = (i + 1) * 100 / len(input_files)
        progress_label.configure(text="Converting file {0} of {1}".format(i + 1, len(input_files)))
        window.update()

        # Run the ffmpeg command to convert the file with hardware acceleration
        subprocess.call(['ffmpeg', '-y', '-hwaccel', 'auto', '-i', input_file, '-c:v', 'h264_nvenc', '-c:a', 'copy', output_file])
        if varDelete.get() == 1:
            os.remove(input_file)

    # Reset the progress bar and label
    progress_bar["value"] = 0
    progress_label.configure(text="Conversion complete!")



# Create a "Select Input Folder" button
select_input_folder_button = tk.Button(window, text="Select Input Folder", command=select_input_folder)
select_input_folder_button.grid(column=1, row=0)

# Create a "Convert" button
convert_button = tk.Button(window, text="Convert", command=convert_files)
convert_button.grid(column=0, pady=10)

#Run the tkinter event loop
window.mainloop()
