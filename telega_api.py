import requests
import logging
from json import dumps

# представляет объект InlineKeyboardButton
class InlineKeyboardButton(dict):
    def __init__(self, text, callback_data):
        self['text'] = text
        self['callback_data'] = callback_data

    def set(self, text_or_callback_data: str, value):
        if text_or_callback_data not in self.keys():
            raise ValueError
        else:
            self[text_or_callback_data] = value

    def set_text(self, text):
        self.set('text', text)

    def set_callback_data(self, callback_data):
        self.set('callback_data', callback_data)
        
 # представляет объект InlineKeyboardMarkup
class InlineKeyboardMarkup(dict):
    def __init__(self):
        self['inline_keyboard'] = []

    # добавить кнопки InlineKeyboardButton
    def add_buttons(self, *buttons: InlineKeyboardButton):
        for button in list(buttons):
            self['inline_keyboard'].append([button])

# представляет объект Message
class Message(dict):
    def __init__(self, message: dict):
        for key in message.keys():
            self[key] = message[key]

    @property
    def message_id(self):
        return self['message_id']

    @property
    def text(self):
        return self['text']

    @property
    def from_user(self):
        return User(self['from'])

# представляет объект User
class User(dict):
    def __init__(self, user: dict):
        for key in user.keys():
            self[key] = user[key]

    @property
    def id(self):
        return self['id']

class Callback_Query(dict):
    def __init__(self, callback_query: dict):
        for key in callback_query.keys():
            self[key] = callback_query[key]

    @property
    def data(self):
        return self['data']

    @property
    def from_user(self):
        return User(self['from'])

    @property
    def id(self):
        return self['id']

    @property
    def chat_instance(self):
        return self['chat_instance']

    @property
    def message(self):
        return Message(self['message'])

# представляет объект Update
class Update(dict):
    def __init__(self, update: dict):
        for key in update.keys():
            self[key] = update[key]

    @property
    def update_id(self):
        return self['update_id']

    @property
    def message(self):
        if 'message' in self.keys():
            return Message(self['message'])
        else:
            return None

    @property
    def callback_query(self):
        if 'callback_query' in self.keys():
            return Callback_Query(self['callback_query'])
        else:
            return None

class InputFile:
    def __init__(self):
        pass

class WebHook(dict):
    def __init__(self, url:str, certificate=None, max_connections=40, allowed_updates=["message", "edited_channel_post", "callback_query"]):
        self['url'] = url
        if certificate:
            self['certificate'] = certificate
        self['max_connections'] = max_connections
        self['allowed_updates'] = allowed_updates

class TelegaAPI:
    _url : str
    logging.basicConfig(filename='log.log', level=logging.INFO, filemode='w')
    _logger = logging.getLogger("[TelegaAPI]")
    _offset = None

    def __init__(self, TOKEN: str, skip_old_updates=True):
        self._logger.info("Init bot")
        self._url = f"https://api.telegram.org/bot{TOKEN}/"
        # пропускаю все сообщения, которые полуичили до включения скрипта
        if skip_old_updates:
            res = self.get_updates(limit=100)
            while(len(res) != 0):
                update = self.get_last_update(res)
                self._offset = update.update_id + 1
                res = self.get_updates(limit=100)
    
    # получить необработанные сообщения
    def get_updates(self, timeout=30, limit=1,
    allowed_updates=["message", "edited_channel_post", "callback_query"]) -> dict:
        params = {'timeout': timeout, 'offset': self._offset, 'limit': limit, 
        'allowed_updates': allowed_updates}
        self._logger.info(f"Getting updates with params {params}")
        updates = requests.get(self._url + "getUpdates", params).json()
        if updates['ok']:
            return updates['result']
        else:
            self._logger.exception(updates)
            raise requests.RequestException

    def get_update(self, updates: dict, update_pos):
        if update_pos >= len(updates['result']):
            raise IndexError
        return Update(updates['result'][update_pos])

    # получить последнее необработанное сообщение
    def get_last_update(self, results: dict):
        if len(results):
            return Update(results[len(results) - 1])
        else:
            return []

    # отправка сообщения
    def send_message(self, chat_id: int, text: str, reply_markup=None):
        params = {'chat_id': chat_id, 'text': text}
        if reply_markup is not None:
            params['reply_markup'] = dumps(reply_markup)
        self._logger.info(f"Sending message: {params}")
        response = requests.post(self._url + 'sendMessage', params).json()
        self._logger.info(f"Response from sending message: {response}")
        if response['ok'] == False:
            self._logger.error(response)
            raise requests.RequestException
        return Message(response['result'])

    # ждем сообщения
    def wait_for_message(self) -> Message:
        updates = []
        while len(updates) == 0:
            updates = self.get_updates(allowed_updates=['message'])
        update = self.get_last_update(updates)
        self._logger.info(f":Recieved update: {update}")
        self._offset = update.update_id + 1
        return update.message
    
    # ждем нажатия пользователем кнопки
    def wait_for_callback_query(self) -> Callback_Query:
        updates = []
        while len(updates) == 0:
            updates = self.get_updates(allowed_updates=['callback_query'])
        update = self.get_last_update(updates)
        self._logger.info(f":Recieved update: {update}")
        self._offset = update.update_id + 1
        return update.callback_query
