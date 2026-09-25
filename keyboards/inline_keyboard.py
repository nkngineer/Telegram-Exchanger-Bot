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


async def tasks_menu(task_ids : list[int], work_titles: list[str]) -> InlineKeyboardMarkup:
    tasks : list[list[int,str]] = list(zip(task_ids, work_titles))
    ikb = InlineKeyboardBuilder()
    for task in tasks:
        ikb.add(InlineKeyboardButton(text = task[1],callback_data = f"task_{task[0]}"))

    ikb.add(InlineKeyboardButton(text="Назад",callback_data = "main_menu"))
    ikb.adjust(1)
    return ikb.as_markup()


async def download_menu(subject_id : int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text = "Загрузить работу", callback_data = f"get_file"))
    ikb.add(InlineKeyboardButton(text = "Отмена", callback_data = f"subject_{subject_id}"))
    ikb.adjust(1)

    return ikb.as_markup()