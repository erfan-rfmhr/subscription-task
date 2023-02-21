from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DATETIME
from sqlalchemy.orm import relationship

from src.database.db import Base


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    credit = Column(Integer, default=0)
    password = Column(String)
    subscriptions = relationship('Subscription', back_populates='owners', secondary='invoices')

    def __repr__(self):
        return f'Customer(id={self.id}, username={self.username}, email={self.email}), credit={self.credit}'


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    price = Column(Integer)
    owners = relationship('Customer', back_populates='subscriptions', secondary='invoices')

    def __repr__(self):
        return f'Subscription(id={self.id}, name={self.name}, price={self.price})'


class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    start_date = Column(DATETIME, default=datetime.now)
    is_active = Column(Boolean, default=False)

    def __repr__(self):
        return f'Invoice(id={self.id}, customer_id={self.customer_id}, subscription_id={self.subscription_id},\
        start date={self.start_date}, is_active={self.is_active})'
