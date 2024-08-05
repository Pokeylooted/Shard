from surrealdb import Surreal
import logging
logging.getLogger().setLevel(logging.DEBUG)

SURREALDB_WS_URL = "ws://surrealdb:5000/rpc" 

@DeprecationWarning
async def insert_user_into_surreal(username, passwordhash, role):
    async with Surreal(SURREALDB_WS_URL) as db:
      
        await db.use("test_namespace", "test_database") 

        # Create a new user
        response = await db.create(
            "user",
            {
                "username": username,   
                "passwordhash": passwordhash,
                "role": role
            },
        ) 

        user_id = response[0]['id']  # Extract the ID from the response
        logging.info(f"User {username} created with ID {user_id}")
        return user_id.removeprefix("user:")  # Return the ID

@DeprecationWarning
async def get_user_from_db(userid):
    async with Surreal(SURREALDB_WS_URL) as db:
        await db.use("test_namespace", "test_database")
        print(f"user:{userid}")
        user = await db.select(f"user:{userid}")
        # user = await db.query(f"SELECT * FROM user WHERE id = '{userid}'")
        print("User is: " + str(user))
        return user
@DeprecationWarning
async def login_user_db(username: str, passwordhash: str):
    async with Surreal(SURREALDB_WS_URL) as db:
        await db.use("test_namespace", "test_database")
        user = await db.query(f"SELECT * FROM user WHERE username = '{username}' AND password = '{passwordhash}'")
        return user[0]['result'][0]['id'] if user[0]['result'] else None