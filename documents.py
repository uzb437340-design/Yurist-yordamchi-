from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import documents_keyboard, payment_keyboard, cancel_keyboard
from utils.database import create_order
from config import PRICES

router = Router()


class IjaraForm(StatesGroup):
    beruvchi_fio = State()
    beruvchi_pasport = State()
    oluvchi_fio = State()
    oluvchi_pasport = State()
    manzil = State()
    narx = State()
    muddat = State()
    shahar = State()


class OldiSotdiForm(StatesGroup):
    sotuvchi_fio = State()
    sotuvchi_pasport = State()
    xaridor_fio = State()
    xaridor_pasport = State()
    tovar = State()
    narx = State()
    shahar = State()


class TilxatForm(StatesGroup):
    fio = State()
    pasport = State()
    manzil = State()
    mazmun = State()
    miqdor = State()
    shahar = State()


# ─── Hujjatlar menyusi ───────────────────────────────────────────────────────

@router.callback_query(F.data == "menu_docs")
async def show_documents(callback: CallbackQuery):
    await callback.message.edit_text(
        "📂 <b>Hujjat turini tanlang:</b>",
        parse_mode="HTML",
        reply_markup=documents_keyboard()
    )


# ─── IJARA SHARTNOMASI ────────────────────────────────────────────────────────

@router.callback_query(F.data == "doc_ijara")
async def start_ijara(callback: CallbackQuery, state: FSMContext):
    await state.set_state(IjaraForm.beruvchi_fio)
    await callback.message.edit_text(
        "🏠 <b>Ijara Shartnomasi</b>\n\n"
        "Savollarga javob bering, bot shartnomani avtomatik tuzadi.\n\n"
        "1️⃣ <b>Ijara beruvchining to'liq ismi familiyasi:</b>",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )


@router.message(IjaraForm.beruvchi_fio)
async def ijara_beruvchi_pasport(message: Message, state: FSMContext):
    await state.update_data(beruvchi_fio=message.text)
    await state.set_state(IjaraForm.beruvchi_pasport)
    await message.answer("2️⃣ <b>Ijara beruvchining pasport seriyasi va raqami</b>\n(Masalan: AB1234567):", parse_mode="HTML")


@router.message(IjaraForm.beruvchi_pasport)
async def ijara_oluvchi_fio(message: Message, state: FSMContext):
    await state.update_data(beruvchi_pasport=message.text)
    await state.set_state(IjaraForm.oluvchi_fio)
    await message.answer("3️⃣ <b>Ijara oluvchining to'liq ismi familiyasi:</b>", parse_mode="HTML")


@router.message(IjaraForm.oluvchi_fio)
async def ijara_oluvchi_pasport(message: Message, state: FSMContext):
    await state.update_data(oluvchi_fio=message.text)
    await state.set_state(IjaraForm.oluvchi_pasport)
    await message.answer("4️⃣ <b>Ijara oluvchining pasport seriyasi va raqami:</b>", parse_mode="HTML")


@router.message(IjaraForm.oluvchi_pasport)
async def ijara_manzil(message: Message, state: FSMContext):
    await state.update_data(oluvchi_pasport=message.text)
    await state.set_state(IjaraForm.manzil)
    await message.answer("5️⃣ <b>Ijaradagi mulkning to'liq manzili:</b>", parse_mode="HTML")


@router.message(IjaraForm.manzil)
async def ijara_narx(message: Message, state: FSMContext):
    await state.update_data(manzil=message.text)
    await state.set_state(IjaraForm.narx)
    await message.answer("6️⃣ <b>Oylik ijara haqi (so'mda):</b>\n(Masalan: 1,500,000)", parse_mode="HTML")


@router.message(IjaraForm.narx)
async def ijara_muddat(message: Message, state: FSMContext):
    await state.update_data(narx=message.text)
    await state.set_state(IjaraForm.muddat)
    await message.answer("7️⃣ <b>Ijara muddati (oyda):</b>\n(Masalan: 12)", parse_mode="HTML")


@router.message(IjaraForm.muddat)
async def ijara_shahar(message: Message, state: FSMContext):
    await state.update_data(muddat=message.text)
    await state.set_state(IjaraForm.shahar)
    await message.answer("8️⃣ <b>Shartnoma tuzilgan shahar:</b>\n(Masalan: Toshkent)", parse_mode="HTML")


@router.message(IjaraForm.shahar)
async def ijara_finish(message: Message, state: FSMContext):
    await state.update_data(shahar=message.text)
    data = await state.get_data()
    await state.clear()

    # Order yaratish
    order_id = await create_order(message.from_user.id, "ijara", PRICES["ijara"])

    # Ma'lumotlarni saqlash uchun state'ni yangilash
    import json
    with open(f"generated_docs/order_{order_id}_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    summary = f"""
✅ <b>Ma'lumotlar qabul qilindi!</b>

📋 <b>Shartnoma xulosasi:</b>
• Ijara beruvchi: {data['beruvchi_fio']}
• Ijara oluvchi: {data['oluvchi_fio']}
• Manzil: {data['manzil']}
• Oylik ijara: {data['narx']} so'm
• Muddat: {data['muddat']} oy

💳 Shartnomani yuklab olish uchun to'lov qiling:
    """
    await message.answer(
        summary,
        parse_mode="HTML",
        reply_markup=payment_keyboard(order_id, PRICES["ijara"])
    )


# ─── OLDI-SOTDI SHARTNOMASI ───────────────────────────────────────────────────

@router.callback_query(F.data == "doc_oldi_sotdi")
async def start_oldi_sotdi(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OldiSotdiForm.sotuvchi_fio)
    await callback.message.edit_text(
        "🤝 <b>Oldi-Sotdi Shartnomasi</b>\n\n"
        "1️⃣ <b>Sotuvchining to'liq ismi familiyasi:</b>",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )


@router.message(OldiSotdiForm.sotuvchi_fio)
async def os_sotuvchi_pasport(message: Message, state: FSMContext):
    await state.update_data(sotuvchi_fio=message.text)
    await state.set_state(OldiSotdiForm.sotuvchi_pasport)
    await message.answer("2️⃣ <b>Sotuvchining pasport seriyasi va raqami:</b>", parse_mode="HTML")


@router.message(OldiSotdiForm.sotuvchi_pasport)
async def os_xaridor_fio(message: Message, state: FSMContext):
    await state.update_data(sotuvchi_pasport=message.text)
    await state.set_state(OldiSotdiForm.xaridor_fio)
    await message.answer("3️⃣ <b>Xaridorning to'liq ismi familiyasi:</b>", parse_mode="HTML")


@router.message(OldiSotdiForm.xaridor_fio)
async def os_xaridor_pasport(message: Message, state: FSMContext):
    await state.update_data(xaridor_fio=message.text)
    await state.set_state(OldiSotdiForm.xaridor_pasport)
    await message.answer("4️⃣ <b>Xaridorning pasport seriyasi va raqami:</b>", parse_mode="HTML")


@router.message(OldiSotdiForm.xaridor_pasport)
async def os_tovar(message: Message, state: FSMContext):
    await state.update_data(xaridor_pasport=message.text)
    await state.set_state(OldiSotdiForm.tovar)
    await message.answer("5️⃣ <b>Sotilayotgan mulk/tovarning tavsifi:</b>\n(Masalan: 2020-yil Nexia 3 avtomobili)", parse_mode="HTML")


@router.message(OldiSotdiForm.tovar)
async def os_narx(message: Message, state: FSMContext):
    await state.update_data(tovar=message.text)
    await state.set_state(OldiSotdiForm.narx)
    await message.answer("6️⃣ <b>Mulkning narxi (so'mda):</b>", parse_mode="HTML")


@router.message(OldiSotdiForm.narx)
async def os_shahar(message: Message, state: FSMContext):
    await state.update_data(narx=message.text)
    await state.set_state(OldiSotdiForm.shahar)
    await message.answer("7️⃣ <b>Shartnoma tuzilgan shahar:</b>", parse_mode="HTML")


@router.message(OldiSotdiForm.shahar)
async def os_finish(message: Message, state: FSMContext):
    await state.update_data(shahar=message.text)
    data = await state.get_data()
    await state.clear()

    order_id = await create_order(message.from_user.id, "oldi_sotdi", PRICES["oldi_sotdi"])

    import json
    with open(f"generated_docs/order_{order_id}_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    summary = f"""
✅ <b>Ma'lumotlar qabul qilindi!</b>

📋 <b>Shartnoma xulosasi:</b>
• Sotuvchi: {data['sotuvchi_fio']}
• Xaridor: {data['xaridor_fio']}
• Mulk: {data['tovar']}
• Narx: {data['narx']} so'm

💳 Shartnomani yuklab olish uchun to'lov qiling:
    """
    await message.answer(
        summary,
        parse_mode="HTML",
        reply_markup=payment_keyboard(order_id, PRICES["oldi_sotdi"])
    )


# ─── TILXAT ───────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "doc_tilxat")
async def start_tilxat(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TilxatForm.fio)
    await callback.message.edit_text(
        "✍️ <b>Tilxat</b>\n\n"
        "1️⃣ <b>Tilxat yozuvchining to'liq ismi familiyasi:</b>",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )


@router.message(TilxatForm.fio)
async def tilxat_pasport(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(TilxatForm.pasport)
    await message.answer("2️⃣ <b>Pasport seriyasi va raqami:</b>", parse_mode="HTML")


@router.message(TilxatForm.pasport)
async def tilxat_manzil(message: Message, state: FSMContext):
    await state.update_data(pasport=message.text)
    await state.set_state(TilxatForm.manzil)
    await message.answer("3️⃣ <b>Yashash manzili:</b>", parse_mode="HTML")


@router.message(TilxatForm.manzil)
async def tilxat_mazmun(message: Message, state: FSMContext):
    await state.update_data(manzil=message.text)
    await state.set_state(TilxatForm.mazmun)
    await message.answer(
        "4️⃣ <b>Tilxat mazmuni:</b>\n"
        "(Masalan: Men Aliyev Sardordan 5,000,000 so'm qarz oldim va 3 oy ichida qaytaraman)",
        parse_mode="HTML"
    )


@router.message(TilxatForm.mazmun)
async def tilxat_miqdor(message: Message, state: FSMContext):
    await state.update_data(mazmun=message.text)
    await state.set_state(TilxatForm.miqdor)
    await message.answer("5️⃣ <b>Miqdori (so'mda):</b>", parse_mode="HTML")


@router.message(TilxatForm.miqdor)
async def tilxat_shahar(message: Message, state: FSMContext):
    await state.update_data(miqdor=message.text)
    await state.set_state(TilxatForm.shahar)
    await message.answer("6️⃣ <b>Shahar:</b>", parse_mode="HTML")


@router.message(TilxatForm.shahar)
async def tilxat_finish(message: Message, state: FSMContext):
    await state.update_data(shahar=message.text)
    data = await state.get_data()
    await state.clear()

    order_id = await create_order(message.from_user.id, "tilxat", PRICES["tilxat"])

    import json
    with open(f"generated_docs/order_{order_id}_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    summary = f"""
✅ <b>Ma'lumotlar qabul qilindi!</b>

📋 <b>Tilxat xulosasi:</b>
• Muallif: {data['fio']}
• Manzil: {data['manzil']}
• Miqdor: {data['miqdor']} so'm

💳 Tilxatni yuklab olish uchun to'lov qiling:
    """
    await message.answer(
        summary,
        parse_mode="HTML",
        reply_markup=payment_keyboard(order_id, PRICES["tilxat"])
    )
