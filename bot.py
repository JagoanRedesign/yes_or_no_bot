import os
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup
from dotenv import load_dotenv
import requests

# installing pip install  python-telegram-bot

load_dotenv()
token = os.getenv('TOKEN')


url = 'https://yesno.wtf/api?force='
answers_list = ['да', 'нет', 'yes', 'no']
help_words = ['помощь', 'help', '/help', '?']

def get_eng_answer(answer):
    if answer in answers_list[0:2]:
        if answer == 'да':
            return 'yes'
        else:
            return 'no'
    else:
        return answer

def get_answer_gif(answer):
    print('answer ', answer)
    response = requests.get(url + get_eng_answer(answer))
    print('response ', response)
    return response.json().get('image')


def say_hi(update, context):
    chat = update.effective_chat
    user_message = update.message['text'].lower()
    if user_message in answers_list:
        context.bot.send_message(
            chat_id=chat.id,
            text=(f'Ожидайте.. (если ответа долго нет попробуйте еще раз)'))
        answer_gif = get_answer_gif(user_message)
        context.bot.send_message(
            chat_id=chat.id,
            text=(f'Вот ваша гифка для ответа {user_message}:'))

        context.bot.send_document(
            chat_id=chat.id,
            document=answer_gif)
    elif user_message in help_words:
        context.bot.send_message(
            chat_id=chat.id,
            text=(f'Для получения гифки с анимацией Да или Нет'
                   ' напишите Да или Нет или нажмите соответствующую кнопку'))
        answer_gif = get_answer_gif(user_message)
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text=f'Для такого ответа нет гифки')


def wake_up(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([
                                ['да', 'нет'],
                                ['помощь']
                                ])
    context.bot.send_message(chat_id=chat.id, 
                             text='Спасибо, что включили меня. '
                             'Для получения гифки напишите "да" или "нет", '
                             'или нажмите соответствующую кнопку',
                             reply_markup=button)


def main():
    updater = Updater(token=token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
    updater.start_polling()
    updater.idle() 


if __name__ == '__main__':
    main()