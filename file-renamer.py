import os
from datetime import datetime
import exifread
import subprocess

def get_image_date_taken(file_path):
    """Extract date and time from image EXIF data."""
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)
        date_taken_tag = tags.get('EXIF DateTimeOriginal')
        if date_taken_tag:
            return str(date_taken_tag)
    return None

def get_video_date_taken(file_path):
    """Extract date and time from video metadata."""
    # This is a placeholder function. Actual implementation depends on the video format and metadata.
    return None

def rename_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg'):
            file_path = os.path.join(directory, filename)
            date_taken = get_image_date_taken(file_path)
            if date_taken:
                new_name = datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d_%H-%M-%S') + '.jpg'
                os.rename(file_path, os.path.join(directory, new_name))
        elif filename.lower().endswith('.mp4'):
            # Similar handling for MP4 files using get_video_date_taken
            pass  # Placeholder

# Replace '/path/to/directory' with the path of your target directory
rename_files_in_directory('/path/to/directory')
