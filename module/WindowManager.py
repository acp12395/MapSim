import tkinter as tk

from .Observer import Subject

class WindowManager(Subject):
    _observers = []
    _window = None

    def __init__(self):
        self._window = tk.Tk()
        self._window.title("Map simulation")
        self._window.state("zoomed")
        self._window.update_idletasks() # For the elements inside window to know window's size from the begining 
        self._windowWidth = self._window.winfo_width()
        self._windowHeight = self._window.winfo_height()
        self._windowAspectRatio = self._windowWidth/self._windowHeight

        if 742/self._windowAspectRatio < 450:
            minHeight = 450
            minWidth = int(450 * self._windowAspectRatio)
        else:
            minHeight = int(742/self._windowAspectRatio)
            minWidth = 742

        self._window.minsize(minWidth,minHeight)

        self._resizing = False
        self._window.bind("<Configure>", self._on_resize)

    @property
    def windowHandle(self):
        return self._window

    def _on_resize(self,event):
        if event.widget != self._window:
            return
        self._eventWidth = event.width
        self._eventHeight = event.height

        self._notifyObservers()

        self._resizing = True

    def executeExistingResizingTasks(self):

        if not self._resizing:
            return
        
        self._resizing = False
    
        # Decide which dimension controls.
        if self._eventWidth != self._windowWidth:
            desired_width = self._eventWidth
            desired_height = int(self._eventWidth / self._windowAspectRatio)
        elif self._eventHeight != self._windowHeight:
            desired_height = self._eventHeight
            desired_width = int(self._eventHeight * self._windowAspectRatio)
        else:
            desired_width = self._eventWidth
            desired_height = self._eventHeight

        # Override if necessary.
        if self._eventWidth != desired_width or self._eventHeight != desired_height:
            self._windowWidth = desired_width
            self._windowHeight = desired_height
            # Manually give it the proper dimensions.
            self._window.geometry(f'{desired_width}x{desired_height}')
            self._window.update_idletasks()

            self._notifyObservers()

    def registerObserver(self, observer):
        self._observers.append(observer)
    
    def _notifyObservers(self):
        for observer in self._observers:
            observer.update("window")