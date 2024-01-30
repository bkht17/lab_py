class String:
    def __init__(self, string):
        self.string = string

    def getString(self):
        return self.string
    
    def printString(self):
        print(self.string.upper())

p1 = String(str(input()))
print(p1.getString())
p1.printString()
