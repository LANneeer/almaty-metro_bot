import typing
from dataclasses import dataclass

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@dataclass
class DynamicButtons:
    text: typing.List
    callback: typing.List = None
    align: typing.List[int] = None

    @property
    def inline(self):
        return generate_inline(self)


def generate_inline(args: DynamicButtons):
    keyboard = InlineKeyboardMarkup()
    if args.text and args.callback and not (len(args.text) == len(args.callback)):
        raise IndexError('Списки разной длинны!')
    if not args.align:
        for index, button in enumerate(args.text):
            keyboard.add(InlineKeyboardButton(text=str(button),
                                              callback_data=str(args.callback[index]))
                         )
    else:
        count = 0
        for row in args.align:
            keyboard.row(*[InlineKeyboardButton(text=str(text), callback_data=str(callback_data)
                                                ) for text, callback_data in
                           tuple(zip(args.text, args.callback))[count: count + row]])
            count += row
    return keyboard
