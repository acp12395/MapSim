class DataBase():
    _crossingData = {}

    def __init__(self):
        pass
    
    @property
    def size(self):
        return len(self._crossingData)
    
    @property
    def data(self):
        return self._crossingData
    
    def initialize(self, start):
        #                    {"CrossingName" : [complex(coordinateX,coordinateY), {"NeighborCrossingName" : [distance, "StreetName"]}]}
        self._crossingData = {start : [complex(0,0), dict({})]}
        #                        {coordinates : [[[neighborCoordinates,"NeighborCrossingName"]],[[NonAccessibleNeighborCoordinates,"NonAccessibleNeighborCrossingName"]]]}
        self._neighborNodeData = {complex(0,0) : [[],[]]}

    def addRoad(self,fromCrossing,toCrossing,toCoords,distance, twoWay, roadName):
        self._crossingData[fromCrossing][1][toCrossing] = [distance, roadName]
        if twoWay:
            self._crossingData[toCrossing] = [toCoords, {fromCrossing : [distance,roadName]}]
        else:
            self._crossingData[toCrossing] = [toCoords, dict({})]

    def getCoordinates(self, crossing):
        retVal = None
        if crossing in self._crossingData:
            retVal = self._crossingData[crossing][0]
        return retVal