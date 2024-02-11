# def squares(n):
#     for x in range(n+1):
#         yield x**2

# inp = int(input())
# for x in squares(inp):
#     print(x, end=" ")

squares = (x**2 for x in range(int(input())+1))

for x in squares:
    print(x, end=" ")


