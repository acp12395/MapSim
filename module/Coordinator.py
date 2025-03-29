from .GeometricCalculator import GeometricCalculator

class Coordinator():
    _dataBase = None
    _mapScreen = None
    _geometricCalculator = None
    _positionMgr = None

    def __init__(self,dataBase, mapScreen, positionMgr):
        self._dataBase = dataBase
        self._mapScreen = mapScreen
        self._geometricCalculator = GeometricCalculator()
        self._positionMgr = positionMgr