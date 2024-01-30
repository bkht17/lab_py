def is_palindrom(string):
    bool = False
    for x in range(len(string) - 1):
        if string[x] != string[len(string) - x - 1]:
            return False
            break
        else:
            bool = True
    
    return bool

print(is_palindrom(str(input())))
            
    


