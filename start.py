from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards.keyboards import main_menu_keyboard
from utils.database import save_user

router = Router()

WELCOME_TEXT = """
⚖️ <b>Yuridik Yordamchi Botiga Xush Kelibsiz!</b>

Men sizga quyidagi xizmatlarni taqdim etaman:

📄 <b>Hujjatlar Konstruktori</b>
— Ijara, Oldi-sotdi, Tilxat shartnomalari

🤖 <b>AI Huquqiy Maslahat</b>
— O'zbekiston qonunchiligiga asoslangan bepul maslahat

Xizmatdan foydalanish uchun quyidagi tugmalardan birini tanlang 👇
"""


@router.message(CommandStart())
async def cmd_start(message: Message):
    await save_user(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name or ""
    )
    await message.answer(
        WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )


@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )


@router.callback_query(F.data == "menu_info")
async def show_info(callback: CallbackQuery):
    text = """
ℹ️ <b>Bot haqida</b>

Bu bot O'zbekiston qonunchiligiga asoslangan yuridik hujjatlarni avtomatik tarzda generatsiya qiladi.

📌 <b>Xizmatlar narxi:</b>
• Ijara shartnomasi — 10,000 so'm
• Oldi-sotdi shartnomasi — 10,000 so'm
• Tilxat — 10,000 so'm
• AI Maslahat — 10,000 so'm/savol

📞 <b>Murojaat uchun:</b> @admin_username
    """
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )
