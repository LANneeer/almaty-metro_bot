import asyncio
import asyncpg

from config import vars


class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool: asyncio.pool.Pool = loop.run_until_complete(
            asyncpg.create_pool(
                user=vars.PG_USER,
                password=vars.PG_PASSWORD,
                host=vars.IP
            )
        )

    async def create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS users(
        id INT NOT NULL,
        notes VARCHAR(255),
        advert BOOL
        );
        '''
        await self.pool.execute(sql)

    async def exist_user(self, id: int):
        sql = 'SELECT id FROM users WHERE id = $1'
        return bool(len(await self.pool.fetch(sql, id)))

    async def add_user(self, id: int):
        sql = 'INSERT INTO users(id) VALUES($1)'
        await self.pool.execute(sql, id)

    async def set_notes(self, text: str, id: int):
        sql = 'UPDATE users SET notes = $1 WHERE id = $2'
        await self.pool.execute(sql, text, id)

    async def get_notes(self, id: int):
        sql = 'SELECT notes FROM users WHERE id = $1'
        return await self.pool.fetchval(sql, id)

