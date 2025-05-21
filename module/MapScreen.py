import tkinter as tk
from PIL import ImageTk, Image, ImageDraw
from time import sleep

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
        self.adaptToWindowSize()
    
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
            self.adaptToWindowSize()

    def adaptToWindowSize(self):
        self._imgTop.place(y=self._margin, x=317,relheight=1 - (2*self._margin/self._windowHandle.winfo_height()),relwidth=1 -((self._margin+332)/self._windowHandle.winfo_width()))
        self._windowHandle.update_idletasks()
        self._imgTopOffset_X = -self._imgTop.winfo_width()
        self._imgTopOffset_Y = -self._imgTop.winfo_height()
        if self._radius != 0:
            self._imgBottomZoom = (self._geometricCalc.hypotenuse(self._imgTop.winfo_width(), self._imgTop.winfo_height())//2) / self._radius


    def drawCircle(self,coord):
        mappedCoord = self._mappedCoordinate(coord)
        nonComplexCoord = [mappedCoord.real, mappedCoord.imag]
        self._imgBottomDraw.circle(nonComplexCoord,10,fill="white")
    
    def _mappedCoordinate(self,coord):
        rotatedCoord = self._geometricCalc.rotate(self._coordsBottom,coord,-self._rotationDegrees)
        retCoord = complex(self._imgBottom.width // 2 + ((rotatedCoord.real - self._coordsBottom.real)*self._imgBottomZoom)//1, self._imgBottom.height // 2 - ((rotatedCoord.imag - self._coordsBottom.imag)* self._imgBottomZoom)//1)
        return retCoord
    
    def drawArrow(self,coord,angle):
        mappedCoord = self._mappedCoordinate(coord)
        mappedVertex = mappedCoord + complex(8,0)
        front = self._geometricCalc.rotate(mappedCoord,mappedVertex,angle-self._rotationDegrees)
        rearLeft = self._geometricCalc.rotate(mappedCoord,mappedVertex,angle-150-self._rotationDegrees)
        rearRight = self._geometricCalc.rotate(mappedCoord,mappedVertex,angle+150-self._rotationDegrees)
        vertices = [front.real, 2*mappedCoord.imag - front.imag,rearLeft.real,2*mappedCoord.imag - rearLeft.imag,rearRight.real,2*mappedCoord.imag - rearRight.imag]
        self._imgBottomDraw.polygon(vertices,outline="red",fill="red")

    def drawRoad(self, fromCoordinates, toCoordinates):
        if self._radius == 0:
            self._radius = self._geometricCalc.distance(complex(0,0), toCoordinates) * 2
            self._imgBottomZoom = (self._geometricCalc.hypotenuse(self._imgTop.winfo_width(), self._imgTop.winfo_height())//2) / self._radius
            self._coordsBottom = self._coordsBottom/self._imgBottomZoom
        fromCoords = self._mappedCoordinate(fromCoordinates)
        toCoords = self._mappedCoordinate(toCoordinates)
        vertices = [fromCoords.real,fromCoords.imag,toCoords.real,toCoords.imag]
        self._imgBottomDraw.line(vertices,fill="white", width=2)
    
    def moveLeft(self, magnitude=10):
        for i in range(1,magnitude):
            sleep(0.015)
            self._scrollImgTop("L")
            self._displayUpdatedImg()
        self._imgTopOffset_X = -self._imgTop.winfo_width()
        moveCoordinate = complex(-100/self._imgBottomZoom,0)
        moveCoordinate = self._mappedMove(moveCoordinate)
        self._coordsBottom = complex(self._coordsBottom.real + moveCoordinate.real, self._coordsBottom.imag - moveCoordinate.imag)

    def moveRight(self, magnitude=10):
        for i in range(magnitude):
            sleep(0.015)
            self._scrollImgTop("R")
            self._displayUpdatedImg()
        self._imgTopOffset_X = -self._imgTop.winfo_width()
        moveCoordinate = complex(100/self._imgBottomZoom,0)
        moveCoordinate = self._mappedMove(moveCoordinate)
        self._coordsBottom = complex(self._coordsBottom.real + moveCoordinate.real, self._coordsBottom.imag - moveCoordinate.imag)

    def moveUp(self, magnitude=10):
        for i in range(magnitude):
            sleep(0.015)
            self._scrollImgTop("U")
            self._displayUpdatedImg()
        self._imgTopOffset_Y = -self._imgTop.winfo_height()
        moveCoordinate = complex(0,-100/self._imgBottomZoom)
        moveCoordinate = self._mappedMove(moveCoordinate)
        self._coordsBottom = complex(self._coordsBottom.real + moveCoordinate.real, self._coordsBottom.imag - moveCoordinate.imag)
    
    def moveUpLeft(self, magnitude=10):
        for i in range(magnitude):
            sleep(0.015)
            self._scrollImgTop("U_L")
            self._displayUpdatedImg()
        self._imgTopOffset_Y = -self._imgTop.winfo_height()
        self._imgTopOffset_X = -self._imgTop.winfo_width()
        moveCoordinate = complex(-70.71/self._imgBottomZoom,-70.71/self._imgBottomZoom)
        moveCoordinate = self._mappedMove(moveCoordinate)
        self._coordsBottom = complex(self._coordsBottom.real + moveCoordinate.real, self._coordsBottom.imag - moveCoordinate.imag)

    def moveUpRight(self, magnitude=10):
        for i in range(magnitude):
            sleep(0.015)
            self._scrollImgTop("U_R")
            self._displayUpdatedImg()
        self._imgTopOffset_Y = -self._imgTop.winfo_height()
        self._imgTopOffset_X = -self._imgTop.winfo_width()
        moveCoordinate = complex(70.71/self._imgBottomZoom,-70.71/self._imgBottomZoom)
        moveCoordinate = self._mappedMove(moveCoordinate)
        self._coordsBottom = complex(self._coordsBottom.real + moveCoordinate.real, self._coordsBottom.imag - moveCoordinate.imag)
    
    def moveDown(self, magnitude=10):
        for i in range(magnitude):
            sleep(0.015)
            self._scrollImgTop("D")
            self._displayUpdatedImg()
        self._imgTopOffset_Y = -self._imgTop.winfo_height()
        moveCoordinate = complex(0,100/self._imgBottomZoom)
        moveCoordinate = self._mappedMove(moveCoordinate)
        self._coordsBottom = complex(self._coordsBottom.real + moveCoordinate.real, self._coordsBottom.imag - moveCoordinate.imag)

    def moveDownLeft(self, magnitude=10):
        for i in range(magnitude):
            sleep(0.015)
            self._scrollImgTop("D_L")
            self._displayUpdatedImg()
        self._imgTopOffset_Y = -self._imgTop.winfo_height()
        self._imgTopOffset_X = -self._imgTop.winfo_width()
        moveCoordinate = complex(-70.71/self._imgBottomZoom,70.71/self._imgBottomZoom)
        moveCoordinate = self._mappedMove(moveCoordinate)
        self._coordsBottom = complex(self._coordsBottom.real + moveCoordinate.real, self._coordsBottom.imag - moveCoordinate.imag)

    def moveDownRight(self, magnitude=10):
        for i in range(magnitude):
            sleep(0.015)
            self._scrollImgTop("D_R")
            self._displayUpdatedImg()
        self._imgTopOffset_Y = -self._imgTop.winfo_height()
        self._imgTopOffset_X = -self._imgTop.winfo_width()
        moveCoordinate = complex(70.71/self._imgBottomZoom,70.71/self._imgBottomZoom)
        moveCoordinate = self._mappedMove(moveCoordinate)
        self._coordsBottom = complex(self._coordsBottom.real + moveCoordinate.real, self._coordsBottom.imag - moveCoordinate.imag)
    
    def _mappedMove(self, movingVectorRectangular):
        mappedOrigin = complex(0,0)
        movingVectorRectangular = self._geometricCalc.rotate(mappedOrigin,movingVectorRectangular,-self._rotationDegrees)
        return movingVectorRectangular
    
    def _scrollImgTop(self, dir):
        if dir == "L":
            dx = 10
            self._imgTopOffset_X += dx
        elif dir == "R":
            dx = -10
            self._imgTopOffset_X += dx
        elif dir == "U":
            dy = 10
            self._imgTopOffset_Y += dy
        elif dir == "U_L":
            dx = 7.071
            self._imgTopOffset_X += dx
            dy = 7.071
            self._imgTopOffset_Y += dy
        elif dir == "U_R":
            dx = -7.071
            self._imgTopOffset_X += dx
            dy = 7.071
            self._imgTopOffset_Y += dy
        elif dir == "D":
            dy = -10
            self._imgTopOffset_Y += dy
        elif dir == "D_L":
            dx = 7.071
            self._imgTopOffset_X += dx
            dy = -7.071
            self._imgTopOffset_Y += dy
        elif dir == "D_R":
            dx = -7.071
            self._imgTopOffset_X += dx
            dy = -7.071
            self._imgTopOffset_Y += dy
    
    def refresh(self):
        self._copyBottomToTop()
        self._displayUpdatedImg()
    
    def clear(self):
        self._makeImgBottom()
        self._adaptImgTopToZoom()

    def rotateLeft(self, magnitude):
        imgCopy = self._imgBottom.copy()
        numericMagnitude = magnitude
        if magnitude == "Quick":
            numericMagnitude = 45
            for i in range(1,numericMagnitude,2):
                self._zoomAdaptedImg = ImageTk.PhotoImage(imgCopy.rotate(i))
                self._displayUpdatedImg()
        self._zoomAdaptedImg = ImageTk.PhotoImage(imgCopy.rotate(numericMagnitude))
        self._displayUpdatedImg()

    def stopLeftRotation(self, magnitude):
        self._rotationDegrees = (self._rotationDegrees - magnitude)%360

    def rotateRight(self, magnitude):
        imgCopy = self._imgBottom.copy()
        numericMagnitude = magnitude
        if magnitude == "Quick":
            numericMagnitude = 45
            for i in range(1,numericMagnitude,2):
                self._zoomAdaptedImg = ImageTk.PhotoImage(imgCopy.rotate(-i))
                self._displayUpdatedImg()
        self._zoomAdaptedImg = ImageTk.PhotoImage(imgCopy.rotate(-numericMagnitude))
        self._displayUpdatedImg()

    def stopRightRotation(self, magnitude):
        self._rotationDegrees = (self._rotationDegrees + magnitude)%360

    def zoomIn(self, magnitude=2):
        magnitude *= self._imgTopZoom
        while self._imgTopZoom * 1.07 < magnitude:
            self._imgTopZoom *= 1.07
            self._adaptImgTopToZoom()
            self._imgTopOffset_X = -(self._zoomAdaptedImg.width()-self._imgTop.winfo_width())/2
            self._imgTopOffset_Y = -(self._zoomAdaptedImg.height()-self._imgTop.winfo_height())/2
            self._displayUpdatedImg()
        self._imgTopZoom = magnitude
        self._adaptImgTopToZoom()
        self._imgTopOffset_X = -(self._zoomAdaptedImg.width()-self._imgTop.winfo_width())/2
        self._imgTopOffset_Y = -(self._zoomAdaptedImg.height()-self._imgTop.winfo_height())/2
        self._displayUpdatedImg()
        self._imgTopOffset_X = -self._imgTop.winfo_width()
        self._imgTopOffset_Y = -self._imgTop.winfo_height()
        self._imgBottomZoom *= self._imgTopZoom
        self._imgTopZoom = 1.0
        
    def zoomOut(self, magnitude=0.5):
        magnitude *= self._imgTopZoom
        while self._imgTopZoom * 0.97 > magnitude:
            sleep(0.01)
            self._imgTopZoom *= 0.97
            self._adaptImgTopToZoom()
            self._imgTopOffset_X = -(self._zoomAdaptedImg.width()-self._imgTop.winfo_width())/2
            self._imgTopOffset_Y = -(self._zoomAdaptedImg.height()-self._imgTop.winfo_height())/2
            self._displayUpdatedImg()
        self._imgTopZoom = magnitude
        self._adaptImgTopToZoom()
        self._imgTopOffset_X = -(self._zoomAdaptedImg.width()-self._imgTop.winfo_width())/2
        self._imgTopOffset_Y = -(self._zoomAdaptedImg.height()-self._imgTop.winfo_height())/2
        self._displayUpdatedImg()
        self._imgTopOffset_X = -self._imgTop.winfo_width()
        self._imgTopOffset_Y = -self._imgTop.winfo_height()
        self._imgBottomZoom *= self._imgTopZoom
        self._imgTopZoom = 1.0