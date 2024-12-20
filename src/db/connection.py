import asyncpg

from core.config import settings


DATABASE_URL = settings.DATABASE_URL


async def get_db():
    pool = await asyncpg.create_pool(DATABASE_URL)
    try:
        yield pool
    finally:
        await pool.close()
