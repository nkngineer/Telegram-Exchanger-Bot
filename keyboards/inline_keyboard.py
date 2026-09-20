from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Профиль",callback_data="get_user_profile")],
            [InlineKeyboardButton(text="Предмет",callback_data="lesson_menu")],
        ]
    )

# TODO: добавить функции изменения группы и фамилии с именем
# def profile_menu() -> InlineKeyboardMarkup:
#     return InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="Изменить фамилию и имя",callback_data="edit_sur_and_last_name")],
#             [InlineKeyboardButton(text="Изменить группу",callback_data="edit_user_group")],
#         ]
#     )


def item_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Внедрение ИС",callback_data="VIS")],
            [InlineKeyboardButton(text="Основы Серт. и Станд.",callback_data="OSaS")],
            [InlineKeyboardButton(text="Основы БД",callback_data="DB")],
        ]
    )


def group_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="09c33",callback_data="09c33")],
            [InlineKeyboardButton(text="09c34",callback_data="09c34")],
            [InlineKeyboardButton(text="09c35",callback_data="09c35")],
            [InlineKeyboardButton(text="09c41",callback_data="09c41")]
        ]
    )