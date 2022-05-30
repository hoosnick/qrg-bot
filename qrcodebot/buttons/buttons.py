from telebot import types


class Buttons:
    def __init__(self):
        self.IKM = types.InlineKeyboardMarkup
        self.IKB = types.InlineKeyboardButton
        self.IQRP = types.InlineQueryResultPhoto

    def main_menu(self) -> types.InlineKeyboardMarkup:
        return self.IKM(
            keyboard=[
                [self.IKB('*️⃣ Inline QR',
                          switch_inline_query_current_chat='hello')],
                [
                    self.IKB('⚙️ Styles', callback_data='change_style'),
                    self.IKB('About ℹ️', callback_data='about')
                ]
            ]
        )

    def faq(self) -> types.InlineKeyboardMarkup:
        return self.IKM(
            [
                [
                    self.back(),
                    self.IKB('Developer', 'https://t.me/hoosnick')
                ],
            ]
        )

    def styles(self) -> types.InlineKeyboardMarkup:
        return self.IKM(
            [
                [
                    self.IKB('Square', callback_data='square_style'),
                    self.IKB('Gapped Square',
                             callback_data='gappedsquare_style'),
                ],
                [
                    self.IKB('Circle', callback_data='circle_style'),
                    self.IKB('Rounded', callback_data='rounded_style'),
                ],
                [
                    self.IKB('Vertical Bars',
                             callback_data='verticalbars_style'),
                    self.IKB('Horizontal Bars',
                             callback_data='horizontalbars_style'),
                ],
                [self.back()]
            ]
        )

    def back(self) -> types.InlineKeyboardButton:
        return self.IKB('◀️ Back', callback_data='back')

    def inlinePhoto(self, image: dict) -> types.InlineQueryResultPhoto:
        return self.IQRP(
            id='@py_examples',
            title="qr_code",
            photo_url=image["photo_url"],
            thumb_url=image["thumb_url"],
        )
