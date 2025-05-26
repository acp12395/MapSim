class DataBase():
    _data = {}

    def __init__(self):
        pass
    
    @property
    def size(self):
        return len(self._data)
    
    @property
    def data(self):
        return self._data
    
    def initialize(self, start):
        #            {"CrossingName" : [complex(coordinateX,coordinateY), {"NeighborCrossingName" : [distance, "StreetName"]}]}
        self._data = {start : [complex(0,0), dict({})]}

    def addRoad(self,fromCrossing,toCrossing,toCoords,distance, twoWay, roadName):
        self._data[fromCrossing][1][toCrossing] = [distance, roadName]
        if twoWay:
            self._data[toCrossing] = [toCoords, {fromCrossing : [distance,roadName]}]
        else:
            self._data[toCrossing] = [toCoords, dict({})]

    def getCoordinates(self, crossing):
        retVal = None
        if crossing in self.data:
            retVal = self._data[crossing][0]
        return retVal