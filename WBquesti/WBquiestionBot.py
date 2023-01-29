import telebot
import time
from telebot import types
from random import randint

with open("../organization/tokenBotTelegram.txt", "r") as f:  # ДОБАВИЛИ токен бот телеграм
        TOKENBOTTELEGRAM = f.readline().rstrip()

bot = telebot.TeleBot(TOKENBOTTELEGRAM)
states = {}
"""Список вариаций"""

STATE1 = 'Ответ по поводу количества запросов или подписка'
STATE2 = 'Ситуация оплаты'
STATE3 = 'текст рекламы'
STATE4 = 'проверка текста'
STATE5 = 'запуск рассылки'


STATE21 = "Оформелние подписки"
STATE22 = "Принимает фотографию"
STATE1000 = "Ожидание"

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    time.sleep(1)
    bot.send_message(message.from_user.id, 'Привет! Этот бот делает рассылку рекламы на Wildberries. Возможность рассказать о своем бизнесе или предложить услугу для предпринимателей')
    bot.send_chat_action(message.from_user.id, 'typing')
    time.sleep(1)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    array = ['Оформить подписку', "Информация о боте"]
    for iter in array:
        keyboard.add(types.KeyboardButton(iter))
    time.sleep(1)
    bot.send_message(message.from_user.id,
                     'Оформи подписку или напиши сколько необходимо сделать запросов, если есть вопросы - информация о боте', reply_markup=keyboard)
    states[message.from_user.id] = STATE1

@bot.message_handler(func=lambda message: states.get(message.from_user.id, STATE1) == STATE1)
def state1_handler(message):
    # if message.text == '10 запросов':
    #     bot.send_message(message.from_user.id, 'Счет №, пришли сюда скрин с оплатой',
    #                      reply_markup=types.ReplyKeyboardRemove())
    # states[message.from_user.id] = STATE21
    # if message.text == '20 запросов':
    #     bot.send_message(message.from_user.id, 'Счет №, пришли сюда скрин с оплатой',
    #                      reply_markup=types.ReplyKeyboardRemove())
    if message.text == 'Оформить подписку':
        bot.send_chat_action(message.from_user.id, 'typing')
        bot.send_message(message.from_user.id, 'стоимость, Счет №, пришли сюда скрин с оплатой',
                         reply_markup=types.ReplyKeyboardRemove())
        states[message.from_user.id] = STATE21
        time.sleep(1)
    elif message.text == "Информация о боте":
        bot.send_chat_action(message.from_user.id, 'typing')
        bot.send_message(message.from_user.id, 'Этот бот делает то-то то',
                         reply_markup=types.ReplyKeyboardRemove())
        states[message.from_user.id] = STATE1
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
        array = ['Оформить подписку', "Информация о боте"]
        for iter in array:
            keyboard.add(types.KeyboardButton(iter))
        time.sleep(1)
        bot.send_message(message.from_user.id,
                         'Оформи подписку или напиши сколько необходимо сделать запросов, если есть вопросы - информация о боте', reply_markup=keyboard)
    else:
        pass
        #TODO: Принять число и провести через обработчик, который определит сумму запросов

@bot.message_handler(func=lambda message: states.get(message.from_user.id, STATE1) == STATE21)
# def state1_handler(message):
#     bot.send_chat_action(message.from_user.id, 'typing')
#     time.sleep(1)
#     bot.send_message(message.from_user.id, "Чтобы активировать подписку, необходимо отправить на счет то-то то-то")
#     bot.send_chat_action(message.from_user.id, 'typing')
#     time.sleep(1)
#     bot.send_message(message.from_user.id, "После удачной оплаты отправьте боту скрин оплаты")
#     states[message.from_user.id] = STATE22


@bot.message_handler(func=lambda message: states.get(message.from_user.id, STATE1) == STATE21, content_types=['photo'])
def state1_handler(message):
    photo = max(message.photo, key=lambda x: x.height)
    print(photo.file_id)
    bot.reply_to(message, "принято")
    time.sleep(1)
    bot.send_message(message.from_user.id, "Вам придет сообщение о проверке оплаты модераторами", reply_markup=types.ReplyKeyboardRemove())
    states[message.from_user.id] = STATE1000
    #TODO: После оплаты нужно внести с помощью администрирования человека в круг привилегированных (создать новый список выводов)


    # @bot.message_handler(func=lambda message: states.get(message.from_user.id, STATE1) == STATE1)
    # def state1_handler(message):
    #     # bot.send_message(message.chat.id, '_', reply_markup=types.ReplyKeyboardRemove())
    #     bot.send_chat_action(message.from_user.id, 'typing')
    #     time.sleep(4)
    #     bot.send_message(message.from_user.id, 'Готово! Напиши сюда текст, который нужно отправить.',
    #                          reply_markup=types.ReplyKeyboardRemove())
    #     # обработка входящего сообщения
    #     if message.text == 'моя реклама ла ла ла':
    #         states[message.from_user.id] = STATE2
    #
    #     bot.send_chat_action(message.from_user.id, 'typing')
    #     time.sleep(2)
    #
    #     keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    #     array = ['да', 'нет']
    #     for iter in array:
    #         keyboard.add(types.KeyboardButton(iter))
    #         # обработка входящего сообщения
    #         if message.text == 'моя реклама ла ла ла':
    #             states[message.from_user.id] = STATE2
    #     bot.send_message(message.chat.id, 'Твое сообщение будет выглядить так: "моя реклама один два". Верно?', reply_markup=keyboard)
    #     if message.text == 'да':
    #         bot.send_message(message.from_user.id, 'Отлично! Запускаем рекламу. Позже пришлем отчет о проделанной работе',
    #                      reply_markup=types.ReplyKeyboardRemove())
    #         else:
    #         return
    # states[message.from_user.id] = STATE5
    #
    # bot.send_chat_action(message.from_user.id, 'typing')
    # time.sleep(4)
    # if message.text == 'нет':
    #     bot.send_message(message.from_user.id, 'Напиши сюда актуальный текст рассылки',
    #                      reply_markup=types.ReplyKeyboardRemove())
    # else:
    #     return
    #     if message.text == 'моя новая реклама ла ла ла':
    #         states[message.from_user.id] = STATE2
    # bot.send_message(message.chat.id, 'Твое сообщение будет выглядить так: "моя реклама один два". Верно?',
    #                  reply_markup=keyboard)
    # if message.text == 'да':
    #     bot.send_message(message.from_user.id, 'Отлично! Запускаем рекламу. Позже пришлем отчет о проделанной работе',
    #                      reply_markup=types.ReplyKeyboardRemove())
    #     else:
    #     return
    # states[message.from_user.id] = STATE5
bot.polling()