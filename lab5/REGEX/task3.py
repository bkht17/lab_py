import re

checker = "[a-z]+_[a-z]+$"
x = re.findall(checker, str(input()))
print(x)