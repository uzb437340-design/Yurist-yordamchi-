import json
import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from utils.database import get_order, update_order_status
from utils.doc_generator import generate_ijara_shartnoma, generate_oldi_sotdi, generate_tilxat
from keyboards.keyboards import main_menu_keyboard, confirm_payment_keyboard

router = Router()


@router.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[1])
    order = await get_order(order_id)

    if not order:
        await callback.answer("Buyurtma topilmadi!", show_alert=True)
        return

    # Demo rejimida to'lov tasdiqlash tugmasi ko'rsatiladi
    # Haqiqiy loyihada shu yerda Click/Payme invoice yaratiladi
    text = f"""
💳 <b>To'lov</b>

📦 Buyurtma #{order_id}
💰 Miqdor: {order['amount']:,} so'm

<i>Demo rejim: Quyidagi tugma orqali to'lovni tasdiqlang.</i>
<i>Haqiqiy rejimda Click/Payme orqali to'lanadi.</i>
    """
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=confirm_payment_keyboard(order_id)
    )


@router.callback_query(F.data.startswith("confirm_pay_"))
async def confirm_payment(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[2])
    order = await get_order(order_id)

    if not order:
        await callback.answer("Buyurtma topilmadi!", show_alert=True)
        return

    await callback.message.edit_text("⏳ Hujjat tayyorlanmoqda...")

    # Ma'lumotlarni yuklash
    data_file = f"generated_docs/order_{order_id}_data.json"
    if not os.path.exists(data_file):
        await callback.message.edit_text("❌ Ma'lumotlar topilmadi.")
        return

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Hujjat generatsiya
    doc_type = order["doc_type"]
    if doc_type == "ijara":
        file_path = generate_ijara_shartnoma(data, order_id)
    elif doc_type == "oldi_sotdi":
        file_path = generate_oldi_sotdi(data, order_id)
    elif doc_type == "tilxat":
        file_path = generate_tilxat(data, order_id)
    else:
        await callback.message.edit_text("❌ Noma'lum hujjat turi.")
        return

    await update_order_status(order_id, "paid", file_path)

    # Faylni yuborish
    doc_file = FSInputFile(file_path)
    await callback.message.answer_document(
        doc_file,
        caption=(
            "✅ <b>To'lov tasdiqlandi!</b>\n\n"
            "📄 Sizning hujjatingiz tayyor.\n"
            "Word (.docx) formatida yuborildi — bosib chiqarib imzolashingiz mumkin.\n\n"
            "🙏 Xizmatdan foydalanganingiz uchun rahmat!"
        ),
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )
    await callback.message.delete()

    # Temp faylni o'chirish
    try:
        os.remove(data_file)
    except Exception:
        pass
