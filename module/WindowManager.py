import tkinter as tk

from .Observer import Subject

class WindowManager(Subject):
    _observers = []
    _window = None

    def __init__(self):
        self._window = tk.Tk()
        self._window.title("Map simulation")
        self._window.bind("<Configure>", self._on_resize)
        self._window.geometry("742x450")
        self._window.minsize(742,450)
        self._window.update_idletasks() # For the elements inside window to know window's size from the begining 

    @property
    def windowHandle(self):
        return self._window

    def _on_resize(self,event):
        self._notifyObservers()

    def registerObserver(self, observer):
        self._observers.append(observer)
    
    def _notifyObservers(self):
        for observer in self._observers:
            observer.update("window")