import tkinter as tk

from .Observer import Observer

class HMI(Observer):
    _margin = 25
    _mapActionsWidth = 170
    _addRoadRouteCalcWidth = 185
    _windowHandle = None
    _coordinator = None
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
    _buttonPressed = False
    _buttonPressedFlavor = "Quick"
    _busy = False

    def __init__(self, windowMgr, coordinator):
        self._windowHandle = windowMgr.windowHandle
        self._coordinator = coordinator
        self._drawMapControl()
        self._drawAddRoadControl()
        self._drawRouteCalculator()
        windowMgr.registerObserver(self)

    def _drawMapControl(self):
        self._mapActionsFrame = tk.Frame(self._windowHandle,bg="lightgray",highlightbackground="black",highlightthickness=1)
        self._mapActionsFrame.place(x=self._margin,y=self._margin, relheight= 1 -(2*self._margin/self._windowHandle.winfo_height()), relwidth=(1-self._windowHandle.winfo_height()/self._windowHandle.winfo_width())*0.5)

        selectorFrameHeight = 60
        selectorFrame = tk.Frame(self._mapActionsFrame, width=self._mapActionsWidth, height=selectorFrameHeight,bg="lightgray")
        selectorFrame.place(relx=0.5,y=15,height=20,anchor="n")
        self._currentPostionMap = tk.StringVar(value="CP")
        map = tk.Radiobutton(selectorFrame,text="Map",variable=self._currentPostionMap,value="Map",bg="lightgray")
        map.place(x=0, y=0)
        currentPosition = tk.Radiobutton(selectorFrame,text="Current Position",variable=self._currentPostionMap,value="CP",bg="lightgray")
        currentPosition.place(x=60,y=0)

        moveFrameHeight = 135
        moveMapFrame = tk.Frame(self._mapActionsFrame, width=60, height=moveFrameHeight,bg="lightgray")
        moveMapFrame.place(relx=0.5,y=selectorFrameHeight,anchor="n")
        labelMoveMap = tk.Label(moveMapFrame,text="Move",bg="lightgray")
        labelMoveMap.place(relx=0.5,y=0,anchor="n")
        buttonUpLeft = tk.Button(moveMapFrame,text=" ",command=self._onClickMoveUpLeft)
        buttonUpLeft.place(x=0,y=25)
        buttonUp = tk.Button(moveMapFrame,text="^",command=self._onClickMoveUp)
        buttonUp.place(x=20,y=25)
        buttonUpRight = tk.Button(moveMapFrame,text=" ",command=self._onClickMoveUpRight)
        buttonUpRight.place(x=45,y=25)
        buttonLeft = tk.Button(moveMapFrame,text="<",command=self._onClickMoveLeft)
        buttonLeft.place(x=0,y=55)
        buttonRight = tk.Button(moveMapFrame,text=">",command=self._onClickMoveRight)
        buttonRight.place(x=40,y=55)
        buttonDownLeft = tk.Button(moveMapFrame,text=" ",command=self._onClickMoveDownLeft)
        buttonDownLeft.place(x=0,y=85)
        buttonDown = tk.Button(moveMapFrame,text="v",command=self._onClickMoveDown)
        buttonDown.place(x=21,y=85)
        buttonDownRight = tk.Button(moveMapFrame,text=" ",command=self._onClickMoveDownRight)
        buttonDownRight.place(x=45,y=85)

        rotateFrameHeight = 70
        rotateMapFrame = tk.Frame(self._mapActionsFrame, width=90, height=rotateFrameHeight,bg="lightgray")
        rotateMapFrame.place(relx=0.5,y=moveFrameHeight+selectorFrameHeight,anchor="n")
        labelRotateMap = tk.Label(rotateMapFrame,text="Rotate",bg="lightgray")
        labelRotateMap.place(relx=0.5,y=0,anchor="n")
        self._buttonRotateLeft1 = tk.Button(rotateMapFrame,text="|\nv")
        self._buttonRotateLeft1.place(x=0,y=25)
        self._buttonRotateLeft1.bind('<ButtonPress-1>', self._onClickRotateLeft)
        self._buttonRotateLeft1.bind('<ButtonRelease-1>', self._onReleaseStopRotateLeft)
        self._buttonRotateLeft2 = tk.Button(rotateMapFrame,text="<-")
        self._buttonRotateLeft2.place(x=15,y=25)
        self._buttonRotateLeft2.bind('<ButtonPress-1>', self._onClickRotateLeft)
        self._buttonRotateLeft2.bind('<ButtonRelease-1>', self._onReleaseStopRotateLeft)
        self._buttonRotateRight1 = tk.Button(rotateMapFrame,text="->")
        self._buttonRotateRight1.place(x=50,y=25)
        self._buttonRotateRight1.bind('<ButtonPress-1>', self._onClickRotateRight)
        self._buttonRotateRight1.bind('<ButtonRelease-1>', self._onReleaseStopRotateRight)
        self._buttonRotateRight2 = tk.Button(rotateMapFrame,text="|\nv")
        self._buttonRotateRight2.place(x=72,y=25)
        self._buttonRotateRight2.bind('<ButtonPress-1>', self._onClickRotateRight)
        self._buttonRotateRight2.bind('<ButtonRelease-1>', self._onReleaseStopRotateRight)

        zoomFrameHeight = 95
        zoomFrameWidth = 35
        zoomFrame = tk.Frame(self._mapActionsFrame,bg="lightgray")
        zoomFrame.place(relx=0.5,rely=0.7,anchor="n",width=zoomFrameWidth,height=zoomFrameHeight)
        labelZoomMap = tk.Label(zoomFrame,text="Zoom",bg="lightgray")
        labelZoomMap.place(x=0,y=0)
        buttonZoomIn = tk.Button(zoomFrame,text="+",command=self._onClickZoomIn)
        buttonZoomIn.place(relx=0.5,y=25,anchor="n")
        buttonZoomOut = tk.Button(zoomFrame,text="-",command=self._onClickZoomOut)
        buttonZoomOut.place(relx=0.5,y=65,anchor="n")

    def _drawAddRoadControl(self):
        self._addRoadFrame = tk.Frame(self._windowHandle,width=185,bg="lightgray",highlightbackground="black",highlightthickness=1)
        self._addRoadFrame.place(relx=((self._windowHandle.winfo_width()-self._windowHandle.winfo_height())*0.5 + self._margin)/self._windowHandle.winfo_width(),y=self._margin, relheight= (250/400)*(1 -((2*self._margin)/self._windowHandle.winfo_height())),relwidth=(1-self._windowHandle.winfo_height()/self._windowHandle.winfo_width())*0.5)

        labelFrom = tk.Label(self._addRoadFrame,bg="lightgray", text="From crossing*:")
        labelFrom.place(relx=0.5,y=3,anchor="n")
        self._from = tk.StringVar()
        inputFrom = tk.Entry(self._addRoadFrame, width=23,textvariable=self._from)
        inputFrom.place(relx=0.5, y=23,anchor="n")
        distanceFrame = tk.Frame(self._addRoadFrame, bg="lightgray")
        distanceFrame.place(anchor="n",relx=0.5,y=60,width=100,height=20)
        labelDistance = tk.Label(distanceFrame,bg="lightgray", text="Distance:")
        labelDistance.place(x=0,y=0)
        self._distance = tk.IntVar()
        inputDistance = tk.Entry(distanceFrame, width=5,textvariable=self._distance,justify="right")
        inputDistance.place(x=55, y=0)
        labelMeters = tk.Label(distanceFrame,bg="lightgray", text="m")
        labelMeters.place(x=87,y=0)
        labelTo = tk.Label(self._addRoadFrame,bg="lightgray", text="To crossing*:")
        labelTo.place(relx=0.5,y=90,anchor="n")
        self._to = tk.StringVar()
        inputTo = tk.Entry(self._addRoadFrame, width=23,textvariable=self._to)
        inputTo.place(relx=0.5, y=110, anchor="n")
        labelSeparatedComma = tk.Label(self._addRoadFrame,bg="lightgray",text="* Add streets separated by commas", font=("Yu Gothic UI",7))
        labelSeparatedComma.place(relx=0.5,y=140, anchor="n")
        self._twoWay = tk.BooleanVar()
        twoWayCheck = tk.Checkbutton(self._addRoadFrame,bg="lightgray", text="Two-Way Road?",variable=self._twoWay,onvalue=True,offvalue=False)
        twoWayCheck.place(relx=0.5, y=170, anchor="n")
        buttonAddRoad = tk.Button(self._addRoadFrame,text="Add road", command=self._addRoad)
        buttonAddRoad.place(relx=0.5,y=215, anchor="n")

    def _addRoad(self):
        self._coordinator.requestAddRoad(self._from.get(),self._to.get(),self._distance.get(),self._twoWay.get())

    def _drawRouteCalculator(self):
        self._calculateRouteFrame = tk.Frame(self._windowHandle,width=185,bg="lightgray",highlightbackground="black",highlightthickness=1)
        self._calculateRouteFrame.place(relx=((self._windowHandle.winfo_width()-self._windowHandle.winfo_height())/self._windowHandle.winfo_width())*0.5 + self._margin/self._windowHandle.winfo_width(),rely= 25/self._windowHandle.winfo_height()+(250/400)*(1 -(2*self._margin/self._windowHandle.winfo_height())), relheight= (150/400)*(1 -(2*self._margin/self._windowHandle.winfo_height())), relwidth=(1-self._windowHandle.winfo_height()/self._windowHandle.winfo_width())*0.5)

        selectorsFrame = tk.Frame(self._calculateRouteFrame, bg="lightgray")
        selectorsFrame.place(anchor="n",relx=0.5,y=10,width=150,height=30)
        self._pedestrianAuto = tk.StringVar(value="Auto")
        pedestrian = tk.Radiobutton(selectorsFrame,text="Pedestrian",variable=self._pedestrianAuto,value="Pedestrian", bg="lightgray")
        pedestrian.place(x=0, y=0,anchor="nw")
        auto = tk.Radiobutton(selectorsFrame,text="Auto",variable=self._pedestrianAuto,value="Auto", bg="lightgray")
        auto.place(x=90,y=0,anchor="nw")

        buttonOrigin = tk.Button(self._calculateRouteFrame,text="Set origin", width=15)
        buttonOrigin.place(relx=0.5,y=40,anchor="n")
        buttonDestination = tk.Button(self._calculateRouteFrame,text="Set destination", width=15)
        buttonDestination.place(relx=0.5,y=70,anchor="n")
        buttonRoute = tk.Button(self._calculateRouteFrame,text="Calculate route",width=15)
        buttonRoute.place(relx=0.5,y=100,anchor="n")

    def update(self, data):
        if data == "window":
            self._adaptToWindowSize()

    def _adaptToWindowSize(self):
        self._mapActionsFrame.place(relheight=1 - (2*self._margin/self._windowHandle.winfo_height()))
        self._addRoadFrame.place(relheight= (250/400)*(1 -(2*self._margin/self._windowHandle.winfo_height())))
        self._calculateRouteFrame.place(rely= 25/self._windowHandle.winfo_height()+(250/400)*(1 -(2*self._margin/self._windowHandle.winfo_height())), relheight= (150/400)*(1 -(2*self._margin/self._windowHandle.winfo_height())))

    def _onClickRotateLeft(self, event):
        self._buttonRotateLeft1.config(relief=tk.SUNKEN)
        self._buttonRotateLeft2.config(relief=tk.SUNKEN)
        self._windowHandle.update_idletasks()
        if not self._busy:
            self._buttonPressed = True
            self._windowHandle.after(150,self._rotateLeftSelectMode)
        
    def _rotateLeftSelectMode(self):
        self._busy = True
        if self._buttonPressed:
            self._buttonPressedFlavor = "Long"
            if self._currentPostionMap.get() == "CP":
                self._coordinator.rotateLeft_CP(self._buttonPressedFlavor)
            else:
                self._coordinator.rotateLeft_Map(self._buttonPressedFlavor)
        else:
            self._buttonPressedFlavor = "Quick"
            if self._currentPostionMap.get() == "CP":
                pass
            else:
                self._coordinator.rotateLeft_Map(self._buttonPressedFlavor)
            self._busy = False

    def _onReleaseStopRotateLeft(self, event):
        self._buttonRotateLeft1.config(relief=tk.RAISED)
        self._buttonRotateLeft2.config(relief=tk.RAISED)
        self._windowHandle.update_idletasks()
        if self._buttonPressed:
            self._buttonPressed = False
            if self._buttonPressedFlavor == "Long":
                if self._currentPostionMap.get() == "CP":
                    self._coordinator.stopRotation_CP()
                else:
                    self._coordinator.stopLeftRotation_Map()
                self._buttonPressedFlavor = "Quick"
                self._busy = False

    def _onClickRotateRight(self, event):
        self._buttonRotateRight1.config(relief=tk.SUNKEN)
        self._buttonRotateRight2.config(relief=tk.SUNKEN)
        self._windowHandle.update_idletasks()
        if not self._busy:
            self._buttonPressed = True
            self._windowHandle.after(150,self._rotateRightSelectMode)

    def _rotateRightSelectMode(self):
        self._busy = True
        if self._buttonPressed:
            self._buttonPressedFlavor = "Long"
            if self._currentPostionMap.get() == "CP":
                self._coordinator.rotateRight_CP(self._buttonPressedFlavor)
            else:
                self._coordinator.rotateRight_Map(self._buttonPressedFlavor)
        else:
            self._buttonPressedFlavor = "Quick"
            if self._currentPostionMap.get() == "CP":
                pass
            else:
                self._coordinator.rotateRight_Map(self._buttonPressedFlavor)
            self._busy = False

    def _onReleaseStopRotateRight(self, event):
        self._buttonRotateRight1.config(relief=tk.RAISED)
        self._buttonRotateRight2.config(relief=tk.RAISED)
        self._windowHandle.update_idletasks()
        if self._buttonPressed:
            self._buttonPressed = False
            if self._buttonPressedFlavor == "Long":
                if self._currentPostionMap.get() == "CP":
                    self._coordinator.stopRotation_CP()
                else:
                    self._coordinator.stopRightRotation_Map()
                self._buttonPressedFlavor = "Quick"
                self._busy = False

    def _onClickMoveLeft(self):
        if self._currentPostionMap.get() == "CP":
            self._coordinator.moveLeftPosition()
        else:
            self._coordinator.moveLeftMap()
    
    def _onClickMoveRight(self):
        if self._currentPostionMap.get() == "CP":
            self._coordinator.moveRightPosition()
        else:
            self._coordinator.moveRightMap()

    def _onClickMoveUp(self):
        if self._currentPostionMap.get() == "CP":
            self._coordinator.moveUpPosition()
        else:
            self._coordinator.moveUpMap()
    
    def _onClickMoveUpLeft(self):
        if self._currentPostionMap.get() == "CP":
            self._coordinator.moveUpLeftPosition()
        else:
            self._coordinator.moveUpLeftMap()

    def _onClickMoveUpRight(self):
        if self._currentPostionMap.get() == "CP":
            self._coordinator.moveUpRightPosition()
        else:
            self._coordinator.moveUpRightMap()

    def _onClickMoveDown(self):
        if self._currentPostionMap.get() == "CP":
            self._coordinator.moveDownPosition()
        else:
            self._coordinator.moveDownMap()
    
    def _onClickMoveDownLeft(self):
        if self._currentPostionMap.get() == "CP":
            self._coordinator.moveDownLeftPosition()
        else:
            self._coordinator.moveDownLeftMap()

    def _onClickMoveDownRight(self):
        if self._currentPostionMap.get() == "CP":
            self._coordinator.moveDownRightPosition()
        else:
            self._coordinator.moveDownRightMap()
            
    def _onClickZoomIn(self):
        self._coordinator.zoomInMap()

    def _onClickZoomOut(self):
        self._coordinator.zoomOutMap()