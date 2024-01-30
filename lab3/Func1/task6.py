def reverseSen(string):
    x = string.split()[::-1]
    print(" ".join(x))

inp = str(input())
reverseSen(inp)