# for each cbz file in the directory, resize all images to 50% of their original size
import os
import glob
import zipfile
from PIL import Image

def zip_files(directory, zip_name):
    # Create a ZipFile object
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        # Iterate over all the files in the directory
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith('.cbz'):
                    continue
                # Create the complete filepath of the file in the directory
                file_path = os.path.join(foldername, filename)
                # Add file to zip
                zipf.write(file_path, os.path.relpath(file_path, directory))

def resize_image(name):
    img = Image.open(name)
    img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)), Image.LANCZOS)
    img.save(name)

def get_all_jpg_files_recursively(directory):
    jpg_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.jpg'):
                jpg_files.append(os.path.join(root, file))
    return jpg_files

directory = 'c:\\temp\\comics\\'
os.chdir(directory)
cbz_files = glob.glob('*.cbz')
# for each cbz file
for cbz_file in cbz_files:
    print(f'Processing {cbz_file}')
    temp_dir_name = cbz_file[:-4]
    # unpack the cbz file
    with zipfile.ZipFile(cbz_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir_name)
    os.chdir(temp_dir_name)
    # resize all images in the directory
    for img_file in get_all_jpg_files_recursively('.'):
        resize_image(img_file)
    # repack the directory, rename into cbz
    zip_files('.', cbz_file)
    # delete the original cbz
    os.remove(directory + cbz_file)
    # move cbz back to the original directory
    os.rename(cbz_file, directory + cbz_file)
    os.chdir(directory)
    # delete the directory
    os.system('rmdir /s /q ' + temp_dir_name)
