import math
class Point:
    def __init__(self, ox, oy, oz):
        self.ox = ox
        self.oy = oy
        self.oz = oz
    def show(self):
        print("Ox:", self.ox, "Oy:", self.oy, "Oz:", self.oz)
    def change(self, newx, newy, newz):
        self.ox = newx
        self.oy = newy
        self.oz = newz
    def dist(self, new_point):
        print(math.sqrt((new_point.ox - self.ox)**2 + (new_point.oy - self.oy)**2 + (new_point.oz - self.oz)**2))
    
p1 = Point(1,2,3)
p2 = Point(4,5,6)

p1.show()
p1.change(7,8,9)
p1.show()
p1.dist(p2)

