import math

def area(n, length):
    print("The area of the polygon is:", round((n* length**2)/(4*math.tan(math.pi/n)),1))

n = int(input("Input number of sides:"))
length = int(input("Input the length of a side:"))

area(n,length)