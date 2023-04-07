import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите текст в следующем формате:\n\
<имя валюты> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\n\
Увидеть список доступных валют: /values'
    bot.send_message(message.chat.id, text)


# Обрабатываются сообщения, содержащие команду '/values/.
@bot.message_handler(commands=['values'])
def handle_start_help(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


# Обрабатываются все текстовые сообщения.
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Запрос должен содержать 3 параметра.')
        quote, base, amount = values

        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

