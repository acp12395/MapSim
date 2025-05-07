from math import sin
from math import cos
from math import pi
from math import sqrt

class GeometricCalculator():
    def __init__(self):
        pass
    
    def rotate(self, origin, distance, angle):
        coordinates = [origin[0] + distance*cos(angle*pi/180), origin[1] - distance*sin(angle*pi/180)]
        return coordinates
    
    def hypotenuse(self, catA, catB):
        return int(sqrt(pow(catA,2) + pow(catB,2)))
    
    def distance(self, pointA, pointB):
        return self.hypotenuse(abs(pointA[0] - pointB[0]), abs(pointA[1] - pointB[1]))