from loader import dp

from keyboards.inline.menu_keyboards.menu_callback_datas import start_menu_callback
from keyboards.inline.menu_keyboards.menu_buttoms import menu_editmsg_back_keyboard, menu_newmsg_back_keyboard
from states.menu_states import ShortcutScanState
from utils.menu_utils import shortcut_apies  
from utils.db_api.models_peewee import *

from aiogram.dispatcher.storage import FSMContext
from aiogram import types


@dp.callback_query_handler(start_menu_callback.filter(category="shortcut_scan"))
async def set_shortcut_state(call: types.CallbackQuery):
    await call.answer(cache_time=0)  
    await call.message.edit_text("Введите ссылку, которую требуется расшифровать")
    await ShortcutScanState.shortcut_scan_data.set()



@dp.message_handler(state=ShortcutScanState.shortcut_scan_data)
async def send_shortcut_url(message: types.Message, state: FSMContext):
    await message.delete()
    print('scan')
    error = False
    try:
        shortcut_func = getattr(shortcut_apies, "tinyurl")
        shortcut_url = shortcut_func(message.text, False)
    except Exception as e:
        print("short_scan_err", e.args)
        print(e)
        print(shortcut_url)
        error = True
        try:
            shortcut_func = getattr(shortcut_apies, "chilpit")
            shortcut_url = shortcut_func(message.text, False)
        except Exception as e:
            print("short_scan_err2", e.args)
            print(e)
            print(shortcut_url)
            await message.answer(text = "я не могу расшифровать данную ссылку(", reply_markup=menu_editmsg_back_keyboard)
            await state.finish()
        else:
            error = False
            
        
       
    if not error:
        text = f"<code>{message.text}</code>\n\
                                \n------------------------>\
                                    \n\n<code>{shortcut_url[1]}</code>"
        await message.answer(text = text, reply_markup=menu_newmsg_back_keyboard)
        await state.finish()



