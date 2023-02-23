from database.db import db_admin
from fastapi_scheduler import SchedulerAdmin

scheduler = SchedulerAdmin.bind(db_admin)


# Define the interval task
async def interval_decrease_credit(user_id: int, cost: int):
    # get user credit
    cursor = await db_admin.db.async_execute(statement="SELECT credit FROM customers WHERE id = :user_id",
                                             params={"user_id": user_id})
    credit = cursor.fetchone()[0]
    print(f"credit: {credit}")
    # decrease credit
    await db_admin.db.async_execute(
        statement="UPDATE customers SET credit = :credit WHERE id = :user_id",
        params={"user_id": user_id, "credit": credit - cost})
    await db_admin.db.commit()
