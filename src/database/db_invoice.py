from database.db import db_admin
from database.models import Invoice


async def get_user_invoices(user_id: int):
    cursor = await db_admin.db.async_execute(
        statement="SELECT * FROM invoices WHERE customer_id = :user_id",
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
