from surrealdb import Surreal

class Database:
    def __init__(self, url, namespace, database):
        self.client = Surreal(url)
        self.namespace = namespace
        self.database = database

    async def connect(self):
        await self.client.signin({"user": "root", "pass": "root"})
        await self.client.use(self.namespace, self.database)

    async def create_user(self, user_id, username, password):
        await self.client.create("user", {
            "id": user_id,
            "username": username,
            "password": password
        })

    async def get_user(self, username):
        result = await self.client.query(f"SELECT * FROM user WHERE username = '{username}'")
        return result[0] if result else None

db = Database("http://localhost:8000", "test_namespace", "test_database")