import os
import subprocess
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_video_files(path, extensions):
    video_files = []
    for ext in extensions:
        video_files.extend(list(path.glob(f'**/*{ext}')))
    return video_files

def convert_to_mp4(input_file, output_file, delete_source):
    command = f'ffmpeg -i "{input_file}" -codec:v libx264 -codec:a aac "{output_file}" -loglevel error'
    subprocess.run(command, shell=True)

    if delete_source:
        os.remove(input_file)

def process_video_file(video_file, delete_source):
    output_file = video_file.with_suffix('.mp4')
    convert_to_mp4(video_file, output_file, delete_source)

def main():
    folder = input("Enter the folder path: ")
    path = Path(folder)

    if not path.is_dir():
        print("Invalid folder path. Exiting.")
        return

    delete_source = input("Do you want to delete the source files after conversion? (y/n): ").lower() == 'y'

    video_extensions = ['.ts', '.avi', '.mkv', '.mov', '.wmv']
    video_files = get_video_files(path, video_extensions)

    if not video_files:
        print("No video files found. Exiting.")
        return

    with ThreadPoolExecutor() as executor:
        tasks = {executor.submit(process_video_file, video_file, delete_source): video_file for video_file in video_files}

        for task in tqdm(as_completed(tasks), desc="Converting", total=len(tasks), unit="file"):
            pass

    print("Video conversion completed.")

if __name__ == '__main__':
    main()
