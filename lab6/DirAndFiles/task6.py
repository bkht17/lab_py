import string

for letter in string.ascii_uppercase:
    path = (
        "/Users/bakhyt17/Documents/python_projects/lab6/DirAndFiles/texts-docs/"
        + letter
        + ".txt"
    )
    with open(path, "w") as my_file:
        my_file.write("Hello".format(path))