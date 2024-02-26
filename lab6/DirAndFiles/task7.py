def copy_file(path1, path2):
    with open(path1, "r") as file1:
        with open(path2, "w") as file2:
            file2.write(file1.read())


file1 = "/Users/bakhyt17/Documents/python_projects/lab6/DirAndFiles/files_for7/file1.txt"
file2 = "/Users/bakhyt17/Documents/python_projects/lab6/DirAndFiles/files_for7/file.txt"

copy_file(file1, file2)