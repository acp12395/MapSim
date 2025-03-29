from module.PositionManager import PositionManager
from module.DataBase import DataBase
from module.WindowManager import WindowManager
from module.MapScreen import MapScreen
from module.HMI import HMI

windowMgr = WindowManager()
dataBase = DataBase()
hmi = HMI(windowMgr,dataBase)
mapScreen = MapScreen(windowMgr,dataBase)
windowMgr.windowHandle.update()
posMgr = PositionManager(mapScreen)

def on_close():
    global running
    running = False

windowMgr.windowHandle.protocol("WM_DELETE_WINDOW", on_close)

running = True

while running:  # It won't try to execute anymore after the window is closed
    windowMgr.windowHandle.update()