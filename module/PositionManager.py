class PositionManager():
    _coords = complex(0,0)
    _angle = 90
    _map = None

    def __init__(self, map):
        self._map = map
        self.drawCurrentPosition()
        self._map.refresh()

    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, value):
        self._angle = value

    @property
    def coords(self):
        return self._coords

    def drawCurrentPosition(self):
        self._map.drawCircle(self._coords)
        self._map.drawArrow(self._coords,self._angle)

    def setCoords(self,coord):
        self._coords = coord