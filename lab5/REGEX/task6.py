import re

checker = "[.,,, ]"
to_change = ":"
x = re.sub(checker,to_change,str(input()))
print(x)