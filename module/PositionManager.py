class PositionManager():
    _coords = [0,0]
    _angle = None
    _map = None

    def __init__(self, map):
        self._map = map
        angle = 90
        self._drawCurrentPosition(0,0,angle)

    @property
    def angle(self):
        return self._angle

    def _drawCurrentPosition(self, x, y, angle):
        self._angle = angle
        self._map.drawCircle(x,y)
        self._map.drawArrow(x,y,self._angle)