from .GeometricCalculator import GeometricCalculator

class DataBase():
    _crossingData = {}
    _geometricCalc = GeometricCalculator()

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

        intermediateNodes = [self._crossingData[fromCrossing][0]]
        self._addIntermediateNodes(intermediateNodes,self._crossingData[fromCrossing][0], toCoords)
        intermediateNodes.append(toCoords)
        self._insertNodesToRoad(intermediateNodes,fromCrossing,toCrossing,twoWay)

        if not toCrossing in self._crossingData:
            if twoWay:
                self._crossingData[toCrossing] = [toCoords, {fromCrossing : [distance,roadName]}]
            else:
                self._crossingData[toCrossing] = [toCoords, dict({})]
        else:
            if twoWay:
                self._crossingData[toCrossing][1][fromCrossing] = [distance,roadName]

    def _insertNodesToRoad(self,nodes,fromCrossing,toCrossing,twoWay):
        for nodeIndex in range(0,len(nodes)):
            if not nodes[nodeIndex] in self._neighborNodeData:
                self._neighborNodeData[nodes[nodeIndex]] = [[],[]]
            if nodeIndex > 0:
                if twoWay:
                    self._neighborNodeData[nodes[nodeIndex]][0].append([nodes[nodeIndex - 1],fromCrossing])
                else:
                    self._neighborNodeData[nodes[nodeIndex]][1].append([nodes[nodeIndex - 1],fromCrossing])
            if nodeIndex < len(nodes) - 1:
                self._neighborNodeData[nodes[nodeIndex]][0].append([nodes[nodeIndex + 1],toCrossing])

    def _addIntermediateNodes(self,nodes,fromCoords, toCoords):
        distance = int(self._geometricCalc.distance(fromCoords,toCoords))
        angle = self._geometricCalc.getAngle(fromCoords, toCoords)
        if distance > 1:
            firstAndLastEdgesDistance = (distance%100)/2
            hundredMetersSegmentsCount = distance//100
            if firstAndLastEdgesDistance == 0:
                firstAndLastEdgesDistance = 50
                hundredMetersSegmentsCount = hundredMetersSegmentsCount - 1
            nodes.append(self._geometricCalc.rotate(fromCoords,fromCoords + firstAndLastEdgesDistance,angle))
            while hundredMetersSegmentsCount > 0:
                hundredMetersSegmentsCount = hundredMetersSegmentsCount - 1
                nodes.append(self._geometricCalc.rotate(nodes[len(nodes) - 1], nodes[len(nodes) - 1] + 100,angle))
        return nodes

    def getCoordinates(self, crossing):
        retVal = None
        if crossing in self._crossingData:
            retVal = self._crossingData[crossing][0]
        return retVal
    
    def getNeighborNodes(self,coords):
        return self._neighborNodeData[coords][0] + self._neighborNodeData[coords][1]