import tkinter as tk
from PIL import ImageTk, Image, ImageDraw

from .Observer import Observer
from .GeometricCalculator import GeometricCalculator

class MapScreen(Observer):
    _geometricCalc = GeometricCalculator()
    _imgTop = None
    _windowHandle = None
    _margin = 25
    _radius = 0
    _degrees = 0
    _coordsBottom = complex(0,0)
    _rotationDegrees = 0
    _imgBottomZoom = 1.0

    def __init__(self, windowMgr):
        self._windowHandle = windowMgr.windowHandle
        self._makeImageTop()
        self._makeImgBottom()
        self._adaptImgTopToZoom()
        self._displayUpdatedImg()
        windowMgr.registerObserver(self)
    
    def _makeImageTop(self):
        self._imgTop = tk.Canvas(self._windowHandle, background="black")
        self._imgTopZoom = 1.0
        self._imgTop.place(y=self._margin, x=317, relheight=1 -(2*self._margin/self._windowHandle.winfo_height()), relwidth=1 -((self._margin+332)/self._windowHandle.winfo_width()))
        self._windowHandle.update()
        self._imgTopOffset_X = -self._imgTop.winfo_width()
        self._imgTopOffset_Y = -self._imgTop.winfo_height()
    
    def _makeImgBottom(self):
        self._imgBottom = Image.new("RGB",(self._imgTop.winfo_width() * 3, self._imgTop.winfo_height() * 3), "black")
        self._imgBottomDraw = ImageDraw.Draw(self._imgBottom)
        self._zoomAdaptedImg = ImageTk.PhotoImage(self._imgBottom)
    
    def _adaptImgTopToZoom(self):
        newImg = self._imgBottom.resize(
            (int(self._imgBottom.width * self._imgTopZoom),
             int(self._imgBottom.height * self._imgTopZoom)),
            Image.LANCZOS
        )
        self._zoomAdaptedImg = ImageTk.PhotoImage(newImg)
    
    def _displayUpdatedImg(self):
        # Delete previous image
        self._imgTop.delete("all")
        self._imgTop.create_image(self._imgTopOffset_X, self._imgTopOffset_Y, anchor=tk.NW, image=self._zoomAdaptedImg)
        self._imgTop.update()

    def _copyBottomToTop(self):
        self._adaptImgTopToZoom()

    def update(self, data):
        if data == "window":
            self._adaptToWindowSize()

    def _adaptToWindowSize(self):
        self._imgTop.place(relheight=1 - (2*self._margin/self._windowHandle.winfo_height()),relwidth=1 -((self._margin+332)/self._windowHandle.winfo_width()))
        if self._radius != 0:
            self._imgBottomZoom = (self._geometricCalc.hypotenuse(self._imgTop.winfo_width(), self._imgTop.winfo_height())//2) / self._radius

    def drawCircle(self,coord):
        mappedCoord = self._mappedCoordinate(coord)
        nonComplexCoord = [mappedCoord.real, mappedCoord.imag]
        self._imgBottomDraw.circle(nonComplexCoord,10,fill="white")
        self._copyBottomToTop()
        self._displayUpdatedImg()
    
    def _mappedCoordinate(self,coord):
        rotatedCoord = self._geometricCalc.rotate(self._coordsBottom,coord,self._rotationDegrees)
        retCoord = complex(self._imgBottom.width // 2 + ((rotatedCoord.real - self._coordsBottom.real)*self._imgBottomZoom)//1, self._imgBottom.height // 2 - ((rotatedCoord.imag - self._coordsBottom.imag)* self._imgBottomZoom)//1)
        return retCoord
    
    def drawArrow(self,coord,angle):
        mappedCoord = self._mappedCoordinate(coord)
        mappedVertex = mappedCoord + complex(8,0)
        front = self._geometricCalc.rotate(mappedCoord,mappedVertex,angle)
        rearLeft = self._geometricCalc.rotate(mappedCoord,mappedVertex,angle-150)
        rearRight = self._geometricCalc.rotate(mappedCoord,mappedVertex,angle+150)
        vertices = [front.real, 2*mappedCoord.imag - front.imag,rearLeft.real,2*mappedCoord.imag - rearLeft.imag,rearRight.real,2*mappedCoord.imag - rearRight.imag]
        self._imgBottomDraw.polygon(vertices,outline="red",fill="red")
        self._copyBottomToTop()
        self._displayUpdatedImg()

    def drawRoad(self, fromCoordinates, toCoordinates):
        if self._radius == 0:
            self._radius = self._geometricCalc.distance(complex(0,0), toCoordinates) * 2
            self._imgBottomZoom = (self._geometricCalc.hypotenuse(self._imgTop.winfo_width(), self._imgTop.winfo_height())//2) / self._radius
        fromCoords = self._mappedCoordinate(fromCoordinates)
        toCoords = self._mappedCoordinate(toCoordinates)
        vertices = [fromCoords.real,fromCoords.imag,toCoords.real,toCoords.imag]
        self._imgBottomDraw.line(vertices,fill="white", width=2)
        self._copyBottomToTop()
        self._displayUpdatedImg()