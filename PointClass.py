import math


class point:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def distance(self, e):
        return math.sqrt((self.x - e.x)**2 + (self.y - e.y)**2)


    def equal(self, e):
        return self.x == e.x and self.y == e.y
