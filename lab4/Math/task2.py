import math

def area_trapezoid(height, a, b):
    print("Expected Output:", ((a+b)/2 * height))

height = int(input("Height: "))
a = int(input("Base, first value: "))
b = int(input("Base, second value: "))
area_trapezoid(height,a,b)