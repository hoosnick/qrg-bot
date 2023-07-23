from loguru import logger
from telebot import TeleBot, types

from constants import CONTENT_TYPES, FAQ, STYLES, STYLES_PREVIEW, WELCOME
from qrcodebot.buttons.keyboards import Buttons
from qrcodebot.database.db import DataBase
from qrcodebot.utils.error_handler import error_handler
from qrcodebot.utils.qrutils import (
    create_qr, delete_image,
    path, read_qr, upload_photo
)

_CONTENT_TYPES = [
    types.Audio, types.Document, types.Sticker, types.Video,
    types.Animation, types.PhotoSize, types.VideoNote, types.Voice
]

db = DataBase()  # database
bt = Buttons()  # buttons


@error_handler
def start(m: types.Message, bot: TeleBot):
    user = m.from_user
    bot_username = bot.get_me().username

    db.new_user(user.id, user.full_name)

    bot.reply_to(
        m, text=WELCOME.format(user.first_name, bot_username),
        parse_mode='Markdown', reply_markup=bt.main_menu()
    )


def text(m: types.Message, bot: TeleBot):
    img = None

    db.update_name(m.from_user.id, m.from_user.full_name)
    style = db.get_user(m.from_user.id).style

    try:
        img = create_qr(m.text, m.from_user.id, style)

        with open(img[0], 'rb') as image:
            bot.send_photo(
                chat_id=m.chat.id, photo=image,
                reply_to_message_id=m.message_id
            )
    except Exception as e:
        logger.exception(e)
        bot.reply_to(m, e)
    finally:
        delete_image(img[0])


def file(m: types.Message, bot: TeleBot):
    img, content_type, file_id = None, None, None

    db.update_name(m.from_user.id, m.from_user.full_name)

    for ct in CONTENT_TYPES + ['photo']:
        data = getattr(m, ct)
        for _ct in _CONTENT_TYPES:
            if isinstance(data, _ct):
                content_type, file_id = ct, data.file_id

    if content_type is not None:
        _data = "{}|{}".format(content_type, file_id)
        style = db.get_user(m.from_user.id).style

        try:
            img = create_qr(_data, m.from_user.id, style)

            with open(img[0], 'rb') as image:
                bot.send_photo(
                    chat_id=m.chat.id, photo=image,
                    reply_to_message_id=m.message_id
                )
        except Exception as e:
            bot.reply_to(
                message=m, text='<b>I can\'t do anything with this!</b>',
            )
            logger.exception(e)
        finally:
            delete_image(img)


def photo(m: types.Message, bot: TeleBot):
    img_path = None
    try:
        if isinstance(m.reply_to_message, types.Message) and \
                m.chat.type in ['supergroup', 'group']:
            is_replied = True
            _photo = m.reply_to_message.photo[-1] \
                if m.reply_to_message.content_type == 'photo' \
                else m.photo[-1]
        else:
            _photo = m.photo[-1]
            is_replied = False

        file_info = bot.get_file(_photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        img_path = f'{path}/qr-codes/qrcode_{_photo.file_unique_id}.png'

        with open(img_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        reply_to = m.message_id if not is_replied \
            else m.reply_to_message.message_id
        text: str = read_qr(img_path)

        if len(text.split('|')) == 2 and text.startswith(tuple(CONTENT_TYPES)):
            my_data = text.split('|')
            code = f"bot.send_{my_data[0]}({m.chat.id}, '{my_data[1]}', reply_to_message_id={reply_to})"
            exec(code)
        else:
            bot.send_message(
                chat_id=m.chat.id, text=text,
                reply_to_message_id=reply_to
            )
    except Exception as e:
        if m.chat.type not in ['supergroup', 'group']:
            bot.reply_to(m, '<b>I can\'t do anything with this!</b>')
        logger.exception(e)
    finally:
        if bot.get_chat_member(m.chat.id, bot.get_me().id).can_delete_messages:
            bot.delete_message(m.chat.id, m.message_id)

        delete_image(img_path)


@error_handler
def inline_photo(iq: types.InlineQuery, bot: TeleBot):
    text = str(iq.query)
    user_id = iq.from_user.id
    qr_images = list()

    if not text.endswith('.'):
        return bot.answer_inline_query(
            inline_query_id=iq.id, cache_time=1000,
            results=[
                types.InlineQueryResultArticle(
                    id=1, title='Error', description='Text must endswith "."',
                    input_message_content=types.InputTextMessageContent(
                        message_text=":("
                    )
                )
            ]
        )

    try:
        qr_images = create_qr(text[:-1], user_id, with_all_styles=True)

        images = list()
        for _id, qr_image in enumerate(qr_images, start=1):
            image = upload_photo(qr_image, bot)

            if not image:
                continue

            images.append(bt.inlinePhoto(id=_id, img=image))

        bot.answer_inline_query(
            inline_query_id=iq.id,
            results=images,
            cache_time=1000
        )
    finally:
        for qr_image in qr_images:
            delete_image(qr_image)


@error_handler
def callback_factory(c: types.CallbackQuery, bot: TeleBot):
    bot.answer_callback_query(c.id)

    if c.data == 'about':
        bot.edit_message_text(
            text=FAQ,
            chat_id=c.from_user.id,
            message_id=c.message.message_id,
            reply_markup=bt.faq(),
            disable_web_page_preview=True
        )
    elif c.data == 'change_style':
        bot.delete_message(c.from_user.id, c.message.message_id)
        bot.send_photo(
            chat_id=c.from_user.id,
            photo=STYLES_PREVIEW,
            caption="<i>Choose style:</i>",
            reply_markup=bt.styles()
        )
    elif c.data == 'back':
        bot.delete_message(c.from_user.id, c.message.message_id)
        bot.send_message(
            chat_id=c.from_user.id,
            text=WELCOME.format(c.from_user.first_name, bot.get_me().username),
            reply_markup=bt.main_menu(),
            parse_mode='Markdown'
        )
    elif c.data.endswith('style'):
        style = c.data.split('_')[0]
        db.update_style(c.from_user.id, STYLES[style])

        bot.delete_message(c.from_user.id, c.message.message_id)
        bot.send_message(
            chat_id=c.from_user.id,
            text="⚡️ Type *text* or send *file*, *qr-coded picture:*",
            parse_mode='Markdown'
        )
