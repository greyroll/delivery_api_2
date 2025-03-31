from sqlmodel import Session, select
from datetime import datetime

from orm_managers import BaseORMManager
from orm_models import DeliveryItemORMModel
from orm_models.user import UserORMModel
from orm_models.item_order import ItemOrder
from orm_models.order import OrderORMModel


class CartOrderORMManager(BaseORMManager):
    model = OrderORMModel

    def has_active_order(self, user_id: int) -> bool:
            result = self.get_active_order_by_user_id(user_id)
            return result is not None

    def get_active_order_by_user_id(self, user_id: int) -> OrderORMModel | None:
        with Session(self.engine) as session:
            statement = select(OrderORMModel).where(
                OrderORMModel.user_id == user_id,
                OrderORMModel.status == "pending"
            )
            return session.exec(statement).first()

    def create_order(self, user_id: int) -> OrderORMModel:
        with Session(self.engine) as session:
            order = OrderORMModel(
                user_id=user_id,
                status="pending",
                created_at=datetime.now(),
                total=0.0,
                address=""
            )
            session.add(order)
            session.commit()
            session.refresh(order)
            return order

    def add_to_cart(self, item_id: int, user_id: int, quantity: int = 1):
        with Session(self.engine) as session:
            statement = select(OrderORMModel).where(
                OrderORMModel.user_id == user_id,
                OrderORMModel.status == "pending"
            )
            order = session.exec(statement).first()

            if order is None:
                order = self.create_order(user_id)

            statement = select(DeliveryItemORMModel).where(DeliveryItemORMModel.id == item_id)
            item: DeliveryItemORMModel = session.exec(statement).first()

            statement = select(ItemOrder).where(
                ItemOrder.order_id == order.id,
                ItemOrder.item_id == item_id
            )
            item_order = session.exec(statement).first()

            if item_order:
                item_order.quantity += quantity
            else:
                item_order = ItemOrder(
                    item_id=item_id,
                    order_id=order.id,
                    quantity=quantity,
                    price=item.price  # возможно, стоит получать из таблицы delivery_item
                )
                session.add(item_order)
                session.commit()
                session.refresh(item_order)

            total = sum(item.quantity * item.price for item in order.items)
            order.total = total
            session.add(order)
            session.commit()
            session.refresh(order)

    def remove_from_cart(self, item_id: int, user_id: int, quantity: int = 1):
        with Session(self.engine) as session:
            statement = select(OrderORMModel).where(
                OrderORMModel.user_id == user_id,
                OrderORMModel.status == "pending"
            )
            order = session.exec(statement).first()

            if not order:
                return

            statement = select(ItemOrder).where(
                ItemOrder.order_id == order.id,
                ItemOrder.item_id == item_id
            )
            item_order = session.exec(statement).first()

            if item_order:
                if item_order.quantity > quantity:
                    item_order.quantity -= quantity
                else:
                    session.delete(item_order)

            total = sum(item.quantity * item.price for item in order.items)
            order.total = total
            session.add(order)
            session.commit()
            session.refresh(order)

    def checkout(self, user_id: int):
        with Session(self.engine) as session:
            statement = select(OrderORMModel).where(
                OrderORMModel.user_id == user_id,
                OrderORMModel.status == "pending"
            )
            order = session.exec(statement).first()

            if not order:
                raise ValueError("No active order to checkout.")

            total = sum(item.quantity * item.price for item in order.items)
            order.total = total
            order.status = "confirmed"
            order.created_at = datetime.now()

            session.add(order)
            session.commit()
            session.refresh(order)
            return order

