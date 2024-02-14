import re

test_checker = "ab{2,3}" #or "ab{2,3}(?!b)"

if re.search(test_checker, str(input())):
    print(True)
else:
    print(False)