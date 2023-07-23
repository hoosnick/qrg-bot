import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN', "token_from_botfather")
ADMIN = os.getenv('ADMIN')

STYLES_PREVIEW = "https://raw.githubusercontent.com/lincolnloop/python-qrcode/main/doc/module_drawers.png"

CONTENT_TYPES = [
    'audio', 'document', 'sticker',
    'animation', 'video', 'video_note', 'voice'
]
STYLES = {
    'square': 1, 'gappedsquare': 2, 'circle': 3,
    'rounded': 4, 'verticalbars': 5, 'horizontalbars': 6
}
WELCOME = '''Hello, *{}*!

➟ _Bot encrypts your text, file messages into a QRCode;_
➟ _And takes link, file, text from QRCoded images;_

*It also works in inline mode and groups:*
*➟ Inline mode:* `@{} some text`
*➟ In groups:* reply with `/read` command to image'''
FAQ = '''<b>Pure QR Code generator&reader Bot</b>

©️ Lincoln Loop | <a href='https://github.com/lincolnloop/python-qrcode'>qrcode</a>

<b>What is a QR Code?</b>
A Quick Response code is a two-dimensional pictographic code used for its fast readability and comparatively large storage capacity. The code consists of black modules arranged in a square pattern on a white background. The information encoded can be made up of any kind of data (e.g., binary, alphanumeric, or Kanji symbols)'''
