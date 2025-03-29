import tkinter as tk

from .Observer import Observer

class MapScreen(Observer):
    _mapScreen = None
    _dataBase = None
    _windowHandle = None
    _margin = 25

    def __init__(self, windowMgr, dataBase):
        self._windowHandle = windowMgr.windowHandle
        self._drawMapScreen()
        self._dataBase = dataBase
        windowMgr.registerObserver(self)

    def update(self, data):
        if data == "window":
            self._adaptToWindowSize()

    def _adaptToWindowSize(self):
        self._mapScreen.place(relheight=1 - (2*self._margin/self._windowHandle.winfo_height()),relwidth=1 -((self._margin+332)/self._windowHandle.winfo_width()))
    
    def _drawMapScreen(self):
        self._mapScreen = tk.Canvas(self._windowHandle, background="black")
        self._mapScreen.place(y=self._margin, x=317, relheight=1 -(2*self._margin/self._windowHandle.winfo_height()), relwidth=1 -((self._margin+332)/self._windowHandle.winfo_width()))