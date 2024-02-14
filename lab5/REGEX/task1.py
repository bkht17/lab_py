import re

test_checker = "ab*"
if re.search(test_checker, str(input())):
    print(True)
else:
    print(False)