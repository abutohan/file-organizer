import json
from constants.constants import DIRECTORY_PATH_JSON
from classes.file_organizer import FileOrganizer

def get_directory(directory, key_name="directory_path"):
  with open(directory, 'r') as json_file:
    data = json.load(json_file)
    path = data[key_name]
    return path

def main():
  directory_path = get_directory(DIRECTORY_PATH_JSON)
  file_organizer = FileOrganizer(directory_path, DIRECTORY_PATH_JSON)
  file_organizer.run_process()

if __name__ == "__main__":
    main()