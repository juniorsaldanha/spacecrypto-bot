import time, sys
from unicodedata import name

from cv2 import log
from threading import  Thread
from queue import Queue
from src.configuration import Configuration
from src.detector import Detector
from src.logger import Logger
from src.telegram import Telegram

def main():
    config = Configuration()
    detector = Detector(config)
    logger = Logger(config)
    telegram = Telegram(config)
    
    queues = {
        detector.__class__.__name__: Queue(),
        logger.__class__.__name__: Queue(),
        telegram.__class__.__name__: Queue(),
    }

    appThreads = [Thread(
        target = detector.loop,
        args =(queues, ),
        name='DetectorThread')]
    appThreads.append(Thread(
        target = logger.loop,
        args =(queues, ),
        name='LoggerThread'))
    appThreads.append(Thread(
        target = telegram.loop,
        args =(queues, ),
        name='TelegramThread'))
    for th in appThreads: th.start()


if __name__ == "__main__":
    main()