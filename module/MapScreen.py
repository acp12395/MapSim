import tkinter as tk

from .Observer import Observer
from .GeometricCalculator import GeometricCalculator

class MapScreen(Observer):
    _geometricCalc = GeometricCalculator()
    _mapScreen = None
    _windowHandle = None
    _margin = 25
    _radius = 0
    _zoom = 1
    _degrees = 0
    _origin = [0,0]

    def __init__(self, windowMgr):
        self._windowHandle = windowMgr.windowHandle
        self._drawMapScreen()
        windowMgr.registerObserver(self)

    def update(self, data):
        if data == "window":
            self._adaptToWindowSize()

    def _adaptToWindowSize(self):
        self._mapScreen.place(relheight=1 - (2*self._margin/self._windowHandle.winfo_height()),relwidth=1 -((self._margin+332)/self._windowHandle.winfo_width()))
        if self._radius != 0:
            self._zoom = (self._geometricCalc.hypotenuse(self._mapScreen.winfo_width(), self._mapScreen.winfo_height())//2) / self._radius

    def _drawMapScreen(self):
        self._mapScreen = tk.Canvas(self._windowHandle, background="black")
        self._mapScreen.place(y=self._margin, x=317, relheight=1 -(2*self._margin/self._windowHandle.winfo_height()), relwidth=1 -((self._margin+332)/self._windowHandle.winfo_width()))

    def drawCircle(self,x,y):
        coord = self._mappedCoordinate(x,y)
        self._mapScreen.create_oval(coord[0]-10,coord[1]-10,coord[0]+10,coord[1]+10,fill="white")
    
    def _mappedCoordinate(self,x,y):
        return [self._mapScreen.winfo_width()//2 + (x - self._origin[0])*self._zoom, self._mapScreen.winfo_height()//2 + (y - self._origin[1])*self._zoom]
    
    def drawArrow(self,x,y,angle):
        coord = self._mappedCoordinate(x,y)
        dist = 8
        front = self._geometricCalc.rotate(coord, dist,angle)
        rearLeft = self._geometricCalc.rotate(coord, dist,angle-150)
        rearRight = self._geometricCalc.rotate(coord, dist,angle+150)
        vertices = [front[0],front[1],rearLeft[0],rearLeft[1],rearRight[0],rearRight[1]]
        self._mapScreen.create_polygon(vertices,fill="red")

    def drawRoad(self, fromCoordinates, toCoordinates):
        if self._radius == 0:
            self._radius = self._geometricCalc.distance(self._origin, toCoordinates) * 2
            self._zoom = (self._geometricCalc.hypotenuse(self._mapScreen.winfo_width(), self._mapScreen.winfo_height())//2) / self._radius
        fromCoords = self._mappedCoordinate(fromCoordinates[0],fromCoordinates[1])
        toCoords = self._mappedCoordinate(toCoordinates[0],toCoordinates[1])
        self._mapScreen.create_line(fromCoords[0],fromCoords[1],toCoords[0],toCoords[1],fill="white", width=2)