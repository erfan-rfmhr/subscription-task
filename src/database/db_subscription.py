from .db import db_admin
from .models import Subscription


async def create_subscriptions():
    cursor = await db_admin.db.execute("SELECT * FROM subscriptions")
    if len(cursor.fetchall()) == 0:
        sub1 = Subscription(name="Product 1", price=10)
        sub2 = Subscription(name="Product 2", price=20)
        sub3 = Subscription(name="Product 3", price=30)
        db_admin.db.add_all([sub1, sub2, sub3])
        await db_admin.db.commit()
        await db_admin.db.refresh(sub1)
        await db_admin.db.refresh(sub2)
        await db_admin.db.refresh(sub3)
