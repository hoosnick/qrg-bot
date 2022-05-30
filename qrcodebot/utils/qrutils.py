import os
import base64
import requests

import qrcode
from qrcode.image.styles.moduledrawers import (SquareModuleDrawer, GappedSquareModuleDrawer,
                                               CircleModuleDrawer, RoundedModuleDrawer,
                                               VerticalBarsDrawer, HorizontalBarsDrawer)
from qrcode.image.styledpil import StyledPilImage
from PIL import Image
from pyzbar import pyzbar

from constants import IMGBB_KEY

path = os.getcwd()


def get_drawer(s: int):
    styles = {
        1: SquareModuleDrawer, 2: GappedSquareModuleDrawer,
        3: CircleModuleDrawer, 4: RoundedModuleDrawer,
        5: VerticalBarsDrawer, 6: HorizontalBarsDrawer
    }
    return styles[s]


def create_qr(data: str, user_id: int, style: int) -> str:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10, border=4
    )
    qr.add_data(str(data))
    qr.make(fit=True)
    
    img = qr.make_image(
        image_factory=StyledPilImage,
        fill_color="black",
        back_color="white",
        module_drawer=get_drawer(style)()
    )
    qr.clear()
    image_path = f'{path}/QRCodes/qrcode_{user_id}.png'
    img.save(image_path)

    return image_path


def read_qr(image):
    img = Image.open(image)
    output = pyzbar.decode(img)
    text = output[0][0].decode('utf-8')

    return text


def upload_photo(photo):
    with open(photo, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": IMGBB_KEY,
            "image": base64.b64encode(file.read()),
        }
        response = requests.post(url, payload)
        if response.status_code == 200:
            return {
                "photo_url": response.json()["data"]["url"],
                "thumb_url": response.json()["data"]["thumb"]["url"],
            }

    return None
