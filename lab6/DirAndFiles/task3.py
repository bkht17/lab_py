import os

def check_path(path):
    if os.path.exists(path):
        print(f"Path '{path}' exists.")
        print(os.path.basename(path) + "\n" + os.path.dirname(path))
    else:
        print(False)


check_path(input("Path: "))