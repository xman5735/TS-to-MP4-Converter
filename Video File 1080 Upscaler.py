import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk # Step 1
import os
import cv2

def upscale_video(input_path, progress_bar, file_label):
    """Upscale a video to 1080p if it is 720p or below."""
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if height <= 720:
        upscale_factor = 1080 / height
        new_width = int(width * upscale_factor)
        new_height = int(height * upscale_factor)
        output_path = os.path.splitext(input_path)[0] + ' up.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 30.0, (new_width, new_height))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (new_width, new_height))
            out.write(frame)
        cap.release()
        out.release()
        progress_bar.step(1)
        progress_bar.update()
        file_label.config(text=f"{progress_bar['value']} / {progress_bar['maximum']} files converted") # Step 6

def process_folder(folder_path, progress_bar, file_label):
    """Recursively process a folder and its subfolders for mp4 or ts files."""
    file_count = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.mp4', '.ts')):
                input_path = os.path.join(root, file)
                upscale_video(input_path, progress_bar, file_label)
                file_count += 1
    progress_bar["value"] = 0
    progress_bar["maximum"] = file_count
    progress_bar.update()
    file_label.config(text=f"{progress_bar['value']} / {progress_bar['maximum']} files converted")
    messagebox.showinfo(title='Upscale Complete', message='Videos have been upscaled.')

def choose_folder():
    """Prompt the user to choose a folder and start processing it."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_count = sum(len(files) for _, _, files in os.walk(folder_path) if files)
        progress_bar = ttk.Progressbar(root, maximum=file_count, mode='determinate') # Step 2
        progress_bar.pack(pady=10)
        file_label = tk.Label(root, text="0 / {}".format(file_count))
        file_label.pack()
        process_folder(folder_path, progress_bar, file_label)

# Create the main Tkinter window
root = tk.Tk()
root.title('Video Upscaler')

# Add a button to choose a folder and start processing
button = tk.Button(root, text='Choose Folder', command=choose_folder)
button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
