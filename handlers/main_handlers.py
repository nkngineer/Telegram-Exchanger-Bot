from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from database.services import add_work, check_user_authorization, add_user, set_user_group, check_group, check_user_profile
from keyboards.inline_keyboard import main_menu, group_menu

from pathlib import Path
import asyncio



class Upload(StatesGroup):
    # waiting_file = State("waiting_file")
    waiting_file = State()


class Text(StatesGroup):
    waiting_username = State()
    waiting_user_group = State()

main_router = Router()





async def start_message(message: Message):
    await message.answer(text="Бот по загрузке лаб", reply_markup=main_menu())


@main_router.message(CommandStart())
async def authorization_user(message: Message, state: FSMContext):
    user_id = message.from_user.id

    is_authorized = await check_user_authorization(user_id)
    print("функция приветствия")
    if is_authorized == False:
        await message.answer("Вы не авторизованы. Введите свои фамилию и имя")
        await state.set_state(Text.waiting_username)

    if is_authorized:
        await start_message(message)


@main_router.message(Text.waiting_username, F.text)
async def edit_user_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    print("функция ожидания ввода имени от пользователя")
    user_answer = message.text

    await state.update_data(waiting_username=user_answer)
    await add_user(user_answer,user_id)
    await message.answer("Фамилия и имя записаны. ")


    await message.answer("Выберите группу", reply_markup=await group_menu())
    await state.set_state(Text.waiting_user_group)


# TODO
@main_router.callback_query(Text.waiting_user_group,F.data)
async def edit_user_group(callback: CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id
    is_group_exist = await check_group(callback.data)
    if not is_group_exist: await callback.answer(text="Такой группы нет!")
    else:
        await set_user_group(callback.data,telegram_id)
        await state.clear()
        await callback.message.edit_text(text=f"Группа {callback.data} выбрана!")
        if await check_user_authorization(telegram_id): await start_message(callback.message)


# TODO: добавить IKB с изменением данных профиля
@main_router.callback_query(F.data == "get_user_profile")
async def get_user_profile(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    user_first_name , user_last_name , user_group = await check_user_profile(telegram_id)
    await callback.message.answer(text=f"Имя : {user_first_name}\nФамилия : {user_last_name}\nГруппа : {user_group}")


@main_router.message(Command("get_file"))
async def cmd_upload(message: Message, state: FSMContext):
    await message.answer("Отправьте файл")
    await state.set_state(Upload.waiting_file)



@main_router.message(Upload.waiting_file, F.document)
async def upload_file_from_user(message: Message, state: FSMContext):
    file = await bot.get_file(message.document.file_id)
    file_path = Path("../fromtg") / message.document.file_name
    await bot.download_file(file.file_path, destination=file_path)
    await asyncio.sleep(3)

    # TODO: создать логику для выбора предмета и автоматического выбора subject_id
    await add_work(subject_id=1,file_path=file_path)

    await state.clear()
    await message.answer("Файл получен")


