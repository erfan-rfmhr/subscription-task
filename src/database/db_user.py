from src.database.db import db_admin
from src.database.models import Customer


def add_user(username, email, password):
    user = Customer(username=username, email=email, password=password)
    db_admin.db.add(user)
    db_admin.db.commit()
    db_admin.db.refresh(user)
    return user
