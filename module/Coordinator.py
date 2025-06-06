from .StringProcessor import StringProcessor
from .GeometricCalculator import GeometricCalculator
from .Observer import Observer

class Coordinator(Observer):
    _strProcessor = None
    _dataBase = None
    _mapScreen = None
    _geometricCalculator = None
    _positionMgr = None
    _windowHandle = None
    _rotationDegree = 0
    _rotating = False

    def __init__(self,dataBase, mapScreen, positionMgr, windowMgr):
        self._dataBase = dataBase
        self._mapScreen = mapScreen
        self._geometricCalculator = GeometricCalculator()
        self._positionMgr = positionMgr
        self._strProcessor = StringProcessor()
        self._windowHandle = windowMgr.windowHandle
        windowMgr.registerObserver(self)
    
    def requestAddRoad(self,fromCrossing,toCrossing,distance,twoWay):
        fromCrossing = self._strProcessor.prettyString(fromCrossing)
        toCrossing = self._strProcessor.prettyString(toCrossing)
        if self._dataBase.size == 0:
            self._dataBase.initialize(fromCrossing)
        fromCoordinates = self._dataBase.getCoordinates(fromCrossing)
        toCoordinates = self._dataBase.getCoordinates(toCrossing)
        if toCoordinates == None:
            toCoordinates = self._geometricCalculator.rotate(fromCoordinates,fromCoordinates+complex(distance,0),self._positionMgr.angle)
        streetName = self._getStreetName(fromCrossing, toCrossing)
        self._dataBase.addRoad(fromCrossing,toCrossing,toCoordinates,distance, twoWay,streetName)
        self._positionMgr.setCoords(toCoordinates)
        self._drawMapScreenFromScratch()
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

    def _goToSuitableNode(self,neighbors,direction):
        if direction == "R":
            directionDegrees = 0
        elif direction == "U_R":
            directionDegrees = 45
        elif direction == "U":
            directionDegrees = 90
        elif direction == "U_L":
            directionDegrees = 135
        elif direction == "L":
            directionDegrees = 180
        elif direction == "D_L":
            directionDegrees = 225
        elif direction == "D":
            directionDegrees = 270
        elif direction == "D_R":
            directionDegrees = 315
        directionSuitableDegrees = (directionDegrees + self._mapScreen.rotationDegrees)%360
        for neighbor in neighbors:
            if self._geometricCalculator.getAngleDifference(directionSuitableDegrees,self._geometricCalculator.getAngle(self._positionMgr.coords,neighbor[0])) <= 23:
                self._positionMgr.setCoords(neighbor[0])
                break

    def moveLeftPosition(self):
        currentCoords = self._positionMgr.coords
        neighborNodes = self._dataBase.getNeighborNodes(currentCoords)
        self._goToSuitableNode(neighborNodes,"L")
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()

    def moveRightPosition(self):
        currentCoords = self._positionMgr.coords
        neighborNodes = self._dataBase.getNeighborNodes(currentCoords)
        self._goToSuitableNode(neighborNodes,"R")
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()

    def moveUpPosition(self):
        currentCoords = self._positionMgr.coords
        neighborNodes = self._dataBase.getNeighborNodes(currentCoords)
        self._goToSuitableNode(neighborNodes,"U")
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()

    def moveUpLeftPosition(self):
        currentCoords = self._positionMgr.coords
        neighborNodes = self._dataBase.getNeighborNodes(currentCoords)
        self._goToSuitableNode(neighborNodes,"U_L")
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()

    def moveUpRightPosition(self):
        currentCoords = self._positionMgr.coords
        neighborNodes = self._dataBase.getNeighborNodes(currentCoords)
        self._goToSuitableNode(neighborNodes,"U_R")
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()

    def moveDownPosition(self):
        currentCoords = self._positionMgr.coords
        neighborNodes = self._dataBase.getNeighborNodes(currentCoords)
        self._goToSuitableNode(neighborNodes,"D")
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()

    def moveDownLeftPosition(self):
        currentCoords = self._positionMgr.coords
        neighborNodes = self._dataBase.getNeighborNodes(currentCoords)
        self._goToSuitableNode(neighborNodes,"D_L")
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()

    def moveDownRightPosition(self):
        currentCoords = self._positionMgr.coords
        neighborNodes = self._dataBase.getNeighborNodes(currentCoords)
        self._goToSuitableNode(neighborNodes,"D_R")
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

    def rotateLeft_Map(self,mode):
        self._rotating = True
        if mode == "Long":
            self._keepRotatingLeft_Map()
        elif mode == "Quick":
            self._mapScreen.rotateLeft(mode)
            self._windowHandle.update_idletasks()
            self._rotationDegree = 45
            self.stopLeftRotation_Map()
    
    def _keepRotatingLeft_Map(self):
        if self._rotating:
            self._rotationDegree = self._rotationDegree + 3
            self._rotationDegree = self._rotationDegree%360
            self._mapScreen.rotateLeft(self._rotationDegree)
            self._windowHandle.update_idletasks()
            self._windowHandle.after(1,self._keepRotatingLeft_Map)
    
    def stopLeftRotation_Map(self):
        if self._rotating:
            self._rotating = False
            self._mapScreen.stopLeftRotation(self._rotationDegree)
            self._drawMapScreenFromScratch()
            self._mapScreen.refresh()
            self._rotationDegree = 0

    def rotateLeft_CP(self, mode):
        self._rotating = True
        if mode == "Long":
            self._keepRotatingLeft_CP()
        elif mode == "Quick":
            self._rotateLeft45Degrees_CP()

    def _keepRotatingLeft_CP(self):
        if self._rotating:
            self._positionMgr.angle = (self._positionMgr.angle + 1)%360
            self._positionMgr.drawCurrentPosition()
            self._mapScreen.refresh()
            self._windowHandle.update_idletasks()
            self._windowHandle.after(1,self._keepRotatingLeft_CP)
    
    def _rotateLeft45Degrees_CP(self):
        for i in range(0,45):
            self._positionMgr.angle = (self._positionMgr.angle + 1)%360
            self._positionMgr.drawCurrentPosition()
            self._mapScreen.refresh()
            self._windowHandle.update_idletasks()
    
    def rotateRight_Map(self,mode):
        self._rotating = True
        if mode == "Long":
            self._keepRotatingRight_Map()
        elif mode == "Quick":
            self._mapScreen.rotateRight(mode)
            self._windowHandle.update_idletasks()
            self._rotationDegree = 45
            self.stopRightRotation_Map()
    
    def _keepRotatingRight_Map(self):
        if self._rotating:
            self._rotationDegree = self._rotationDegree + 3
            self._rotationDegree = self._rotationDegree%360
            self._mapScreen.rotateRight(self._rotationDegree)
            self._windowHandle.update_idletasks()
            self._windowHandle.after(1,self._keepRotatingRight_Map)

    def stopRightRotation_Map(self):
        if self._rotating:
            self._rotating = False
            self._mapScreen.stopRightRotation(self._rotationDegree)
            self._drawMapScreenFromScratch()
            self._mapScreen.refresh()
            self._rotationDegree = 0

    def rotateRight_CP(self, mode):
        self._rotating = True
        if mode == "Long":
            self._keepRotatingRight_CP()
        elif mode == "Quick":
            self._rotateRight45Degrees_CP()

    def _keepRotatingRight_CP(self):
        if self._rotating:
            self._positionMgr.angle = (self._positionMgr.angle - 1)%360
            self._positionMgr.drawCurrentPosition()
            self._mapScreen.refresh()
            self._windowHandle.update_idletasks()
            self._windowHandle.after(1,self._keepRotatingRight_CP)
    
    def _rotateRight45Degrees_CP(self):
        for i in range(0,45):
            self._positionMgr.angle = (self._positionMgr.angle - 1)%360
            self._positionMgr.drawCurrentPosition()
            self._mapScreen.refresh()
            self._windowHandle.update_idletasks()

    def stopRotation_CP(self):
        if self._rotating:
            self._rotating = False

    def zoomInMap(self):
        self._mapScreen.zoomIn()
        self._mapScreen.adaptToWindowSize()
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()
    
    def zoomOutMap(self):
        self._mapScreen.zoomOut()
        self._mapScreen.adaptToWindowSize()
        self._drawMapScreenFromScratch()
        self._mapScreen.refresh()
    
    def update(self, data):
        if data == "window-finished":
            self._mapScreen.adaptToWindowSize("calculate-zoom")
            self._drawMapScreenFromScratch()
            self._mapScreen.refresh()