from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 Hujjat olish", callback_data="menu_docs")],
        [InlineKeyboardButton(text="🤖 AI Huquqiy maslahat", callback_data="menu_ai")],
        [InlineKeyboardButton(text="ℹ️ Ma'lumot", callback_data="menu_info")],
    ])
    return keyboard


def documents_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Ijara shartnomasi - 10,000 so'm", callback_data="doc_ijara")],
        [InlineKeyboardButton(text="🤝 Oldi-sotdi shartnomasi - 10,000 so'm", callback_data="doc_oldi_sotdi")],
        [InlineKeyboardButton(text="✍️ Tilxat - 10,000 so'm", callback_data="doc_tilxat")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_main")],
    ])
    return keyboard


def payment_keyboard(order_id: int, amount: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"💳 To'lash ({amount:,} so'm)",
            callback_data=f"pay_{order_id}"
        )],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="back_main")],
    ])
    return keyboard


def confirm_payment_keyboard(order_id: int):
    """Demo uchun: haqiqiy to'lov tasdiqlash tugmasi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ To'lovni tasdiqlash (Demo)", callback_data=f"confirm_pay_{order_id}")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_main")],
    ])
    return keyboard


def admin_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📢 Xabar tarqatish", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="⬅️ Bosh menyu", callback_data="back_main")],
    ])
    return keyboard


def cancel_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="back_main")],
    ])
    return keyboard
