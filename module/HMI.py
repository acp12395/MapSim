import tkinter as tk

from .Observer import Observer

class HMI(Observer):
    _margin = 25
    _mapActionsWidth = 107
    _addRoadRouteCalcWidth = 185
    _windowHandle = None
    _dataBase = None
    _mapActionsFrame = None
    _addRoadFrame = None
    _calculateRouteFrame = None
    _buttonRotateLeft1 = None
    _buttonRotateLeft2 = None
    _buttonRotateRight1 = None
    _buttonRotateRight2 = None
    _addRoadFrame = None
    _from = None
    _degrees = None
    _leftRight = None
    _distance = None
    _to = None
    _twoWay = None
    _calculateRouteFrame = None

    def __init__(self, windowMgr,dataBase):
        self._windowHandle = windowMgr.windowHandle
        self._dataBase = dataBase
        self._drawMapControl()
        self._drawAddRoadControl()
        self._drawRouteCalculator()
        windowMgr.registerObserver(self)

    def _drawMapControl(self):
        self._mapActionsFrame = tk.Frame(self._windowHandle,width=self._mapActionsWidth,bg="lightgray",highlightbackground="black",highlightthickness=1)
        self._mapActionsFrame.place(x=self._margin,y=self._margin, relheight= 1 -(2*self._margin/self._windowHandle.winfo_height()))

        selectorFrameHeight = 80
        selectorFrame = tk.Frame(self._mapActionsFrame, width=self._mapActionsWidth-2, height=selectorFrameHeight,bg="lightgray")
        selectorFrame.place(x=0,y=0)
        self._currentPostionMap = tk.StringVar(value="CP")
        map = tk.Radiobutton(selectorFrame,text="Map",variable=self._currentPostionMap,value="Map", bg="lightgray")
        map.place(x=15, y=5)
        currentPosition = tk.Radiobutton(selectorFrame,text="Current\nPosition",variable=self._currentPostionMap,value="CP", bg="lightgray")
        currentPosition.place(x=15,y=30)

        moveFrameHeight = 115
        moveMapFrame = tk.Frame(self._mapActionsFrame, width=self._mapActionsWidth-2, height=moveFrameHeight,bg="lightgray")
        moveMapFrame.place(x=0,y=selectorFrameHeight)
        labelMoveMap = tk.Label(moveMapFrame,text="Move",bg="lightgray")
        labelMoveMap.place(x=34,y=0)
        buttonUpLeft = tk.Button(moveMapFrame,text=" ")
        buttonUpLeft.place(x=23,y=25)
        buttonUp = tk.Button(moveMapFrame,text="^")
        buttonUp.place(x=43,y=25)
        buttonUpRight = tk.Button(moveMapFrame,text=" ")
        buttonUpRight.place(x=68,y=25)
        buttonLeft = tk.Button(moveMapFrame,text="<")
        buttonLeft.place(x=23,y=55)
        buttonRight = tk.Button(moveMapFrame,text=">")
        buttonRight.place(x=63,y=55)
        buttonDownLeft = tk.Button(moveMapFrame,text=" ")
        buttonDownLeft.place(x=23,y=85)
        buttonDown = tk.Button(moveMapFrame,text="v")
        buttonDown.place(x=44,y=85)
        buttonDownRight = tk.Button(moveMapFrame,text=" ")
        buttonDownRight.place(x=68,y=85)

        rotateFrameHeight = 70
        rotateMapFrame = tk.Frame(self._mapActionsFrame, width=self._mapActionsWidth-2, height=rotateFrameHeight,bg="lightgray")
        rotateMapFrame.place(x=0,y=moveFrameHeight+selectorFrameHeight)
        labelRotateMap = tk.Label(rotateMapFrame,text="Rotate",bg="lightgray")
        labelRotateMap.place(x=31,y=0)
        self._buttonRotateLeft1 = tk.Button(rotateMapFrame,text="|\nv",command=self._onClickRotateLeft)
        self._buttonRotateLeft1.place(x=10,y=25)
        self._buttonRotateLeft2 = tk.Button(rotateMapFrame,text="<-",command=self._onClickRotateLeft)
        self._buttonRotateLeft2.place(x=25,y=25)
        self._buttonRotateRight1 = tk.Button(rotateMapFrame,text="->",command=self._onClickRotateRight)
        self._buttonRotateRight1.place(x=60,y=25)
        self._buttonRotateRight2 = tk.Button(rotateMapFrame,text="|\nv",command=self._onClickRotateRight)
        self._buttonRotateRight2.place(x=82,y=25)

        zoomFrameHeight = 95
        zoomFrame = tk.Frame(self._mapActionsFrame, width=self._mapActionsWidth-2, height=zoomFrameHeight,bg="lightgray")
        zoomFrame.place(x=0,rely=0.7)
        labelZoomMap = tk.Label(zoomFrame,text="Zoom",bg="lightgray")
        labelZoomMap.place(x=33,y=0)
        buttonZoomIn = tk.Button(zoomFrame,text="+")
        buttonZoomIn.place(x=44,y=25)
        buttonZoomOut = tk.Button(zoomFrame,text="-")
        buttonZoomOut.place(x=45,y=65)

    def _drawAddRoadControl(self):
        self._addRoadFrame = tk.Frame(self._windowHandle,width=185,bg="lightgray",highlightbackground="black",highlightthickness=1)
        self._addRoadFrame.place(x=self._margin + self._mapActionsWidth,y=self._margin, relheight= (250/400)*(1 -((2*self._margin)/self._windowHandle.winfo_height())))

        labelFrom = tk.Label(self._addRoadFrame,bg="lightgray", text="From crossing*:")
        labelFrom.place(relx=0.28,y=3)
        self._from = tk.StringVar()
        inputFrom = tk.Entry(self._addRoadFrame, width=23,textvariable=self._from)
        inputFrom.place(relx=0.11, y=23)
        labelTurn = tk.Label(self._addRoadFrame,bg="lightgray",text="Turn approx. ")
        labelTurn.place(x=18,y=48)
        self._degrees = tk.IntVar()
        inputDegrees = tk.Entry(self._addRoadFrame, width=3,textvariable=self._degrees,justify="right")
        inputDegrees.place(x=93, y=48)
        labelDegrees = tk.Label(self._addRoadFrame,bg="lightgray",text="° to the")
        labelDegrees.place(x=115,y=48)
        self._leftRight = tk.StringVar()
        left = tk.Radiobutton(self._addRoadFrame,text="Left",variable=self._leftRight,value="Left", bg="lightgray")
        left.place(x=30,y=73)
        right = tk.Radiobutton(self._addRoadFrame,text="Right",variable=self._leftRight,value="Right", bg="lightgray")
        right.place(x=100, y=73)
        labelDistance = tk.Label(self._addRoadFrame,bg="lightgray", text="Distance:")
        labelDistance.place(x=35,y=98)
        self._distance = tk.IntVar()
        inputDistance = tk.Entry(self._addRoadFrame, width=5,textvariable=self._distance,justify="right")
        inputDistance.place(x=90, y=98)
        labelMeters = tk.Label(self._addRoadFrame,bg="lightgray", text="m")
        labelMeters.place(x=122,y=98)
        labelTo = tk.Label(self._addRoadFrame,bg="lightgray", text="To crossing*:")
        labelTo.place(x=55,y=123)
        self._to = tk.StringVar()
        inputTo = tk.Entry(self._addRoadFrame, width=23,textvariable=self._to)
        inputTo.place(relx=0.11, y=143)
        labelSeparatedComma = tk.Label(self._addRoadFrame,bg="lightgray",text="* Add streets separated by commas", font=("Yu Gothic UI",7))
        labelSeparatedComma.place(x=17,y=173)
        self._twoWay = tk.BooleanVar()
        twoWayCheck = tk.Checkbutton(self._addRoadFrame,bg="lightgray", text="Two-Way Road?",variable=self._twoWay,onvalue=True,offvalue=False)
        twoWayCheck.place(x=40, y=188)
        buttonAddRoad = tk.Button(self._addRoadFrame,text="Add road")
        buttonAddRoad.place(relx=0.35,y=215)

    def _drawRouteCalculator(self):
        self._calculateRouteFrame = tk.Frame(self._windowHandle,width=185,bg="lightgray",highlightbackground="black",highlightthickness=1)
        self._calculateRouteFrame.place(x=self._margin + self._mapActionsWidth,rely= 25/self._windowHandle.winfo_height()+(250/400)*(1 -(2*self._margin/self._windowHandle.winfo_height())), relheight= (150/400)*(1 -(2*self._margin/self._windowHandle.winfo_height())))
        self._pedestrianAuto = tk.StringVar(value="Auto")
        pedestrian = tk.Radiobutton(self._calculateRouteFrame,text="Pedestrian",variable=self._pedestrianAuto,value="Pedestrian", bg="lightgray")
        pedestrian.place(x=20, y=10)
        auto = tk.Radiobutton(self._calculateRouteFrame,text="Auto",variable=self._pedestrianAuto,value="Auto", bg="lightgray")
        auto.place(x=110,y=10)
        buttonOrigin = tk.Button(self._calculateRouteFrame,text="Set origin", width=15)
        buttonOrigin.place(x=35,y=40)
        buttonDestination = tk.Button(self._calculateRouteFrame,text="Set destination", width=15)
        buttonDestination.place(x=35,y=70)
        buttonRoute = tk.Button(self._calculateRouteFrame,text="Calculate route",width=15)
        buttonRoute.place(x=35,y=100)

    def update(self, data):
        if data == "window":
            self._adaptToWindowSize()

    def _adaptToWindowSize(self):
        self._mapActionsFrame.place(relheight=1 - (2*self._margin/self._windowHandle.winfo_height()))
        self._addRoadFrame.place(relheight= (250/400)*(1 -(2*self._margin/self._windowHandle.winfo_height())))
        self._calculateRouteFrame.place(rely= 25/self._windowHandle.winfo_height()+(250/400)*(1 -(2*self._margin/self._windowHandle.winfo_height())), relheight= (150/400)*(1 -(2*self._margin/self._windowHandle.winfo_height())))

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