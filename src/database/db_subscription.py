from .db import db_admin
from .models import Subscription


async def create_subscriptions():
    cursor = await db_admin.db.execute("SELECT * FROM subscriptions")
    if len(cursor.fetchall()) == 0:
        sub1 = Subscription(name="Subscription 1", price=10)
        sub2 = Subscription(name="Subscription 2", price=20)
        sub3 = Subscription(name="Subscription 3", price=30)
        db_admin.db.add_all([sub1, sub2, sub3])
        await db_admin.db.commit()
        await db_admin.db.refresh(sub1)
        await db_admin.db.refresh(sub2)
        await db_admin.db.refresh(sub3)


async def get_subscription_price(subscription_id: int):
    cursor = await db_admin.db.execute(
        statement="SELECT price FROM subscriptions WHERE id = :subscription_id",
        params={"subscription_id": subscription_id})
    return cursor.fetchone()[0]
