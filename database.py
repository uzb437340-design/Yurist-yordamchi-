import aiosqlite
import logging
from datetime import datetime

DB_PATH = "yuridik_bot.db"
logger = logging.getLogger(__name__)


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                language TEXT DEFAULT 'uz',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                doc_type TEXT,
                amount INTEGER,
                status TEXT DEFAULT 'pending',
                file_path TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ai_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                question TEXT,
                answer TEXT,
                paid INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
    logger.info("Ma'lumotlar bazasi tayyor.")


async def save_user(user_id: int, username: str, full_name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (user_id, username, full_name)
            VALUES (?, ?, ?)
        """, (user_id, username, full_name))
        await db.commit()


async def create_order(user_id: int, doc_type: str, amount: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO orders (user_id, doc_type, amount, status)
            VALUES (?, ?, ?, 'pending')
        """, (user_id, doc_type, amount))
        await db.commit()
        return cursor.lastrowid


async def update_order_status(order_id: int, status: str, file_path: str = None):
    async with aiosqlite.connect(DB_PATH) as db:
        if file_path:
            await db.execute("""
                UPDATE orders SET status=?, file_path=? WHERE id=?
            """, (status, file_path, order_id))
        else:
            await db.execute("""
                UPDATE orders SET status=? WHERE id=?
            """, (status, order_id))
        await db.commit()


async def get_order(order_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM orders WHERE id=?", (order_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "id": row[0], "user_id": row[1], "doc_type": row[2],
                    "amount": row[3], "status": row[4], "file_path": row[5]
                }
    return None


async def get_stats():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as c:
            users = (await c.fetchone())[0]
        async with db.execute("SELECT COUNT(*), SUM(amount) FROM orders WHERE status='paid'") as c:
            row = await c.fetchone()
            orders, revenue = row[0], row[1] or 0
    return {"users": users, "orders": orders, "revenue": revenue}


async def get_all_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]
