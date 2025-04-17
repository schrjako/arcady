import math

class Point:
    def __init__(self, x: float, y:float):
        self.x = x
        self.y = y

    @property
    def phi(self):
        return math.atan2(self.y, self.x)
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __mult__(self, other):
        return Point(self.x * other.x, self.y * other.y)
    
    def __div__(self, other):
        return Point(self.x / other.x, self.y / other.y)
    
class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2
        
        self.a = -(p1 - p2).y
        self.b = (p1 - p2).x
        self.c = -(self.a * p1.x + self.b * p1.y)
    
    def eval(self, point: Point):
        '''
        Returns positive number if the point is on the one side and negative number if on the other. Otherwise 0
        '''
        return self.a * point.x + self.b * point.y + self.c
    
    def intersection(self, line):
        ...