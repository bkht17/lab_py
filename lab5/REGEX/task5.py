import re

checker = "a.+b$"
x = re.search(checker, str(input()))
if x:
    print(True)
else:
    print(False)