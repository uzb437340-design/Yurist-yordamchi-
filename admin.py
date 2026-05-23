from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import ADMIN_IDS
from utils.database import get_stats, get_all_users
from keyboards.keyboards import admin_keyboard, main_menu_keyboard

router = Router()


class BroadcastForm(StatesGroup):
    waiting_message = State()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q.")
        return

    await message.answer(
        "👨‍💼 <b>Admin Panel</b>\n\nBoshqaruv panelga xush kelibsiz!",
        parse_mode="HTML",
        reply_markup=admin_keyboard()
    )


@router.callback_query(F.data == "admin_stats")
async def show_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!", show_alert=True)
        return

    stats = await get_stats()
    text = f"""
📊 <b>Statistika</b>

👥 Jami foydalanuvchilar: <b>{stats['users']}</b>
📄 Jami buyurtmalar: <b>{stats['orders']}</b>
💰 Jami daromad: <b>{stats['revenue']:,} so'm</b>
    """
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=admin_keyboard()
    )


@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!", show_alert=True)
        return

    await state.set_state(BroadcastForm.waiting_message)
    await callback.message.edit_text(
        "📢 <b>Xabar tarqatish</b>\n\nBarcha foydalanuvchilarga yuboriladigan xabarni yozing:",
        parse_mode="HTML"
    )


@router.message(BroadcastForm.waiting_message)
async def send_broadcast(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    users = await get_all_users()
    sent = 0
    failed = 0

    progress_msg = await message.answer(f"📤 Yuborilmoqda... 0/{len(users)}")

    for i, user_id in enumerate(users):
        try:
            await message.bot.send_message(
                user_id,
                f"📢 <b>Yangilik:</b>\n\n{message.text}",
                parse_mode="HTML"
            )
            sent += 1
        except Exception:
            failed += 1

        if (i + 1) % 10 == 0:
            await progress_msg.edit_text(f"📤 Yuborilmoqda... {i+1}/{len(users)}")

    await progress_msg.edit_text(
        f"✅ <b>Xabar tarqatildi!</b>\n\n"
        f"✅ Muvaffaqiyatli: {sent}\n"
        f"❌ Xato: {failed}",
        parse_mode="HTML",
        reply_markup=admin_keyboard()
    )
