import os
from datetime import datetime
import exifread
import subprocess

# Function to extract date and time from image EXIF data
def get_image_date_taken(file_path):
    """Extract date and time from image EXIF data."""
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)
        date_taken_tag = tags.get('EXIF DateTimeOriginal')
        if date_taken_tag:
            return str(date_taken_tag)
    return None

# Function to extract date and time from video metadata (MP4 format)
def get_video_date_taken(file_path):
    """Extract date and time from video metadata (MP4 format)."""
    try:
        # Use the 'ffprobe' tool from FFmpeg to extract creation time from MP4 video metadata
        cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream_tags=creation_time', '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
        creation_time = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True).strip()
        if creation_time:
            return creation_time
    except Exception as e:
        print(f"Error extracting video creation time from {file_path}: {str(e)}")
    return None

# Function to rename files in a directory based on date and time
def rename_files_in_directory(source_directory, destination_directory):
    renamed_files = []  # To store the successfully renamed files
    not_renamed_files = []  # To store files that were not renamed
    
    for filename in os.listdir(source_directory):
        source_path = os.path.join(source_directory, filename)
        
        if filename.lower().endswith('.jpg'):
            date_taken = get_image_date_taken(source_path)
            if date_taken:
                try:
                    # Convert the extracted date and time to the desired format and add it to the new filename
                    new_name = datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S').strftime('%Y%m%d_%H%M%S') + '.jpg'
                    destination_path = os.path.join(destination_directory, new_name)
                    
                    # Rename the file
                    os.rename(source_path, destination_path)
                    renamed_files.append(filename)
                except Exception as e:
                    not_renamed_files.append(filename)
                    print(f"Error renaming {filename}: {str(e)}")
        elif filename.lower().endswith('.mp4'):
            date_taken = get_video_date_taken(source_path)
            if date_taken:
                try:
                    # Convert the extracted date and time to the desired format and add it to the new filename
                    new_name = datetime.strptime(date_taken, '%Y-%m-%dT%H:%M:%S').strftime('%Y%m%d_%H%M%S') + '.mp4'
                    destination_path = os.path.join(destination_directory, new_name)
                    
                    # Rename the file
                    os.rename(source_path, destination_path)
                    renamed_files.append(filename)
                except Exception as e:
                    not_renamed_files.append(filename)
                    print(f"Error renaming {filename}: {str(e)}")
        else:
            # Handle other file types or extensions if needed
            pass  # Placeholder
    
    return renamed_files, not_renamed_files

if __name__ == "__main__":
    # Get user input for source and destination directories
    source_directory = input("Enter the source directory path: ")
    destination_directory = input("Enter the destination directory path: ")

    # Call the rename_files_in_directory function with user-provided directories
    renamed_files, not_renamed_files = rename_files_in_directory(source_directory, destination_directory)

    # Display status messages and lists of renamed and not renamed files
    print("Status:")
    if renamed_files:
        print("Renamed files:")
        for filename in renamed_files:
            print(f"- {filename}")
    if not_renamed_files:
        print("Files not renamed:")
        for filename in not_renamed_files:
            print(f"- {filename}")
    print("Script completed successfully.")
