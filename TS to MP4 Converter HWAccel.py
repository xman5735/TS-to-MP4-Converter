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

# Create a label to display the output folder path
output_folder_label = tk.Label(window, text="Output Folder:")
output_folder_label.grid(column=0, row=1)

# Create a label to display the progress
progress_label = tk.Label(window, text="")
progress_label.grid(column=0, row=2)

# Create a progress bar
progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(column=0, row=3, pady=10)

# Define a function to handle the "Select Input Folder" button click event
def select_input_folder():
    # Ask the user to select the input folder and update the input folder label
    input_folder_path = filedialog.askdirectory()
    input_folder_label.configure(text="Input Folder: " + input_folder_path)

# Define a function to handle the "Select Output Folder" button click event
def select_output_folder():
    # Ask the user to select the output folder and update the output folder label
    output_folder_path = filedialog.askdirectory()
    output_folder_label.configure(text="Output Folder: " + output_folder_path)

# Define a function to handle the "Convert" button click event
def convert_files():
    # Get the input and output folder paths from the labels
    input_folder_path = input_folder_label.cget("text")[len("Input Folder: "):]
    output_folder_path = output_folder_label.cget("text")[len("Output Folder: "):]

    # Get a list of all .ts files in the input folder
    input_files = [f for f in os.listdir(input_folder_path) if f.endswith('.ts')]

    # Loop through each input file and convert it to an mp4 file
    for i, input_file in enumerate(input_files):
        # Create the output file name by replacing the .ts extension with .mp4
        output_file = os.path.join(output_folder_path, input_file.replace('.ts', '.mp4'))

        # Update the progress bar and label
        progress_bar["value"] = (i + 1) * 100 / len(input_files)
        progress_label.configure(text="Converting file {0} of {1}".format(i + 1, len(input_files)))
        window.update()

       # Run the ffmpeg command to convert the file with hardware acceleration
        subprocess.call(['ffmpeg', '-hwaccel', 'auto', '-i', os.path.join(input_folder_path, input_file), '-c:v', 'h264_nvenc', '-c:a', 'copy', output_file])

    # Reset the progress bar and label
    progress_bar["value"] = 0
    progress_label.configure(text="Conversion complete!")

# Create "Select Input Folder" and "Select Output Folder" buttons
select_input_folder_button = tk.Button(window, text="Select Input Folder", command=select_input_folder)
select_input_folder_button.grid(column=1, row=0)

select_output_folder_button = tk.Button(window, text="Select Output Folder", command=select_output_folder)
select_output_folder_button.grid(column=1, row=1)

# Create a "Convert" button
convert_button = tk.Button(window, text="Convert", command=convert_files)
convert_button.grid(column=0, pady=10)

#Run the tkinter event loop
window.mainloop()

