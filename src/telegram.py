from queue import Queue
import requests
from src.configuration import Configuration

class Telegram:
    def __init__(self, config:Configuration = Configuration()) -> None:
        self.config = config['telegram']

    def loop(self, queues:dict[str, Queue]):
        ...

    def send_message(self, message:str) -> bool:
        if self.config['enable'] and self.config['token_api']!='your_bot_token' and self.config['token_api']!='your_chat_id':
            telegram_payload = f'https://api.telegram.org/bot{self.config["token_api"]}/sendMessage?chat_id={self.config["token_api"]}&parse_mode=Markdown&text={message}'
            response = requests.get(telegram_payload).status_code
            if response.status_code == 200:
                return True
            return False