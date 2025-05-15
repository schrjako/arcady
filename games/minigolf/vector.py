import math
class Vector:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        
        
    @property
    def sqdist(self):
        return self.x*self.x+self.y*self.y
    
    @property
    def magnitude(self):
        return math.sqrt(self.sqdist)
    
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)

    def __mul__(self, scalar):
        if type(scalar)==type(self):
            return self.x*scalar.x+self.y*scalar.y
        return Vector(self.x*scalar, self.y*scalar)
    
    def __div__(self, scalar):
        return Vector(self.x/scalar, self.y/scalar)
    
    def __iadd__(self, other):
        self.x+=other.x
        self.y+=other.y
        return self
    
    def __isub__(self, other):
        self.x-=other.x
        self.y-=other.y
        return self
    
    def __imul__(self, scalar):
        self.x*=scalar
        self.y*=scalar
        return self
    
    def __idiv__(self, scalar):
        self.x/=scalar
        self.y/=scalar
        return self
    
    @property
    def normalized(self):
        if self.magnitude<1e-8:
            return self
        return self*(1/self.magnitude)
    
    def normalize(self):
        if self.magnitude>=1e-8:
            self/=self.magnitude
        return self
    
    @property
    def totuple(self):
        return (self.x, self.y)