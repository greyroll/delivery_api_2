from pathlib import Path

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from classes.app_manager import AppManager
from orm_managers.cart_manager import CartOrderORMManager
from orm_models import UserORMModel, DeliveryItemORMModel, DeliveryCategoryORMModel, ItemOrder, OrderORMModel


app_manager = AppManager()
app_manager.items_manager.create_all_tables()
