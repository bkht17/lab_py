decreasing_gen = (x for x in range(int(input()), -1, -1))

for x in decreasing_gen:
    print(x,end=" ")