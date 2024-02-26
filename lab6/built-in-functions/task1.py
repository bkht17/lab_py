def multiply_list(list):
    result = 1
    while len(list) != 0:
        x = list.pop()
        result *= x

    return result

nums = [int(x) for x in input().split()]
print(multiply_list(nums))