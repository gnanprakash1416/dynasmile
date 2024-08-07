import os
import zipfile


def zip_directory(folder_path, zip_file):
    for folder_name, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            # Create complete filepath of file in directory
            file_path = os.path.join(folder_name, filename)
            # Add file to zip
            zip_file.write(file_path)


# Create a new zip file
zip_file = zipfile.ZipFile('../service.zip', 'w')

# Zip the directory
zip_directory('../service/', zip_file)

# Close the zip file
zip_file.close()
