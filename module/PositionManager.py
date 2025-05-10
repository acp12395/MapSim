class PositionManager():
    _coords = complex(0,0)
    _angle = 90
    _map = None

    def __init__(self, map):
        self._map = map
        self.drawCurrentPosition()

    @property
    def angle(self):
        return self._angle

    def drawCurrentPosition(self):
        self._map.drawCircle(self._coords)
        self._map.drawArrow(self._coords,self._angle)
        self._map.refresh()
    
    def setPosition(self, coord, angle):
        self._map.drawCircle(self._coords)
        self._coords = coord
        self._angle = self._angle + angle
        self.drawCurrentPosition()