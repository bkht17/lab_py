def has_33(list):
    if ([3, 3] in [list[i:i+2] for i in range(len(list) - 1)]):
        return True
    else:
        return False


print(has_33([1, 3, 3]))
has_33([1, 3, 1, 3]) 
has_33([3, 1, 3]) 
