from os import listdir
from queue import Queue
import mss, numpy as np, pyautogui
from random import randint, random
from cv2 import cv2
from src.configuration import Configuration

class Detector:
    def __init__(self, config:Configuration) -> None:
        self.config = config['detector']
        self.config_metamask = config['metamask']
        self.config_game = config['game']
        self.data = {
            'screenshoot_status' : False
        }
        self.objects = self.__load_objects(self.config['images_path'])
    
    def loop(self, queues:dict[str, Queue]):
        while True:
            self.__printSreen()
            if self.data['screenshoot_status']: self.analyse()

    def analyse(self,sc:np.array,im:str):
        self.__clearPrintScreen()

    def __remove_suffix(input_string:str, suffix:str = '.png') -> str:
        """Returns the input_string without the suffix"""

        if suffix and input_string.endswith(suffix):
            return input_string[:-len(suffix)]
        return ''

    def __load_objects(self, dirPath:str):
        if not dirPath.endswith('/'): dirPath += '/'
        path_in_game = f"{dirPath}/in-game/"
        path_metamask = f"{dirPath}/metamask/{self.config_metamask['language']}/"
        files_in_game = listdir(path_in_game)
        files_metamask = listdir(path_metamask)
        objects = {}
        for file in files_in_game:
            objects['in-game'][self.__remove_suffix(file, '.png')] = cv2.imread(path_in_game + file)
        for file in files_metamask:
            objects['metamask'][self.__remove_suffix(file, '.png')] = cv2.imread(path_metamask + file)
        return objects

    def __clearPrintScreen(self,):
        self.data['screenshoot'] = None
        self.data['screenshoot_status'] = False

    def __printSreen(self,):
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            sct_img = np.array(sct.grab(monitor))
            # The screen part to capture
            # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

            # Grab the data
            self.data['screenshoot'] = sct_img[:,:,:3]
            self.data['screenshoot_status'] = True
            
    def __random_movement(self, positionToGo:tuple, velocity:float = 1):
        xNow, yNow = pyautogui.position() # Current Position
        moves = random.randint(2,4)
        pixelsx = positionToGo[0]-xNow
        pixelsy = positionToGo[1]-yNow
        if moves >= 4:
                moves = random.randint(2,4)
        avgpixelsx = pixelsx/moves
        avgpixelsy = pixelsy/moves
        while moves > 0:
            offsetx = (avgpixelsx+random.randint(-8, random.randint(5,10)));
            offsety = (avgpixelsy+random.randint(-8, random.randint(5,10)));
            # print(xNow + offsetx, yNow + offsety, moves)
            pyautogui.moveTo(xNow + offsetx, yNow + offsety, duration=0.2)
            moves = moves-1
            avgpixelsx = pixelsx / moves
            avgpixelsy = pixelsy / moves
        if moves == 0: return True
        return False


    def __calculatePosition(self, screenshoot:np.ndarray, object, threshold = 0.7):
        ...
    
    def __detectObjects(self, screenshoot, object):
        ...
    