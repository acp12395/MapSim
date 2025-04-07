from .StringProcessor import StringProcessor
from .GeometricCalculator import GeometricCalculator

class Coordinator():
    _strProcessor = None
    _dataBase = None
    _mapScreen = None
    _geometricCalculator = None
    _positionMgr = None

    def __init__(self,dataBase, mapScreen, positionMgr):
        self._dataBase = dataBase
        self._mapScreen = mapScreen
        self._geometricCalculator = GeometricCalculator()
        self._positionMgr = positionMgr
        self._strProcessor = StringProcessor()
    
    def requestAddRoad(self,fromCrossing,toCrossing,distance,degrees,leftRight,twoWay):
        fromCrossing = self._strProcessor.prettyString(fromCrossing)
        toCrossing = self._strProcessor.prettyString(toCrossing)
        if leftRight == "Right":
            degrees = -1 * degrees
        if self._dataBase.size == 1:
            self._dataBase.initialize(fromCrossing)
        fromCoordinates = self._dataBase.getCoordinates(fromCrossing)
        toCoordinates = self._geometricCalculator.rotate(fromCoordinates,distance,self._positionMgr.angle + degrees)
        streetName = self._getStreetName(fromCrossing, toCrossing)
        self._dataBase.addRoad(fromCrossing,toCrossing,toCoordinates,distance, twoWay,streetName)
        self._mapScreen.drawRoad(fromCoordinates, toCoordinates)
        self._positionMgr.setPosition(toCoordinates[0], toCoordinates[1], degrees)
    
    def _getStreetName(self, fromCrossing, toCrossing):
        fromSet = self._strProcessor.getWords(fromCrossing)
        toSet = self._strProcessor.getWords(toCrossing)
        return (fromSet & toSet).pop()