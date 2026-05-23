from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import httpx

from config import OPENAI_API_KEY
from keyboards.keyboards import cancel_keyboard, main_menu_keyboard

router = Router()

SYSTEM_PROMPT = """Siz O'zbekiston Respublikasining yuridik maslahatchi botisiz. 
Faqat O'zbekiston qonunchiligiga asoslanib javob bering.
Javoblaringizda quyidagilarga amal qiling:
1. Aniq va tushunarli til ishlating (oddiy fuqaro uchun)
2. Tegishli qonun moddasini ko'rsating (agar bilsangiz)
3. Kerak bo'lsa, keyingi qadam sifatida qanday hujjat kerakligini ayting
4. Muhim: Siz faqat boshlang'ich maslahat berasiz, advokat o'rnini bosa olmaysiz
5. Javob oxirida: "⚠️ Bu boshlang'ich maslahat bo'lib, to'liq huquqiy yordam uchun advokatga murojaat qiling" deb yozing
"""


class AIForm(StatesGroup):
    waiting_question = State()


@router.callback_query(F.data == "menu_ai")
async def start_ai(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AIForm.waiting_question)
    await callback.message.edit_text(
        "🤖 <b>AI Huquqiy Maslahat</b>\n\n"
        "Huquqiy muammoingizni yozing, men O'zbekiston qonunchiligiga asoslanib javob beraman.\n\n"
        "<i>Misol: \"Do'kon sotib olgan kiyimimni qaytarib olmayapti, nima qilay?\"</i>",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )


@router.message(AIForm.waiting_question)
async def process_ai_question(message: Message, state: FSMContext):
    await state.clear()
    thinking_msg = await message.answer("🤔 Savol tahlil qilinmoqda...")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": message.text}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.7
                }
            )
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
    except Exception as e:
        answer = (
            "❌ AI xizmati hozircha mavjud emas. "
            "Iltimos, keyinroq urinib ko'ring yoki adminга murojaat qiling."
        )

    await thinking_msg.delete()
    await message.answer(
        f"⚖️ <b>Huquqiy Maslahat:</b>\n\n{answer}",
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )
