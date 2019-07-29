from telega_api import *
from datetime import time, datetime
from time import sleep
import actions_impl

#здесь токен бота
TOKEN = ""
#Время проверки (час, минута, секунда)
check_time = time(7, 7, 7, 0)

if TOKEN == "":
    print("Отсутствует токен бота")
    exit(-1)

#Инициализация бота
bot = TelegaAPI(TOKEN)

#id пользователя, которому будет приходить уведомление
#получается после запуска скрипта отправкой команды /start боту
worker_id = 0

#функция для проверки БД
def check_db_data():
    return {"code":12, "message":"Empty values"}

#словарь ошибок
#Ключ - кол ошибки, значения - предлгаемые действия
#0 позиция - название вызываемой функции, 1 позиция - описание
dict_of_actions = \
    {12: [
        ["action1", "Do action 1"],
        ["action2", "Do action 2"],
        ["action3", "Do action 3"]
    ],
     13: [
        ["action4", "Do action 4"],
        ["action5", "Do action 5"]
     ]

    }

#Добавление кнопок выбора действий в клавиатуру
def add_keys(keyboard :InlineKeyboardMarkup, error_code: int):
    actions = dict_of_actions[error_code]
    for action in actions:
        key = InlineKeyboardButton(text=action[1], callback_data=action[0])
        keyboard.add_buttons(key)

#Получение и вызов функции для выполнения выбора пользователя (добавить реализацию аргументов функции?)
def call_action(action):
    try:
        action_func = getattr(actions_impl, action.lower())
    except AttributeError:
        bot.send_message(worker_id, f"Неудалось выполнить действие {action}. "
        f"Возможно функция реагирования не реализована")
        return "Error"
    return action_func()


#Функция для проверки БД, получения возможных действий и отправки результатов в телегу
def send_bd_check_results():
    check_result = check_db_data()
    # клавиатура для выбора действий
    keyboard = InlineKeyboardMarkup()
    add_keys(keyboard, check_result["code"])
    # клавиатура дотверждения выбора
    confirm_keyboard = InlineKeyboardMarkup()
    confirm_keyboard.add_buttons(InlineKeyboardButton("Подтвердить", "yes"),
                                 InlineKeyboardButton("Изменить выбор", "no"))
    confirm = "no"
    while confirm == "no":
        response = bot.send_message(worker_id, f"Результаты проверки базы данных:\n\n"
        f"Код ошибки: {check_result['code']}\n"
        f"Сообщение:  {check_result['message']}",
        reply_markup = keyboard)
        # ждем выбора пользователя
        callback = bot.wait_for_callback_query()
        bot.send_message(worker_id, f"Вы выбрали {callback.data}", 
                        reply_markup=confirm_keyboard)
        # ждем подтверждение выбора
        confirm = bot.wait_for_callback_query().data
    result = call_action(callback.data)
    bot.send_message(worker_id, f"Результат выполнения: {result}")



# Обработчик команды /start
def get_worker_id(message):
    global worker_id
    worker_id = message.from_user.id

# Обработчик выбора пользователя
# по какой-то причине при первом выборе варианта, он не считается обработанным в телеграмме и обрабатывается
# при следующем запуске скрипта автоматически. Для этого идет проверка id пользователя.
# Поправка - считается обработанным через некоторое время (около пол минуты)
def get_action(call):
    result = call_action(call.data)
    bot.send_message(worker_id, f"Результат выполнения: {result}")

#Функция для проверки времени
def is_check_time():
    now = datetime.now().time()
    #если просто сравнить, то сравниваются и миллисекунды
    if now.hour == check_time.hour and now.minute == check_time.minute and now.second == check_time.second:
        return True
    else:
        return False

print("Отправьте команду /start боту")
try:
    #Ожидание команды /start
    while True:
        message = bot.wait_for_message()
        if message.text == '/start':
            break
    get_worker_id(message)
    bot.send_message(worker_id, f"Готово, проверка будет выполнена в {check_time}")
    # ждем наступления времени проверки
    while not is_check_time():
        sleep(1)
    # выполняем проверку и высылаем результаты
    send_bd_check_results()
    pass
except KeyboardInterrupt:
    if worker_id:
        bot.send_message(worker_id, "Скрипт остановлен")
    print("Скрипт остановлен")