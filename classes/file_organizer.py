import os
import json
import shutil
import hashlib

class FileOrganizer:
  def __init__(self, directory_folder, directory_json):
    self.directory_folder = directory_folder
    self.directory_json = directory_json
    self.file_types =[]

  def get_file_types(self):
    print("Getting all file types...")
    for file_name in os.listdir(self.directory_folder):
      file_path = os.path.join(self.directory_folder, file_name)
      if os.path.isfile(file_path):
        file_extension = os.path.splitext(file_name)[1][1:]
        if file_extension not in self.file_types:
          self.file_types.append(file_extension)
    print(f"File Types: {self.file_types}")

  def create_folders(self):
    for file_type in self.file_types:
      folder_name = os.path.join(self.directory_folder, file_type)
      os.makedirs(folder_name, exist_ok=True)
    print("Folders are created.")

  def move_files(self):
    print("Moving files...")
    for file_name in os.listdir(self.directory_folder):
      file_path = os.path.join(self.directory_folder, file_name)
      if os.path.isfile(file_path):
        file_extension = os.path.splitext(file_name)[1][1:]
        if file_extension:
            destination_folder = os.path.join(self.directory_folder, file_extension)
            shutil.move(file_path, destination_folder)
    print("Files are moved to their respective folders.")

  def remove_duplicate_files(self):
    file_checksums ={}
    duplicates = []
    for root, dirs, files in os.walk(self.directory_folder):
      for file_name in files:
        file_path = os.path.join(root, file_name)
        checksum = self.get_file_checksum(file_path)
        if checksum in file_checksums:
            duplicates.append(file_path)
        else:
            file_checksums[checksum] = file_path
    for duplicate in duplicates:
      os.remove(duplicate)
      print(f"Removed duplicate file: {duplicate}")
    print(f"Removed {len(duplicates)} duplicate files.")

  
  def get_file_checksum(self, file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
      for chunk in iter(lambda: file.read(4096), b''):
        hasher.update(chunk)
    return hasher.hexdigest()

  def rename_files(self):
    print("Renaming files...")
    for folder_name in os.listdir(self.directory_folder):
      folder_dir = os.path.join(self.directory_folder, folder_name)
      if os.path.isdir(folder_dir):
        for file_name in os.listdir(folder_dir):
          file_ext = os.path.splitext(file_name)[1]
          new_file_name = self.get_unique_filename(os.path.join(folder_dir, file_name))
          file_path = os.path.join(folder_dir, file_name)
          new_file_path = os.path.join(folder_dir, new_file_name)
          os.rename(file_path, new_file_path)
    print("Files are properly renamed.")

  def get_unique_filename(self, file_path):
    file_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
          file_hash.update(chunk)
    file_extension = os.path.splitext(file_path)[1]
    unique_filename = file_hash.hexdigest() + file_extension
    return unique_filename

  def update_json(self):
    with open(self.directory_json, 'r') as json_file:
      data = json.load(json_file)
      data['file_types'] = self.file_types

    with open(self.directory_json, 'w') as json_file:
      json.dump(data, json_file, indent=4)
    os.system('powershell -c (New-Object Media.SoundPlayer "C:\\Windows\\Media\\notify.wav").PlaySync()')
    print("Done.")

  def run_process(self):
    self.get_file_types()
    self.create_folders()
    self.move_files()
    self.remove_duplicate_files()
    self.rename_files()
    self.update_json()