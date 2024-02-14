import re

example = "Hell1NewTextExample"
checker = "[A-Z][^A-Z]*"
x = re.findall(checker, example)
print(x)