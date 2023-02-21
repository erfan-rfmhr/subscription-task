from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    subscriptions = relationship('Subscriptions', back_populates='owners', secondary='invoices')

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, email={self.email})'


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    price = Column(Integer)
    owners = relationship('User', back_populates='subscriptions', secondary='invoices')

    def __repr__(self):
        return f'Subscription(id={self.id}, name={self.name}, price={self.price})'


class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    date = Column(Date)
    price = Column(Integer)
    is_active = Column(Boolean, default=False)

    def __repr__(self):
        return f'Invoice(id={self.id}, user_id={self.user_id}, subscription_id={self.subscription_id},\
        date={self.date}, price={self.price}, is_active={self.is_active})'
