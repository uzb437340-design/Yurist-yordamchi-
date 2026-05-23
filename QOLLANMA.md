# 🤖 Yuridik Yordamchi Bot — O'rnatish Qo'llanmasi

## 📁 Loyiha tuzilmasi
```
yuridik_bot/
├── main.py              # Botning asosiy fayli
├── config.py            # Konfiguratsiya
├── requirements.txt     # Kutubxonalar
├── Procfile             # Railway uchun
├── .env.example         # Muhit o'zgaruvchilari namunasi
├── handlers/
│   ├── start.py         # /start va bosh menyu
│   ├── documents.py     # Hujjatlar konstruktori
│   ├── payment.py       # To'lov tizimi
│   ├── ai_advisor.py    # AI maslahatchi
│   └── admin.py         # Admin panel
├── keyboards/
│   └── keyboards.py     # Barcha tugmalar
└── utils/
    ├── database.py      # SQLite baza
    └── doc_generator.py # Word hujjat generatsiya
```

---

## 🚀 1-QADAM: Bot Token olish

1. Telegramda **@BotFather** ga o'ting
2. `/newbot` buyrug'ini yuboring
3. Botga nom bering (masalan: `Yuridik Yordamchi`)
4. Username bering (masalan: `yuridik_yordamchi_bot`)
5. BotFather **TOKEN** beradi — uni saqlang!

---

## 🆔 2-QADAM: Admin ID olish

1. Telegramda **@userinfobot** ga yozing
2. U sizning Telegram ID raqamingizni beradi
3. Uni `.env` fayliga yozing

---

## 🤖 3-QADAM: OpenAI API Key (ixtiyoriy)

1. https://platform.openai.com ga kiring
2. "API Keys" bo'limidan yangi key yarating
3. `.env` fayliga qo'ying

> **Eslatma:** OpenAI pullik. Agar kerak bo'lmasa, AI maslahat funksiyasini o'chirib qo'yishingiz mumkin.

---

## ☁️ 4-QADAM: Railway.app ga Deploy (BEPUL)

### 4.1. GitHub'ga yuklash
1. https://github.com ga kiring (hisob oching)
2. "New Repository" bosing → nom bering
3. Barcha fayllarni yukang

### 4.2. Railway'da deploy
1. https://railway.app ga kiring
2. GitHub bilan bog'lang
3. "New Project" → "Deploy from GitHub repo"
4. Repozitoriyangizni tanlang

### 4.3. Muhit o'zgaruvchilarini qo'shish
Railway dashboard'da **Variables** bo'limiga o'ting:
```
BOT_TOKEN = 1234567890:ABCdef...
OPENAI_API_KEY = sk-...
ADMIN_IDS = 987654321
```

### 4.4. Deploy!
Railway avtomatik `requirements.txt` ni o'qib, botni ishga tushiradi.

---

## 💻 LOCAL (Kompyuterda) Ishga Tushirish

```bash
# 1. Papkaga kiring
cd yuridik_bot

# 2. .env fayl yarating
cp .env.example .env
# .env faylini oching va ma'lumotlarni kiriting

# 3. Kutubxonalarni o'rnating
pip install -r requirements.txt

# 4. Botni ishga tushiring
python main.py
```

---

## 📱 Botdan Foydalanish

| Buyruq | Vazifasi |
|--------|----------|
| `/start` | Botni ishga tushirish |
| `/admin` | Admin panelni ochish (faqat adminlar) |

### Foydalanuvchi uchun:
1. `/start` → Bosh menyu
2. **Hujjat olish** → Tur tanlash → Savollar → To'lov → Hujjat
3. **AI Maslahat** → Savol yozish → Javob

### Admin uchun:
1. `/admin` → Admin menyu
2. **Statistika** → Foydalanuvchilar va daromad
3. **Xabar tarqatish** → Barcha foydalanuvchilarga xabar

---

## 💳 Haqiqiy To'lov Ulash (Kelajak uchun)

Hozir "Demo" rejimda ishlaydi. Haqiqiy Click/Payme ulash uchun:

1. **Click** → https://my.click.uz → Merchant ro'yxatdan o'tish
2. **Payme** → https://payme.uz → Biznes hisob ochish
3. API kalitlarni olib, `handlers/payment.py` ga ulash

---

## ❓ Muammolar

**Bot javob bermayapti:**
- Token to'g'ri kiritilganini tekshiring
- Railway'da bot ishlayotganini ko'ring (Logs bo'limi)

**Hujjat yaratilmayapti:**
- `generated_docs/` papkasi mavjudligini tekshiring
- `python-docx` o'rnatilganini tekshiring

**AI javob bermayapti:**
- OpenAI API key to'g'riligini tekshiring
- OpenAI hisobingizda kredit borligini tekshiring

---

## 📞 Yordam kerakmi?

Muammo bo'lsa, admin bilan bog'laning.
