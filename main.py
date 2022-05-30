import telebot

from qrcodebot.handlers import (start, photo, text, file)
from qrcodebot.handlers import (callback_factory, inline_photo)

from constants import (TOKEN, CONTENT_TYPES)

bot = telebot.TeleBot(
    token=TOKEN,
    num_threads=10,
    parse_mode='html'
)


def register_handlers() -> None:
    bot.register_message_handler(
        callback=start,
        chat_types=['private'],
        commands=['start'],
        pass_bot=True
    )
    bot.register_message_handler(
        callback=text,
        chat_types=['private'],
        content_types=['text'],
        pass_bot=True
    )
    bot.register_message_handler(
        callback=file,
        chat_types=['private'],
        content_types=CONTENT_TYPES,
        pass_bot=True
    )
    bot.register_message_handler(
        callback=photo,
        chat_types=['private'],
        content_types=['photo'],
        pass_bot=True
    )
    bot.register_message_handler(
        callback=photo,
        chat_types=['supergroup', 'group'],
        commands=['read'],
        pass_bot=True
    )
    bot.register_inline_handler(
        callback=inline_photo,
        pass_bot=True,
        func=lambda q: len(q.query) > 1
    )
    bot.register_callback_query_handler(
        callback=callback_factory,
        pass_bot=True,
        func=lambda c: True
    )


def main():
    register_handlers()
    bot.infinity_polling(skip_pending=True)


if __name__ == '__main__':
    main()
