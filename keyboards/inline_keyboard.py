from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select

from database.database import SessionLocal
from database.models import Group, Subject



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


async def item_menu() -> InlineKeyboardMarkup:
    async with SessionLocal() as session:
        subjects = (await session.scalars(select(Subject.name))).all()
        ikb = InlineKeyboardBuilder()
        for subject in subjects:
            ikb.add(InlineKeyboardButton(text=subject, callback_data=f"{subject}"))


        return ikb.as_markup()



async def group_menu() -> InlineKeyboardMarkup:
    async with SessionLocal() as session:
        groups = (await session.scalars(select(Group.name))).all()
        ikb = InlineKeyboardBuilder()
        for group in groups:
            ikb.add(InlineKeyboardButton(text=group, callback_data=f"{group}"))


        return ikb.as_markup()
