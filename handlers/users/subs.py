from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
import re
from loader import dp, db
from aiogram import types
from keyboards.inline.choice_buttons import user_keyboard
from keyboards.inline.callback_datas import choise_callback
# from utils.habr.habr_users import get_habr_user
from utils.misc import rate_limit
from utils.habr.HabrUser import get_user_tags


@rate_limit(limit=4)
@dp.message_handler(Command('subscribe'), state=None)
async def show_items(message: types.Message, user: dict, state: FSMContext):
    await message.answer(f"<b>{user['name']}</b>, выберите параметры рассылки.\n"
                         f"Ваш текущий статус <b>{user['status_ru']}</b> Неинтересно - Отмена", reply_markup= user_keyboard(user['status']))


# нажата кнопка посты профиля
@dp.callback_query_handler(choise_callback.filter(post_type_choise='profile_posts'))
async def get_profile_posts(call: CallbackQuery, state: FSMContext, callback_data: dict):
    print(call.message.from_user)
    await state.set_state('set_profile')
    await call.message.answer(f'<b>{call.message.chat.full_name}</b>, '
                              f'Введите имя существующего профиля Хабра; canсel - отмена')  #,reply_markup=choice_cansel)
    await call.message.edit_reply_markup()


# нажата кнопка все посты
@dp.callback_query_handler(choise_callback.filter(post_type_choise='all_posts'))
async def get_all_posts(call: CallbackQuery, callback_data: dict):
    # await bot.answer_callback_query(callback_query_id=call.id)
    # можно так часики закрыть )) cache_time - чтобы не ловил нажатие и еще раз не обраб update
    await call.answer(cache_time=60)
    print(f'call.data={call.data}')
    print(f'callback_data={callback_data}')
    await db.update_user_status('all_posts', call.message.chat.id)
    await call.message.answer(f'<b>{call.message.chat.full_name}</b>, Вы подписаны <b>на все посты</b> с Хабра!')
    await call.message.edit_reply_markup()


@dp.callback_query_handler(choise_callback.filter(post_type_choise='cancel'))  # text - это не text из назв кнопки а из callback_data
async def cancel(call: CallbackQuery):
    await call.answer('Отмена! Параметры подписки остались прежними', show_alert=True)
    await call.message.edit_reply_markup()


@dp.callback_query_handler(choise_callback.filter(post_type_choise='cancel_allez'))
async def cancel_allez(call: CallbackQuery):
    await call.answer('Вы <b>отписались</b> от всех постов Хабра', show_alert=True)
    await db.update_user_status('new_user', call.message.chat.id)
    await call.message.edit_reply_markup()


@dp.message_handler(state='set_profile')
async def subscr_cancel(message: types.Message, state: FSMContext, user: dict):
    template = r'[a-zA-Z0-9_-]+'
    if re.fullmatch(template, message.text) is None:
        await message.answer(f"<b>{user['name']}</b>, вы пытаетесь ввести недопустимые в имени профиля символы;\n"
                             f"попробуйте еще; canсel - отмена")
        return

    if message.text == 'cancel':
        await state.finish()
        await message.answer(f"<b>{user['name']}</b>, ваш статус подписки на Хабре остался прежним - <b>{user['status']}</b>")
        return

    if get_user_tags(message.text):
        await state.finish()
        await db.update_user_status(message.text, message.chat.id)
        await message.answer(f"<b>{user['name']}</b>Теперь вы будете получать посты по хабам профиля "
                             f"<b>{message.text}</b>")
    else:
        await message.answer(f"<b>{user['name']}</b>, на Хабре профиля <b>{message.text}</b> нет\n!"
                             f"попробуйте еще; canсel - отмена")


