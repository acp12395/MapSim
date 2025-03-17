import tkinter as tk

class DataBase():
    _data = None
    def __init__(self):
        pass

class MapScreen():
    _mapScreen = None
    _dataBase = None
    _windowHandle = None
    def __init__(self, windowHandle, dataBase):
        self._windowHandle = windowHandle
        mapScreenHeight = self._windowHandle.winfo_height() - 25*2
        self._mapScreen = tk.Canvas(windowHandle, background="black",height=mapScreenHeight,width=500)
        self._mapScreen.place(x=475,y=25)
        self._mapScreen.create_line((50, 50), (100, 100), width=2, fill='white')
        self._dataBase = dataBase

class HMI():
    _margin = 25

    def __init__(self, windowHandle,dataBase):
        self._windowHandle = windowHandle
        self._dataBase = dataBase
        self.drawMapControl()

    def drawMapControl(self):
        self._mapActionsWidth = 107
        self._mapActionsFrame = tk.Frame(self._windowHandle,width=self._mapActionsWidth,bg="lightgray")
        self._mapActionsFrame.place(x=self._margin,y=self._margin, relheight= 1 -(2*self._margin/self._windowHandle.winfo_height()))

        moveFrameHeight = 95
        self._moveMapFrame = tk.Frame(self._mapActionsFrame, width=self._mapActionsWidth, height=moveFrameHeight,bg="lightgray")
        self._moveMapFrame.place(x=0,y=0)
        labelMoveMap = tk.Label(self._moveMapFrame,text="Move map",bg="lightgray")
        labelMoveMap.place(x=23,y=0)
        self._buttonUp = tk.Button(self._moveMapFrame,text="U")
        self._buttonUp.place(x=45,y=25)
        self._buttonLeft = tk.Button(self._moveMapFrame,text="L")
        self._buttonLeft.place(x=20,y=45)
        self._buttonRight = tk.Button(self._moveMapFrame,text="R")
        self._buttonRight.place(x=70,y=45)
        self._buttonDown = tk.Button(self._moveMapFrame,text="D")
        self._buttonDown.place(x=45,y=65)

        rotateFrameHeight = 70
        rotateMapFrame = tk.Frame(self._mapActionsFrame, width=self._mapActionsWidth, height=rotateFrameHeight,bg="lightgray")
        rotateMapFrame.place(x=0,y=moveFrameHeight)
        labelRotateMap = tk.Label(rotateMapFrame,text="Rotate map",bg="lightgray")
        labelRotateMap.place(x=21,y=0)
        self._buttonRotateLeft1 = tk.Button(rotateMapFrame,text="|\nv",command=self._onClickRotateLeft)
        self._buttonRotateLeft1.place(x=10,y=25)
        self._buttonRotateLeft2 = tk.Button(rotateMapFrame,text="<-",command=self._onClickRotateLeft)
        self._buttonRotateLeft2.place(x=25,y=25)
        self._buttonRotateRight1 = tk.Button(rotateMapFrame,text="->",command=self._onClickRotateRight)
        self._buttonRotateRight1.place(x=60,y=25)
        self._buttonRotateRight2 = tk.Button(rotateMapFrame,text="|\nv",command=self._onClickRotateRight)
        self._buttonRotateRight2.place(x=82,y=25)

        zoomFrameHeight = 95
        zoomFrame = tk.Frame(self._mapActionsFrame, width=self._mapActionsWidth, height=zoomFrameHeight,bg="lightgray")
        zoomFrame.place(x=0,y=moveFrameHeight+rotateFrameHeight)
        labelZoomMap = tk.Label(zoomFrame,text="Zoom",bg="lightgray")
        labelZoomMap.place(x=33,y=0)
        self._buttonZoomIn = tk.Button(zoomFrame,text="+")
        self._buttonZoomIn.place(x=44,y=25)
        self._buttonZoomOut = tk.Button(zoomFrame,text="-")
        self._buttonZoomOut.place(x=45,y=65)

    def adaptToWindowSize(self,event):
        self._mapActionsFrame.place(x=self._margin, y=self._margin,relheight=1 - (2*self._margin/event.height))

    def _onClickRotateLeft(self):
        self._buttonRotateLeft1.config(relief=tk.SUNKEN)
        self._buttonRotateLeft2.config(relief=tk.SUNKEN)
        self._windowHandle.update_idletasks()
        self._windowHandle.after(100)
        self._buttonRotateLeft1.config(relief=tk.RAISED)
        self._buttonRotateLeft2.config(relief=tk.RAISED)
        self._windowHandle.update_idletasks()

    def _onClickRotateRight(self):
        self._buttonRotateRight1.config(relief=tk.SUNKEN)
        self._buttonRotateRight2.config(relief=tk.SUNKEN)
        self._windowHandle.update_idletasks()
        self._windowHandle.after(100)
        self._buttonRotateRight1.config(relief=tk.RAISED)
        self._buttonRotateRight2.config(relief=tk.RAISED)
        self._windowHandle.update_idletasks()
        
def on_resize(event):
    hmi.adaptToWindowSize(event)

window = tk.Tk()

window.title("Map simulation")
window.bind("<Configure>", on_resize)
window.geometry("1000x500")
window.minsize(330,330)
window.update_idletasks() # For the elements inside window to know window's size from the begining 

dataBase = DataBase()
hmi = HMI(window,dataBase)
mapScreen = MapScreen(window,dataBase)
window.update_idletasks()

def on_close():
    global running
    running = False

window.protocol("WM_DELETE_WINDOW", on_close)

running = True

while running:  # It won't still try to execute even after windows is closed
    window.update()