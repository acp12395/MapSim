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
        if self._dataBase.size == 0:
            self._dataBase.initialize(fromCrossing)
        fromCoordinates = self._dataBase.getCoordinates(fromCrossing)
        toCoordinates = self._geometricCalculator.rotate(fromCoordinates,fromCoordinates+complex(distance,0),self._positionMgr.angle + degrees)
        streetName = self._getStreetName(fromCrossing, toCrossing)
        self._dataBase.addRoad(fromCrossing,toCrossing,toCoordinates,distance, twoWay,streetName)
        self._mapScreen.drawRoad(fromCoordinates, toCoordinates)
        self._positionMgr.setPosition(toCoordinates, degrees)
        self._mapScreen.refresh()
    
    def _getStreetName(self, fromCrossing, toCrossing):
        fromSet = self._strProcessor.getWords(fromCrossing)
        toSet = self._strProcessor.getWords(toCrossing)
        return (fromSet & toSet).pop()
    
    def moveLeftMap(self):
        self._mapScreen.moveLeft()
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()

    def moveRightMap(self):
        self._mapScreen.moveRight()
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()

    def moveUpMap(self):
        self._mapScreen.moveUp()
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()
    
    def moveUpLeftMap(self):
        self._mapScreen.moveUpLeft()
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()
    
    def moveUpRightMap(self):
        self._mapScreen.moveUpRight()
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()

    def moveDownMap(self):
        self._mapScreen.moveDown()
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()
    
    def moveDownLeftMap(self):
        self._mapScreen.moveDownLeft()
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()
    
    def moveDownRightMap(self):
        self._mapScreen.moveDownRight()
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()
    
    def _drawMapScreenFromScratch(self):
        self._mapScreen.clear()
        for node in self._dataBase.data.values():
            fromCoord = node[0]
            self._mapScreen.drawCircle(fromCoord)
            for neighbor in node[1]:
                toCoord = self._dataBase.data[neighbor][0]
                self._mapScreen.drawRoad(fromCoord,toCoord)
        self._positionMgr.drawCurrentPosition()