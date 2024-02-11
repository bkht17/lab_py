import math

def to_radians(degrees):
    print("Output radian:", round((degrees * math.pi/180), 6))

to_radians(float(input("Input degree: ")))