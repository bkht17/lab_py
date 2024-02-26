def write_list_to_file(file_path, data):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(str(item) + '\n')

data = [6,7,7,8,9]
file_path = "/Users/bakhyt17/Documents/python_projects/lab6/DirAndFiles/check.txt"

write_list_to_file(file_path, data)

