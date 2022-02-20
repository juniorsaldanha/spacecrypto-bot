from src.configuration import Configuration
from src.date import dateFormatted
from queue import Queue
import sys

class Logger:
    COLOR = {
        'default': '\033[99m',
        'black': '\033[90m',
        'blue': '\033[94m',
        'grey': '\033[90m',
        'yellow': '\033[93m',
        'cyan': '\033[96m',
        'green': '\033[92m',
        'magenta': '\033[95m',
        'white': '\033[97m',
        'red': '\033[91m'
    }
    def __init__(self, config:Configuration = Configuration()) -> None:
        self.config = config['logger']
        if not self.config['path'].startswith('./'): self.config['path'] = f"./{self.config['path']}"
        if not self.config['path'].endswith('/'): self.config['path'] = f"{self.config['path']}/"
        self.__create_file()

    def loop(self, queue:dict[str, Queue]):
        while True:
            if queue[self.__class__.__name__].qsize():
                msg = queue[self.__class__.__name__].get_nowait()
                self.save(msg)
                self.print_message(msg)

    def format_message(self, message:str, color:str = 'default') -> str:
        message = f"[{dateFormatted()}] => {message}"
        return (
            self.COLOR.get(color.lower(), self.COLOR['default'])
            + message
            + '\033[0m'
        )

    def print_message(self, message:str, color:str = 'default') -> None:
        sys.stdout.write(self.format_message(message=message, color=color))
        sys.stdout.flush()

    def save(self, message:str) -> None:
        with open(self.config['path'], "a", encoding='utf-8') as logger_file:
            logger_file.write(f"{self.format_message(message)}\n")
            logger_file.close()

    def __create_file(self,) -> None:
        if (self.config['enable']):
            with open(self.config['path'], "a", encoding='utf-8') as logger_file:
                logger_file.write(self.format_message('Logger file created! 🤘') + '\n')
                logger_file.close()
