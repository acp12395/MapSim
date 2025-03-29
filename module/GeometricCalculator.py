from math import sin
from math import cos
from math import pi

class GeometricCalculator():
    def __init__(self):
        pass
    
    def rotate(self, origin, distance, angle):
        coordinates = [int(origin[0] + distance*cos(angle*pi/180)), int(origin[1] - distance*sin(angle*pi/180))]
        return coordinates