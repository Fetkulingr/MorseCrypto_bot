'''
This program make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 2022/04/26
Ending 2022/05/06

'''
# Installing the necessary libraries
import telebot
from telebot import types
from settings import TG_TOKEN
from telebot import types
# Dictionary of Morse code letter correspondences
morse_code = {'а': '.-', 'б': '-...', 'в': '.--', 'г': '--.',
              'д': '-..', 'е': '.', 'ж': '...-', 'з': '--..',
              'и': '..', 'й': '.---', 'к': '-.-', 'л': '.-..', 'м': '--',
              'н': '-.', 'о': '---', 'п': '.--.', 'р': '.-.', 'с': '...',
              'т': '-', 'у': '..-', 'ф': '..-.', 'х': '....', 'ц': '-.-.',
              'ч': '---.', 'ш': '----', 'щ': '--.-', 'ъ': '.--.-.', 'ы': '-.--',
              'ь': '-..-', 'э': '..-..', 'ю': '..--', 'я': '.-.-'}

# Dictionary of Morse code letter correspondences
text_to_morse_code = {v: k for k, v in morse_code.items()}

# Creating an instance of the bot
bot = telebot.TeleBot(TG_TOKEN)

# Handler of the /start command
@bot.message_handler(commands=['start'])
def start_command(message):
    # Creating a keyboard with two buttons to select an action
    keyboard = types.InlineKeyboardMarkup()
    encrypt_button = types.InlineKeyboardButton(text='Зашифровать', callback_data='encrypt')
    decrypt_button = types.InlineKeyboardButton(text='Расшифровать', callback_data='decrypt')
    keyboard.add(encrypt_button, decrypt_button)
    # Sending a message with the keyboard
    bot.send_message(message.chat.id,
                     "Здравствуйте, {0.first_name}!\nМеня зовут<b> {1.first_name}</b>, Я бот, который может зашифровать и расшифровать текст в морзе-коде. Нажмите на одну из кнопок ниже, чтобы выбрать действие.".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=keyboard)


# Button click handler
@bot.callback_query_handler(func=lambda call: True)
def on_callback_query(call):
    if call.data == 'encrypt':  # Если была нажата кнопка "Зашифровать"
        bot.answer_callback_query(callback_query_id=call.id, text='Вы выбрали зашифровать')
        # Request a text from the user for encryption
        bot.send_message(chat_id=call.message.chat.id, text='Введите сообщение для шифрования:')
        # Register the following function to process the user's response
        bot.register_next_step_handler(call.message, encrypt_message)
    elif call.data == 'decrypt':  # If the "Decrypt" button was pressed
        bot.answer_callback_query(callback_query_id=call.id, text='Вы выбрали расшифровать')
        # Request a decryption text from the user
        bot.send_message(chat_id=call.message.chat.id, text='Введите сообщение для расшифровки:')
        # Register the following function to process the user's response
        bot.register_next_step_handler(call.message, decrypt_message)


# Function for encrypting the message
def encrypt_message(message):
    morse = ''
    text = message.text.lower()  # Reduce the text to lowercase
   # Go through each letter in the text and add the corresponding morse code to the string
    for letter in text:
        if letter in morse_code:
            morse += morse_code[letter] + ' '
    # If you manage to encrypt the message, send it to the user
    if morse:
        bot.send_message(chat_id=message.chat.id, text=f'Ваше зашифрованное сообщение:\n{morse}')
   # Otherwise inform the user that the message cannot be encrypted
    else:
        bot.send_message(chat_id=message.chat.id, text='Сообщение не может быть зашифровано.')


# Function to decrypt the message
def decrypt_message(message):
    text = ''
    morse = message.text.split()  # Split the text into separate morse codes
    # Go through each morse code and add the corresponding letter to the string
    for symbol in morse:
        if symbol in text_to_morse_code:
            text += text_to_morse_code[symbol]
        else:
            text += ' '  # If there is no match for the current Morse code, add a space
    # If you manage to decrypt the message, send it to the user
    if text:
        bot.send_message(chat_id=message.chat.id, text=f'Ваше расшифрованное сообщение:\n{text}')
    # Otherwise inform the user that the message cannot be decrypted
    else:
        bot.send_message(chat_id=message.chat.id, text='Сообщение не может быть расшифровано.')


# Launching the bot
bot.polling()
