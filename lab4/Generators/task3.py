def div_by_3and4(n):
    for x in range(n+1):
        if x%3 == 0 and x%4==0:
            yield x

for x in div_by_3and4(int(input())):
    print(x, end=" ")