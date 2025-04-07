class PositionManager():
    _coords = [0,0]
    _angle = 90
    _map = None

    def __init__(self, map):
        self._map = map
        self._drawCurrentPosition()

    @property
    def angle(self):
        return self._angle

    def _drawCurrentPosition(self):
        self._map.drawCircle(self._coords[0],self._coords[1])
        self._map.drawArrow(self._coords[0],self._coords[1],self._angle)
    
    def setPosition(self, x, y, angle):
        self._map.drawCircle(self._coords[0],self._coords[1])
        self._coords = [x,y]
        self._angle = self._angle + angle
        self._drawCurrentPosition()