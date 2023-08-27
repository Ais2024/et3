
import json
import shutil
from PIL.ExifTags import TAGS
import os
import re
from datetime import datetime
import csv
from PIL import Image

############################################   fun
def remove_prefix(image_name):
    match = re.search(r'^.*?-+', image_name)
    if match:
        return image_name[match.end():]  # Return the part of the image name after the hyphen
    return image_name  # Return the original name if no match


def get_modification_type(image_path, original_width, original_height):
    with Image.open(image_path) as img:
        width, height = img.size
        if width == original_height and height == original_width:
            return "Orientation Change"
        elif width / height != original_width / original_height:
            return "Cropped"
        else:
            return "Other"

######################################################
# extract the images and copy them to a one folder

src_foldr = "D:\dairies"
targ_foldr = "D:\soli"

for folder, sub_folder, files in os.walk(src_foldr):
    for file in files:
        if file.endswith(".jpg"):
            print(file)
            filename = os.path.join(src_foldr, folder, file)
            if os.path.exists(filename):
                print(filename)
                shutil.copy(filename,targ_foldr)
print(len(os.listdir(targ_foldr)))

#############################################################

# for prefix

# Directory containing image files
image_directory = "D:\soli"

# List all files in the directory
image_files = os.listdir(image_directory)

for image_name in image_files:
    new_image_name = remove_prefix(image_name)
    print(f"Original Name: {image_name} | New Name: {new_image_name}")

############################################################################

# for modification and report
# Directory containing image files

image_directory = "D:\soli"

# CSV report file path
csv_report_path = "D:\soli\image_report.csv"

# Original dimensions (Replace these with the original image dimensions before any modification)
original_width = 1920
original_height = 1080

# List all files in the directory
image_files = os.listdir(image_directory)

# Create or overwrite the CSV file
with open(csv_report_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write header row
    csvwriter.writerow(['Image Name', 'Size (bytes)', 'Last Modification Date', 'Modification Type'])

    # Loop through each file in the directory
    for image_name in image_files:
        # Construct the full image path
        image_path = os.path.join(image_directory, image_name)

        # Check if the current file is an image
        if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # Extract image details
            clean_image_name = remove_prefix(image_name)
            image_size = os.path.getsize(image_path)
            timestamp = os.path.getmtime(image_path)
            last_modification = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            # Get modification type
            modification_type = get_modification_type(image_path, original_width, original_height)

            # Write the details to the CSV
            csvwriter.writerow([clean_image_name, image_size, last_modification, modification_type])
            print(f"Image Name: {image_name}")
            print(f"Image Size: {image_size} bytes")
            print(f"Last Modification Date: {last_modification}")
            print("-----")
print(f"Report generated at {csv_report_path}")
