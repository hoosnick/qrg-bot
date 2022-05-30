import os

from telebot import TeleBot
from telebot.types import (Message, InlineQuery, CallbackQuery)
from telebot.types import (Audio, Document, Sticker, Animation,
                           Video, PhotoSize, VideoNote, Voice)

from qrcodebot.database import DataBase
from qrcodebot.buttons import Buttons

from qrcodebot.utils import error_handler
from qrcodebot.utils import (create_qr, read_qr, upload_photo, path)

from constants import (CONTENT_TYPES, WELCOME, STYLES, STYLES_PREVIEW, FAQ)

_CONTENT_TYPES = [Audio, Document, Sticker,
                  Video, Animation, PhotoSize,
                  VideoNote, Voice]

db = DataBase()  # database
db.create()  # create table if not exists
bt = Buttons()  # buttons


@error_handler
def start(m: Message, bot: TeleBot):
    user = m.from_user
    db.new_user(user.id, user.full_name)
    bot.reply_to(
        message=m,
        text=WELCOME.format(m.from_user.first_name, bot.get_me().username),
        parse_mode='Markdown',
        reply_markup=bt.main_menu()
    )


def text(m: Message, bot: TeleBot):
    user = m.from_user
    data, user_id = m.text, user.id
    img = None

    db.update_name(user_id, user.full_name)
    try:
        style = db.get_user(user_id).style
        img = create_qr(data, user_id, style)

        with open(img, 'rb') as image:
            bot.send_photo(
                chat_id=m.chat.id,
                photo=image,
                reply_to_message_id=m.message_id
            )
    except Exception:
        bot.reply_to(
            message=m,
            text='<b>Too many characters!</b>',
        )
    finally:
        if isinstance(img, str):
            os.unlink(img) if os.path.isfile(img) else None


def file(m: Message, bot: TeleBot):
    user = m.from_user
    user_id = user.id
    content_type, file_id = None, None

    db.update_name(user_id, user.full_name)
    for ct in CONTENT_TYPES + ['photo']:
        data = getattr(m, ct)
        for _ct in _CONTENT_TYPES:
            if isinstance(data, _ct):
                content_type, file_id = ct, data.file_id

    if content_type is not None:
        _data = "{}|{}".format(
            content_type,
            file_id,
        )
        img = None
        try:
            style = db.get_user(user_id).style
            img = create_qr(_data, user_id, style)

            with open(img, 'rb') as image:
                bot.send_photo(
                    chat_id=m.chat.id,
                    photo=image,
                    reply_to_message_id=m.message_id
                )
        except Exception:
            bot.reply_to(
                message=m,
                text='<b>I can\'t do anything with this!</b>',
            )
        finally:
            if isinstance(img, str):
                os.unlink(img) if os.path.isfile(img) else None


def photo(m: Message, bot: TeleBot):
    img_path = None
    try:
        if isinstance(m.reply_to_message, Message) and m.chat.type in ['supergroup', 'group']:
            is_replied = True
            photo_id = m.reply_to_message.photo[-1].file_id \
                if m.reply_to_message.content_type == 'photo' \
                else m.photo[-1].file_id
        else:
            photo_id = m.photo[-1].file_id
            is_replied = False

        file_info = bot.get_file(photo_id)
        downloaded_file = bot.download_file(file_info.file_path)
        img_path = f'{path}/QRCodes/qrcode_{photo_id}.png'

        with open(img_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        reply_to = m.message_id if not is_replied else m.reply_to_message.message_id
        text: str = read_qr(img_path)

        if len(text.split('|')) == 2 and text.startswith(tuple(CONTENT_TYPES)):
            my_data = text.split('|')
            code = f"bot.send_{my_data[0]}({m.chat.id}, '{my_data[1]}', reply_to_message_id={reply_to})"
            exec(code)
        else:
            bot.send_message(
                chat_id=m.chat.id,
                text=text,
                reply_to_message_id=reply_to
            )
    except Exception:
        if m.chat.type not in ['supergroup', 'group']:
            bot.reply_to(
                m, '<b>I can\'t do anything with this!</b>'
            )
    finally:
        if bot.get_chat_member(m.chat.id, bot.get_me().id).can_delete_messages:
            bot.delete_message(m.chat.id, m.message_id)

        if isinstance(img_path, str):
            os.unlink(img_path) if os.path.isfile(img_path) else None


@error_handler
def inline_photo(iq: InlineQuery, bot: TeleBot):
    text = str(iq.query)
    user_id = iq.from_user.id
    qr_image = None
    try:
        style = db.get_user(user_id).style
        qr_image = create_qr(text, user_id, style)
        image = upload_photo(qr_image)

        if image:
            bot.answer_inline_query(
                inline_query_id=iq.id,
                results=[bt.inlinePhoto(image)],
                cache_time=1000
            )
    finally:
        if isinstance(qr_image, str):
            try:
                os.unlink(qr_image) if os.path.isfile(qr_image) else None
            except:
                pass


@error_handler
def callback_factory(c: CallbackQuery, bot: TeleBot):
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
            text="*⚡️ Type text or send File, QRCoded picture:*",
            parse_mode='Markdown'
        )
