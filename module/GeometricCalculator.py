from math import sin
from math import cos
from math import pi
from math import sqrt
from cmath import phase

class GeometricCalculator():
    def __init__(self):
        pass
    
    def rotate(self, origin, point, angleDeg):
        mappedPoint = point - origin
        mappedPhaseDeg = phase(mappedPoint)*180/pi
        mappedMagnitude = self._magnitude(mappedPoint)
        newMappedPhaseDeg = (mappedPhaseDeg + angleDeg)%360
        newMappedPhaseRad = newMappedPhaseDeg*pi/180
        x = mappedMagnitude*cos(newMappedPhaseRad)
        y = mappedMagnitude*sin(newMappedPhaseRad)
        newPoint = complex(x, y)
        return newPoint + origin
    
    def hypotenuse(self, catA, catB):
        return int(sqrt(pow(catA,2) + pow(catB,2)))
    
    def distance(self, pointA, pointB):
        return self.hypotenuse(abs(pointA.real - pointB.real), abs(pointA.imag - pointB.imag))
    
    def _magnitude(self, point):
        return abs(point)