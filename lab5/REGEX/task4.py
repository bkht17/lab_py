import re

checker = "[A-Z][a-z]+"
x = re.findall(checker,str(input()))
print(x)