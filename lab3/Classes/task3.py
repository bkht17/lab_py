class Shape:
    def __init__(self):
        self.area = 0
    def Print_area(self):
        print(self.area)

class Square(Shape):
        def __init__(self, length):
            self.length = length
            self.area = self.length * self.length

fig = Square(5)
fig.Print_area()

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.area = self.length*self.width
   
p1 = Rectangle(2, 5)
p1.Print_area()
