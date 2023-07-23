import os
import typing as t
import uuid

import qrcode
import telebot
from loguru import logger
from PIL import Image
from pyzbar import pyzbar
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles import moduledrawers

from constants import ADMIN
from qrcodebot.utils.error_handler import error_handler

path = os.getcwd()


def create_qr(
    data: str, user_id: int, style: int = 1,
    with_all_styles: bool = False
) -> t.List[str]:
    styles: t.Dict[int, moduledrawers.QRModuleDrawer] = {
        1: moduledrawers.SquareModuleDrawer,
        2: moduledrawers.GappedSquareModuleDrawer,
        3: moduledrawers.CircleModuleDrawer,
        4: moduledrawers.RoundedModuleDrawer,
        5: moduledrawers.VerticalBarsDrawer,
        6: moduledrawers.HorizontalBarsDrawer
    }

    if not os.path.exists(f'{path}/qr-codes'):
        os.makedirs('qr-codes')

    def make_image(_style: moduledrawers.QRModuleDrawer, img_path: str):
        qr = qrcode.QRCode(
            version=None,
            error_correction=ERROR_CORRECT_H,
            box_size=10, border=4
        )
        qr.add_data(str(data))
        qr.make(fit=True)

        img = qr.make_image(
            image_factory=StyledPilImage,
            fill_color="black",
            back_color="white",
            module_drawer=_style()
        )
        qr.clear()

        img.save(img_path)

    images = list()
    base_path = f'{path}/qr-codes/qrcode_{user_id}_'

    if with_all_styles:
        for __style in styles.values():
            image_path = f'{base_path}{uuid.uuid4().hex}.png'
            make_image(__style, image_path)
            images.append(image_path)
    else:
        image_path = f'{base_path}{uuid.uuid4().hex}.png'
        make_image(styles.get(style), image_path)
        images.append(image_path)

    return images


@error_handler
def delete_image(img: t.Union[str, None]):
    if img is None:
        return

    if not isinstance(img, str):
        return

    if not os.path.isfile(img):
        return

    os.unlink(img)


def read_qr(image):
    img = Image.open(image)
    output = pyzbar.decode(img)
    text = output[0][0].decode('utf-8')

    return text


def upload_photo(photo: str, bot: telebot.TeleBot):
    with open(photo, "rb") as file:
        m = bot.send_photo(ADMIN, file)

    return {
        "photo_file_id": str(m.photo[-1].file_id)
    }
