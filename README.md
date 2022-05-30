# QR-Code Reader & Generator Bot -> @qrg_bot
**Source code of** *[@qrg_bot](https://t.me/qrg_bot)* 
***
## What is a QR Code?
A Quick Response code is a two-dimensional pictographic code used for its fast readability and comparatively large storage capacity. The code consists of black modules arranged in a square pattern on a white background. The information encoded can be made up of any kind of data (e.g., binary, alphanumeric, or Kanji symbols)
***
## Introduction & Usage:
Bot encrypts your text, file messages into a qr code, and takes link, media files, text from qr coded images<br>It also works in inline mode and groups:<br>Inline mode: `@QRG_Bot some text`<br>In groups: reply with `/read` command to image(qr code)
***
## Installation:
- `git clone https://github.com/hoosnick/qrg-bot`<br>
- Create new virtual environment (if you want):<br>`virtualenv -p /usr/bin/python3 venv` `. ./venv/bin/activate`<br>
- `pip(3) install -r requirements.txt`<br>
- Fill your details in a .env file, as given in .env.sample. (You can either edit and rename the file or make a new file named .env)<br>
- `python(3) main.py`
***
## Credits
- [Lincoln Loop](https://github.com/lincolnloop) for [qrcode](https://github.com/lincolnloop/python-qrcode).
- [eternnoir](https://github.com/eternnoir) for [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).
- [coder2020official](https://github.com/coder2020official) for [pytba-templates](https://github.com/coder2020official/telebot_template).

Made with 💕 by [@hoosnick](https://github.com/hoosnick)