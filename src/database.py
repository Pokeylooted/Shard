from surrealdb import Surreal
import logging

class Database:
    def __init__(self, url, namespace, database):
        self.client = Surreal(url)
        self.namespace = namespace
        self.database = database

    async def connect(self):
        try:
            await self.client.connect()
            await self.client.signin({"user": "root", "pass": "root"})
            await self.client.use(self.namespace, self.database)
            logging.info("Successfully connected to the database.")
        except Exception as e:
            logging.error(f"Failed to connect to the database: {e}")

    async def create_user(self, user_id, username, password):
        await self.client.create("user", {
            "id": user_id,
            "username": username,
            "password": password
        })

    async def get_user(self, username):
        result = await self.client.query(f"SELECT * FROM user WHERE username = '{username}'")
        return result[0] if result else None

db = Database("ws://surrealdb:8000/rpc", "test_namespace", "test_database")