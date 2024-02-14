import re 

def spacesCapital(my_string):
    x = re.sub("(.)([A-Z])", r"\1 \2", my_string)
    return x

example = "HelloWorldNewSome"
print(spacesCapital(example))