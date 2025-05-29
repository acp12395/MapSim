from math import sin
from math import cos
from math import pi
from math import sqrt
from cmath import phase
from math import atan

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
        return sqrt(pow(catA,2) + pow(catB,2))
    
    def distance(self, pointA, pointB):
        return self.hypotenuse(abs(pointA.real - pointB.real), abs(pointA.imag - pointB.imag))
    
    def _magnitude(self, point):
        return abs(point)

    def getAngle(self,origin,point):
        point = point - origin
        origin = complex(0,0)
        try:
            angle = (atan(point.imag/point.real)*180/pi)%360
        except ZeroDivisionError:
            if point.imag > 0:
                angle = 90
            else:
                angle = 270
        if point.real < 0:
            retAngle = 180 + angle
        elif point.real > 0:
            retAngle = 0 + angle
        else:
            retAngle = angle
        return retAngle