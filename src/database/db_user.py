from authentication.auth import login_manager
from database.db import db_admin
from database.models import Customer


async def add_user(username, password):
    user = Customer(username=username, password=password)
    db_admin.db.add(user)
    await db_admin.db.commit()
    await db_admin.db.refresh(user)


@login_manager.user_loader()
async def get_user_by_username(username):
    cursor = await db_admin.db.async_execute(statement="SELECT * FROM customers WHERE username = :username",
                                             params={"username": username})
    return cursor.fetchone()


async def get_user(username: str):
    cursor = await db_admin.db.async_execute(statement="SELECT * FROM customers WHERE username = :username",
                                             params={"username": username})
    return cursor.fetchone()
