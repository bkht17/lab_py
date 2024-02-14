import re

def toCamel(snake_string):
    def capitalize(match):
        return match.group(1).upper()

    camelString = re.sub('_([a-zA-Z])', capitalize, snake_string)
    return camelString


x = "hello_world_lol_lol"
print(toCamel(x))

