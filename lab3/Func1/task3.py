def solve(numheads, numlegs):
    rabbits = int((numlegs - 2*numheads)/2)
    chicken = int(numheads - rabbits)
    print("Number of chicken is " , chicken)
    print("Number of rabbits is " , rabbits) 

solve(35, 94)
