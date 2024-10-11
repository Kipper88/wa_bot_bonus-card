import asyncio
import asyncpg
from asyncio import WindowsSelectorEventLoopPolicy

#asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

class Database:
    def __init__(self, name, password, host, user):
        self.db_password = password
        self.db_name = name
        self.db_host = host
        self.user = user
        
    async def create_conn(self):
        return await asyncpg.connect(
            host=self.db_host,
            port=5432,
            user=self.user,
            password=self.db_password,
            database=self.db_name
        )
        
    async def create_db(self):
        pass
        """ conn = await self.create_conn()
        
        try:
            async with conn.transaction():
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS 'user' (
                        index INT PRIMARY KEY,
                        id BIGINT DEFAULT 0,
                        username VARCHAR DEFAULT NULL,
                        phone VARCHAR NOT NULL,
                        balance BIGINT DEFAULT 0,
                        status VARCHAR DEFAULT 'Серебряная',
                        stamp VARCHAR DEFAULT NULL,
                        bday VARCHAR DEFAULT NULL
                    );
                ''')
                await conn.execute('COMMIT;')
        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")
            raise
        finally:
            await conn.close()  # Закрытие соединения """

    async def query_select(self, query):
        conn = await self.create_conn()
        try:
            data = await conn.fetch(query)  # Получение всех строк, соответствующих запросу
            return data
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            raise
        finally:
            await conn.close()  # Закрытие соединения
           
    async def query_insert(self, query, data):
        conn = await self.create_conn()
        try:
            async with conn.transaction():  # Создаем транзакцию
                await conn.execute(query, 
                        data['id'], data['username'],
                        data['phone'], data['balance'],
                        data['status'], data['stamp'],
                        data['bday'])         # Выполнение запроса
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            raise
        finally:
            await conn.close()  # Закрытие соединения
