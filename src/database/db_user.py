from authentication.auth import login_manager
from database.db import db_admin
from database.models import Customer, Invoice


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


async def get_user_invoices(user_id: int):
    cursor = await db_admin.db.async_execute(
        statement="SELECT subscription_id, is_active FROM invoices WHERE customer_id = :user_id",
        params={"user_id": user_id})
    return cursor.fetchall()


async def user_has_already_bought_this_subscription(user_id: int, subscription_id: int) -> bool:
    cursor = await db_admin.db.async_execute(
        statement="SELECT * FROM invoices WHERE customer_id = :user_id AND subscription_id = :subscription_id",
        params={"user_id": user_id, "subscription_id": subscription_id})
    invoice = cursor.fetchone()
    if invoice is not None:
        return True
    return False


async def buy_subscription(user_id: int, subscription_id: int):
    # create invoice
    invoice = Invoice(customer_id=user_id, subscription_id=subscription_id)
    db_admin.db.add(invoice)
    await db_admin.db.commit()
    await db_admin.db.refresh(invoice)


async def activate_subscription(user_id: int, subscription_id: int):
    # activate invoice
    cursor = await db_admin.db.async_execute(
        statement="UPDATE invoices SET is_active = 1 WHERE customer_id = :user_id AND subscription_id = :subscription_id",
        params={"user_id": user_id, "subscription_id": subscription_id})

    cursor = await db_admin.db.async_execute(
        statement="SELECT * FROM invoices WHERE customer_id = :user_id AND subscription_id = :subscription_id",
        params={"user_id": user_id, "subscription_id": subscription_id})
    invoice = cursor.fetchone()
    await db_admin.db.commit()
    return invoice


async def deactivate_subscription(user_id: int, subscription_id: int):
    # deactivate invoice
    cursor = await db_admin.db.async_execute(
        statement="UPDATE invoices SET is_active = 0 WHERE customer_id = :user_id AND subscription_id = :subscription_id",
        params={"user_id": user_id, "subscription_id": subscription_id})

    cursor = await db_admin.db.async_execute(
        statement="SELECT * FROM invoices WHERE customer_id = :user_id AND subscription_id = :subscription_id",
        params={"user_id": user_id, "subscription_id": subscription_id})
    invoice = cursor.fetchone()
    await db_admin.db.commit()
    return invoice
