def histogram(list):
    for x in list:
        for j in range(x):
            print("*", end="")
        print()

hist = [int(x) for x in input().split()]
histogram(hist)
