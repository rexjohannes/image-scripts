import os
import shutil
from PIL import Image
from datetime import datetime

# Define input and output directories
input_dir = 'SOURCE'
output_dir = 'TARGET'

# Define a list of allowed image formats
photo_formats = ['.jpg', '.jpeg', '.webp', '.bmp', '.tif', '.tiff', '.svg', '.heic', '.JPG', '.JPEG', '.MPO']

# Define a dictionary mapping month numbers to their German names
months = {
    1: '01 - Januar',
    2: '02 - Februar',
    3: '03 - März',
    4: '04 - April',
    5: '05 - Mai',
    6: '06 - Juni',
    7: '07 - Juli',
    8: '08 - August',
    9: '09 - September',
    10: '10 - Oktober',
    11: '11 - November',
    12: '12 - Dezember'
}

# Iterate over all files in the input directory and its subdirectories
for root, dirs, files in os.walk(input_dir):
    for file in files:
        # Check if the file is an image
        _, ext = os.path.splitext(file)
        if ext.lower() not in photo_formats:
            continue

        # Read the EXIF data from the image file
        try:
            with Image.open(os.path.join(root, file)) as img:
                exif_data = img._getexif()
        except (AttributeError, OSError, IndexError):
            print(f"Skipping file '{file}' in '{root}' - unable to read EXIF data")
            exif_data = None

        # Extract the date information from the EXIF data, or use the file's creation date if not available
        if exif_data is not None:
            try:
                date_str = exif_data[36867]
                date_taken = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
            except (KeyError, ValueError):
                print(f"Unable to parse date information from EXIF data for file '{file}' in '{root}'")
                date_taken = False
        else:
            # Put them in Unknown folder if no date info is available
            date_taken = False
            print(f"Unable to parse date information from EXIF data for file '{file}' in '{root}'")

        if date_taken == False:
            year_dir_name = 'Unknown'
            year_dir_path = os.path.join(output_dir, year_dir_name)
            output_path = os.path.join(year_dir_path, file)
        else:
            # Create the output directory structure based on the date information
            year = date_taken.year
            month = date_taken.month
            month_name = months.get(month, str(month)).replace('_', ' ')
            month_dir_name = f"{month_name} {str(year)}"
            year_dir_name = str(year)
            year_dir_path = os.path.join(output_dir, year_dir_name)
            month_dir_path = os.path.join(year_dir_path, month_dir_name)
            output_path = os.path.join(month_dir_path, file)

        # Create the output directory structure if it does not exist
        if not os.path.exists(year_dir_path):
            print(f"Creating directory '{year_dir_path}'")
            os.makedirs(year_dir_path)

        if date_taken != False:
            if not os.path.exists(month_dir_path):
                print(f"Creating directory '{month_dir_path}'")
                os.makedirs(month_dir_path)

        # Move the file to the output directory
        src_path = os.path.join(root, file)
        print(f"Moving file '{src_path}' to '{output_path}'")
        shutil.move(src_path, output_path)
