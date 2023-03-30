import os
import shutil

source_folder = 'SOURCE' # replace with the path of your source folder
target_folder = 'TARGET' # replace with the path of your target folder

# List of video file extensions
video_formats = ['.mp4', '.gif', '.mov', '.webm', '.avi', '.wmv', '.rm', '.mpg', '.mpe', '.mpeg', '.mkv', '.m4v', '.mts', '.m2ts', '.MP4']

# Iterate over all the files and folders in the source folder
for root, dirs, files in os.walk(source_folder):
    for file in files:
        # Check if the file is a video file by its extension
        if os.path.splitext(file)[1].lower() in video_formats:
            # Construct the full path of the source file
            source_file = os.path.join(root, file)
            # Construct the full path of the target file
            target_file = os.path.join(target_folder, file)
            # Move the file to the target folder
            shutil.move(source_file, target_file)
