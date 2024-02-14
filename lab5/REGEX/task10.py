import re

def to_snake(my_string):
    x = re.sub("(.)([A-Z])", r"\1_\2", my_string)
    return x.lower()

example = "helloWorldLolSumn"
print(to_snake(example))