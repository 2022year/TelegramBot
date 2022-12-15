import telebot
from config import money, TOKEN
from extensions import Converter, APIException
from telebot import types

bot = telebot.TeleBot(TOKEN)
sFormat=f"Формат ввода: Исх.валюта Рез.Валюта Количество\n(доллар рубль 100)\nили команды:/start /convert /values /help"

# Кнопки
def create_markup(base=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    for i in money.keys():
        if i != base:
            buttons.append(types.KeyboardButton(i.capitalize()))
    markup.add(*buttons)
    return markup


# Команды /start и /help
@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    user_name = message.from_user.full_name
    text = f"Привет, {user_name}!\n \
\n{sFormat}"
    bot.send_message(message.chat.id, text)


#/values - список валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Валюты:\n"
    for key in money:
        text = '\n-  <b>'.join((text, key)) + '</b>\n   <i>' + money[key][0] + '</i>'
    bot.send_message(message.chat.id, text, parse_mode='html')




#/convert - ввод с кнопками
@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = "Исходная валюта:"
    bot.send_message(message.chat.id, text, reply_markup=create_markup())
    bot.register_next_step_handler(message, base_handler)


def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = "Результирующая валюта:"
    bot.send_message(message.chat.id, text, reply_markup=create_markup(base))
    bot.register_next_step_handler(message, quote_handler, base)


def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip().lower()
    text = "Количество исходной валюты:"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)


def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        new_price = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации...\n{e}")
    else:
        text = f"Результат: ({base} {quote} {amount})={round(new_price, 4)}"
        bot.send_message(message.chat.id, text)


#Обработка сообщений
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.lower().split()
    try:
        if len(values) != 3:
            raise APIException(sFormat)
        b, q, a = map(str.lower, values)
        total_base = Converter.get_price(*values)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка ввода...\n{e}")
    else:
        text = f"Результат: ({b} {q} {a})={round(total_base, 4)}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

