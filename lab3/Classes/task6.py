nums = [int(x) for x in input().split()]
is_prime = lambda num: all(num%i!=0 for i in range(2, num)) and num > 1 
new_nums = filter(is_prime, nums)
print(*new_nums)