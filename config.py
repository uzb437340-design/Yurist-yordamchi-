import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_KEY_HERE")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "123456789").split(",")))

# Narxlar (so'm)
PRICES = {
    "ijara": 10000,
    "oldi_sotdi": 10000,
    "tilxat": 10000,
    "ai_maslahat": 10000,
}

DATABASE_URL = os.getenv("DATABASE_URL", "yuridik_bot.db")
