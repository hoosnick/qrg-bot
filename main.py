import telebot
from loguru import logger
from constants import CONTENT_TYPES, TOKEN
from qrcodebot.handlers import users

bot = telebot.TeleBot(
    token=TOKEN,
    num_threads=10,
    parse_mode='html'
)


def register_handlers() -> None:
    bot.register_message_handler(
        callback=users.start,
        chat_types=['private'],
        commands=['start'],
        pass_bot=True
    )
    bot.register_message_handler(
        callback=users.text,
        chat_types=['private'],
        content_types=['text'],
        pass_bot=True
    )
    bot.register_message_handler(
        callback=users.file,
        chat_types=['private'],
        content_types=CONTENT_TYPES,
        pass_bot=True
    )
    bot.register_message_handler(
        callback=users.photo,
        chat_types=['private'],
        content_types=['photo'],
        pass_bot=True
    )
    bot.register_message_handler(
        callback=users.reply_to_photo,
        chat_types=['supergroup', 'group'],
        func=lambda m: m.reply_to_message.content_type == 'photo',
        commands=['read', 'r'], pass_bot=True
    )
    bot.register_inline_handler(
        callback=users.inline_photo,
        pass_bot=True,
        func=lambda q: len(q.query) >= 1
    )
    bot.register_callback_query_handler(
        callback=users.callback_factory,
        pass_bot=True,
        func=lambda c: True
    )


def main():
    logger.add("bot.log", backtrace=True, diagnose=True)
    register_handlers()
    bot.infinity_polling(skip_pending=True)


if __name__ == '__main__':
    main()
