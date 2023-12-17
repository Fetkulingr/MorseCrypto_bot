'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 2022/04/26
Ending 2022/05/06

'''
# Установка необходимых библиотек
import telebot
from telebot import types
from settings import TG_TOKEN
from telebot import types
# Словарь соответствий букв морзе-кодам
morse_code = {'а': '.-', 'б': '-...', 'в': '.--', 'г': '--.',
              'д': '-..', 'е': '.', 'ж': '...-', 'з': '--..',
              'и': '..', 'й': '.---', 'к': '-.-', 'л': '.-..', 'м': '--',
              'н': '-.', 'о': '---', 'п': '.--.', 'р': '.-.', 'с': '...',
              'т': '-', 'у': '..-', 'ф': '..-.', 'х': '....', 'ц': '-.-.',
              'ч': '---.', 'ш': '----', 'щ': '--.-', 'ъ': '.--.-.', 'ы': '-.--',
              'ь': '-..-', 'э': '..-..', 'ю': '..--', 'я': '.-.-'}

# Словарь соответствий морзе-кодов буквам
text_to_morse_code = {v: k for k, v in morse_code.items()}

# Создаем экземпляр бота
bot = telebot.TeleBot(TG_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    # Создаем клавиатуру с двумя кнопками для выбора действия
    keyboard = types.InlineKeyboardMarkup()
    encrypt_button = types.InlineKeyboardButton(text='Зашифровать', callback_data='encrypt')
    decrypt_button = types.InlineKeyboardButton(text='Расшифровать', callback_data='decrypt')
    keyboard.add(encrypt_button, decrypt_button)
    # Отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id,
                     "Здравствуйте, {0.first_name}!\nМеня зовут<b> {1.first_name}</b>, Я бот, который может зашифровать и расшифровать текст в морзе-коде. Нажмите на одну из кнопок ниже, чтобы выбрать действие.".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=keyboard)


# Обработчик нажатия на кнопку
@bot.callback_query_handler(func=lambda call: True)
def on_callback_query(call):
    if call.data == 'encrypt':  # Если была нажата кнопка "Зашифровать"
        bot.answer_callback_query(callback_query_id=call.id, text='Вы выбрали зашифровать')
        # Запросить у пользователя текст для шифрования
        bot.send_message(chat_id=call.message.chat.id, text='Введите сообщение для шифрования:')
        # Зарегистрировать следующую функцию для обработки ответа пользователя
        bot.register_next_step_handler(call.message, encrypt_message)
    elif call.data == 'decrypt':  # Если была нажата кнопка "Расшифровать"
        bot.answer_callback_query(callback_query_id=call.id, text='Вы выбрали расшифровать')
        # Запросить у пользователя текст для расшифровки
        bot.send_message(chat_id=call.message.chat.id, text='Введите сообщение для расшифровки:')
        # Зарегистрировать следующую функцию для обработки ответа пользователя
        bot.register_next_step_handler(call.message, decrypt_message)


# Функция для зашифровки сообщения
def encrypt_message(message):
    morse = ''
    text = message.text.lower()  # Привести текст к нижнему регистру
    # Пройти по каждой букве в тексте и добавить соответствующий морзе-код в строку
    for letter in text:
        if letter in morse_code:
            morse += morse_code[letter] + ' '
    # Если получилось зашифровать сообщение, отправить его пользователю
    if morse:
        bot.send_message(chat_id=message.chat.id, text=f'Ваше зашифрованное сообщение:\n{morse}')
    # Иначе сообщить пользователю, что сообщение не может быть зашифровано
    else:
        bot.send_message(chat_id=message.chat.id, text='Сообщение не может быть зашифровано.')


# Функция для расшифровки сообщения
def decrypt_message(message):
    text = ''
    morse = message.text.split()  # Разбить текст на отдельные морзе-коды
    # Пройти по каждому морзе-коду и добавить соответствующую букву в строку
    for symbol in morse:
        if symbol in text_to_morse_code:
            text += text_to_morse_code[symbol]
        else:
            text += ' '  # Если для текущего морзе-кода нет соответствия, добавить пробел
    # Если получилось расшифровать сообщение, отправить его пользователю
    if text:
        bot.send_message(chat_id=message.chat.id, text=f'Ваше расшифрованное сообщение:\n{text}')
    # Иначе сообщить пользователю, что сообщение не может быть расшифровано
    else:
        bot.send_message(chat_id=message.chat.id, text='Сообщение не может быть расшифровано.')


# Запускаем бота
bot.polling()
