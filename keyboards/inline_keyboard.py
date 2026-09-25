from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from database.services import get_subjects, get_groups


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text = "Профиль",callback_data = "get_user_profile")],
            [InlineKeyboardButton(text = "Предмет",callback_data = "lesson_menu")],
        ]
    )


async def item_menu() -> InlineKeyboardMarkup:
    subjects = await get_subjects()
    ikb = InlineKeyboardBuilder()
    for subject in subjects:
        ikb.add(InlineKeyboardButton(text = subject.name, callback_data = f"subject_{subject.id}"))

    ikb.add(InlineKeyboardButton(text="Назад",callback_data = "main_menu"))
    ikb.adjust(1)
    return ikb.as_markup()



async def group_menu() -> InlineKeyboardMarkup:
    groups = await get_groups()
    ikb = InlineKeyboardBuilder()
    for group in groups:
        ikb.add(InlineKeyboardButton(text = group.name, callback_data = f"{group.name}"))


    ikb.adjust(1)
    return ikb.as_markup()


async def profile_menu() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text="Изменить id",callback_data="change_id"))
    ikb.add(InlineKeyboardButton(text="Назад",callback_data = "main_menu"))
    ikb.adjust(1)
    return ikb.as_markup()


async def works_menu(works : list[str]) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    for work in works:
        # ikb.add(InlineKeyboardButton(text = work,callback_data = f"work_{work}")) # мб по work_id потом сделать
        ikb.add(InlineKeyboardButton(text = work,callback_data = f"get_file"))
    ikb.adjust(1)
    return ikb.as_markup()