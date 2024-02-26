def sum_of_lower_and_upper(string):
    count_lower = 0
    count_upper = 0
    for i in range(len(string)):
        if string[i].islower():
            count_lower += 1
        elif string[i].isupper():
            count_upper += 1
    
    return count_upper, count_lower

x = str(input())
print(sum_of_lower_and_upper(x))
