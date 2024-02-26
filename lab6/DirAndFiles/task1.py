import os

def list_directories_files(path):
    directories = [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]
    print(directories,'\n')

    files = [item for item in os.listdir(path) if os.path.isfile(os.path.join(path, item))]
    print(files,'\n')

    print(directories + files)

path = "/Users/bakhyt17"
list_directories_files(path)
