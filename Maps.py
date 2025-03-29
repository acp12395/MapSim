from module.PositionManager import PositionManager
from module.DataBase import DataBase
from module.WindowManager import WindowManager
from module.MapScreen import MapScreen
from module.HMI import HMI
from module.Coordinator import Coordinator

windowMgr = WindowManager()
dataBase = DataBase()
mapScreen = MapScreen(windowMgr)
windowMgr.windowHandle.update()
posMgr = PositionManager(mapScreen)
coordinator = Coordinator(dataBase, mapScreen, posMgr)
hmi = HMI(windowMgr,coordinator)

def on_close():
    global running
    running = False

windowMgr.windowHandle.protocol("WM_DELETE_WINDOW", on_close)

running = True

while running:  # It won't try to execute anymore after the window is closed
    windowMgr.windowHandle.update()