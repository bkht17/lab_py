import os

def delete_file(path):
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"File '{path}' has been deleted")
        except Exception as e:
            print(f"Error '{path}': {e}")
    else:
        print(f"File '{path}' does not exist")


file_path = "/Users/bakhyt17/Documents/python_projects/lab6/DirAndFiles/texts-docs/file-to-del.txt"
delete_file(file_path)