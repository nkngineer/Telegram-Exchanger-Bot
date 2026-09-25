from asyncio import tasks

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, user

from database.services import insert_work, check_user_authentication, register_user, check_group, check_user_profile, get_task_names_by_subject_id, get_task_data_by_task_id
from keyboards.inline_keyboard import main_menu, group_menu, item_menu, profile_menu, tasks_menu, download_menu

from pathlib import Path
import asyncio



class Upload(StatesGroup):
    """
    FSM states for receiving file uploads from the user
    """
    waiting_subject_id = State()
    waiting_file = State()


class Text(StatesGroup):
    """
    FSM states for creating a Student entity (group + ID)
    """
    waiting_user_group = State()
    waiting_user_id = State()
    waiting_user_password = State()

main_router = Router()


async def start_message(message: Message) -> None:
    """
    Handle the start message and show the main menu
    """
    await message.answer(text = "Бот по загрузке лаб", reply_markup = main_menu())


async def edit_start_message(message: Message) -> None:
    """
    Handle the start message and show the main menu
    """
    await message.edit_text(text = "Бот по загрузке лаб", reply_markup = main_menu())


@main_router.message(CommandStart())
async def authentication_user(message: Message, state: FSMContext) -> None:
    """
    Handle the /start command and check user authentication

    :param message: incoming message from telegram by /start
    :return: None
    """
    telegram_user_id = message.from_user.id

    is_authorized = await check_user_authentication(telegram_user_id)
    print(f"Статус авторизации для {telegram_user_id} : {is_authorized}") # Полезный лог
    if not is_authorized:
        await message.answer(text = "Вы не авторизованы. Выберите группу",reply_markup = await group_menu())
        await state.set_state(Text.waiting_user_group)
        return

    await start_message(message)



@main_router.callback_query(Text.waiting_user_group,F.data)
async def edit_user_group(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Validate the selected group and advance the user to the corporate ID step.


    :param callback:
    :param state:
    :return: None
    """
    is_group_exist = await check_group(callback.data)
    if not is_group_exist: await callback.answer(text = "Такой группы нет!")
    else:
        await callback.message.edit_text(text = f"Группа {callback.data} выбрана!")

        await state.update_data(waiting_user_group = callback.data)


        await callback.message.answer(text = "Введите id вашей корпоративной почты / зачетки.\n"
                                                "Например - для p09s3452@voenmeh.ru id будет 52")
        await state.set_state(Text.waiting_user_id)

        # await edit_user_id(callback.message, state)



@main_router.callback_query(F.data == "lesson_menu")
async def output_lesson_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(text = "Предметы", reply_markup = await item_menu())


@main_router.callback_query(F.data == "main_menu")
async def output_lesson_menu(callback: CallbackQuery) -> None:
    await edit_start_message(callback.message)



# TODO
# @main_router.callback_query(F.data == "change_id")
# async def change_user_id(callback: CallbackQuery, state: FSMContext) -> None:
#     await callback.answer("Введите id")
#     await state.set_state(Text.waiting_user_id)



# TODO
@main_router.message(Text.waiting_user_id, F.text)
async def edit_user_id(message: Message, state: FSMContext) -> None:
    """
    Receive the corporate id, register the user and route to the main menu.

    :return: None
    """

    # await message.answer(text = "Введите id вашей корпоративной почты / зачетки.\n"
    #                                             "Например - для p09s3452@voenmeh.ru id будет 52")

    user_telegram_id = message.from_user.id

    print("функция ожидания ввода id от пользователя")
    corporate_id : int = int(message.text)



    state_data : dict[str,int] = await state.get_data()
    group_name : str = state_data.get("waiting_user_group")

    await register_user(user_telegram_id, corporate_id, group_name)

    await message.answer("id записан. ")

    await state.clear()
    # await state.set_state(Text.waiting_user_password)

    if await check_user_authentication(user_telegram_id):
        await start_message(message)


# TODO: future
# @main_router.message(Text.waiting_user_password, F.text)
# async def edit_user_id(message: Message, state: FSMContext) -> None:
#     # await message.answer(text = "Введите id вашей корпоративной почты / зачетки.\n"
#     #                                             "Например - для p09s3452@voenmeh.ru id будет 52")
#
#     user_telegram_id = message.from_user.id
#
#     user_password : int = int(message.text)
#     # await check_user_password(user_password)
#
#
#
#     # await register_user(user_telegram_id, corporate_id, group_name, user_password)
#
#     # await message.answer("пользователь зарегистрирован. ")
#
#     # await state.clear()
#
#     # if await check_user_authentication(user_telegram_id):
#     #     await start_message(message)





# TODO: добавить IKB с изменением данных профиля
@main_router.callback_query(F.data == "get_user_profile")
async def get_user_profile(callback: CallbackQuery) -> None:
    """
    Output user's profile(id and group)

    :return: None
    :note: Calls check_user_profile(), which returns Student.id and Student group name.
    """
    telegram_id = callback.from_user.id
    profile  = await check_user_profile(telegram_id)
    if not profile:
        await callback.message.answer(text = "Профиль не найден!")
        return

    corporate_id, user_group_name = profile
    await callback.message.edit_text(text = f"Ваш id : {corporate_id}\nГруппа : {user_group_name}",reply_markup=await profile_menu())




@main_router.callback_query(F.data.startswith("subject_"))
async def get_subject_tasks(callback : CallbackQuery, state : FSMContext) -> None:
    await callback.answer()
    subject_id : int = int(callback.data.split("_")[-1])
    user_telegram_id : int = callback.from_user.id

    tasks_id, work_titles = zip(*await get_task_names_by_subject_id(subject_id, user_telegram_id))


    await state.update_data(waiting_subject_id = subject_id)

    await callback.message.edit_text(text="Список работ", reply_markup = await tasks_menu(tasks_id, work_titles))


@main_router.callback_query(F.data.startswith("task_"))
async def get_tasks_data(callback : CallbackQuery, state : FSMContext) -> None:
    await callback.answer()
    state_data: dict[str, int] = await state.get_data()
    subject_id: int = state_data.get("waiting_subject_id")
    task_id : int = int(callback.data.split("_")[-1])
    telegram_id : int = callback.from_user.id
    task_description, task_starts_at, task_ends_at = zip(*await get_task_data_by_task_id(task_id, subject_id, telegram_id))


    # TODO: сделать функцию вывода описания каждой из работ
    await callback.message.edit_text(text=f"Описание: {task_description}\n"
                                          f"Начало: {task_starts_at}\n"
                                          f"Конец: {task_ends_at}", reply_markup = await download_menu(subject_id))



@main_router.callback_query(F.data == "get_file")
async def cmd_upload(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Prompt the user to send a file and enter the file-upload FSM state.

    :return: None
    """

    await callback.message.delete()
    await callback.message.answer(text = "Отправьте файл")
    await state.set_state(Upload.waiting_file)


# @main_router.message(Command("get_file"))
# async def cmd_upload(message: Message, state: FSMContext) -> None:
#     """
#     Prompt the user to send a file and enter the file-upload FSM state.
#
#     :return: None
#     """
#     await message.answer("Отправьте файл")
#     await state.set_state(Upload.waiting_file)



@main_router.message(Upload.waiting_file, F.document)
async def upload_file_from_user(message: Message, state: FSMContext) -> None:
    """
    Receive a file from the user and persist it via ``add_work``


    :return: None
    :note: Calls add_work(), that converts document into binary form and insert it into the database.

    """
    file = await message.bot.get_file(message.document.file_id)
    file_path = Path(__file__).resolve().parent.parent / "fromtg" / message.document.file_name
    await message.bot.download_file(file.file_path, destination = file_path)
    await asyncio.sleep(3)

    # TODO: subject id из State
    await insert_work(title = message.document.file_name, subject_id = 1, file_path = file_path)

    await state.clear()
    await message.answer("Файл загружен")
    await start_message(message)

