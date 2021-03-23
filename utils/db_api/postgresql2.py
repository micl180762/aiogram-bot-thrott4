from typing import Union, Any
import asyncio
import asyncpg
from asyncpg.pool import Pool
from data import config


class Database:
    def __init__(self) -> None:
        self.pool: Union[Pool, None] = None
        # self.pool = None
        pass

    async def create(self):
        pool = await asyncpg.create_pool(
            user=config.PGUSER,
            password = config.PGPASSWORD,
            host = config.IP,
            database = config.DATABASE
        )
        self.pool = pool
        return pool

    async def select_all_users(self):
        # self.pool = await self.create()
        async with self.pool.acquire() as con:
            rez = await con.fetch('SELECT * FROM Usersn')
        print(rez)

    async def add_user(self, id: int, name: str, email: str = None):
        sql = "INSERT INTO Usersn(id, name, email) VALUES ($1, $2, $3)"
        try:
            await self.pool.execute(sql, id, name, email)
        except asyncpg.exceptions.UniqueViolationError:
            pass

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += ' AND '.join([f'{item} = ${num}' for num, item in enumerate(parameters, start=1)])
        return sql, tuple(parameters.values())

    async def select_user(self, **kwargs):
        sql = "SELECT id, name, email, status FROM Usersn WHERE "
        sql, params = self.format_args(sql, kwargs)
        print(sql)
        print(*params)
        return await self.pool.fetchrow(sql, *params)

    async def update_user_status(self, status, id):
        sql = 'UPDATE Usersn SET status = $1 WHERE id = $2'
        return await self.pool.execute(sql, status, id)


# db = Database()
# # db.create()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(db.select_all_users())
# pass

