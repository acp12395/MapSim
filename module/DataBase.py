class DataBase():
    _data = None

    def __init__(self):
        #{"CrossingName" : [[coordinateX,coordinateY], {"NeighborCrossingName" : [distance, "StreetName"]}]}
        self._data = {"Start" : [[0,0], {"Start" : [0,"Start"]}]}
    
    @property
    def size(self):
        return len(self._data)
    
    def initialize(self, start):
        self._data.clear()
        self._data = {start : [[0,0], dict({})]}
    
    def addRoad(self,fromCrossing,toCrossing,toCoords,distance, twoWay, roadName):
        self._data[fromCrossing][1][toCrossing] = [distance, roadName]
        if twoWay:
            self._data[toCrossing] = [toCoords, {fromCrossing : [distance,roadName]}]
        else:
            self._data[toCrossing] = [toCoords, dict({})]

    def getCoordinates(self, crossing):
        return self._data[crossing][0]