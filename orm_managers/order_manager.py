from sqlalchemy.orm import selectinload
from sqlmodel import Session, select, desc
from datetime import datetime

from classes.custom_exceptions import NoItemsInCartException, NoOrderHistoryException
from classes.order_status import OrderStatus
from orm_managers import BaseORMManager
from orm_models import DeliveryItemORMModel
from orm_models.item_order import ItemOrder
from orm_models.order import OrderORMModel
from pydantic_models.order_dto import OrderDTO


class OrderORMManager(BaseORMManager):
    model = OrderORMModel

    def not_nested_session_scope(self):
        session = Session(self.engine)
        session.commit()
        session.close()

    def has_active_order(self, user_id: int) -> bool:
            result = self.get_active_order_by_user_id(user_id)
            return result is not None

    def _get_active_order_by_user_id(self, session: Session, user_id: int) -> OrderORMModel | None:
        statement = select(OrderORMModel).where(
            OrderORMModel.user_id == user_id,
            OrderORMModel.status == OrderStatus.PENDING
        ).options(selectinload(OrderORMModel.items).options(selectinload(ItemOrder.item)))
        return session.exec(statement).first()

    def get_active_order_by_user_id(self, user_id: int) -> OrderDTO | None:
        with self.session_scope() as session:
            order = self._get_active_order_by_user_id(session, user_id)
            return OrderDTO.model_validate(order) if order else None

    def _create_order(self, session: Session, user_id: int) -> OrderORMModel:
        order = OrderORMModel(
            user_id=user_id,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            total=0.0,
        )
        session.add(order)
        session.commit()
        session.refresh(order)
        return order

    def create_order(self, user_id: int) -> OrderDTO:
        with self.session_scope() as session:
            order = self._create_order(session, user_id)
            return OrderDTO.model_validate(order)

    def _get_delivery_item_by_id(self, session: Session, item_id: int) -> DeliveryItemORMModel | None:
        statement = select(DeliveryItemORMModel).where(DeliveryItemORMModel.id == item_id)
        return session.exec(statement).first()

    def _get_item_order(self, session: Session, order_id: int, item_id: int) -> ItemOrder | None:
        statement = select(ItemOrder).where(
            ItemOrder.order_id == order_id,
            ItemOrder.item_id == item_id
        )
        return session.exec(statement).first()

    def _update_order_total(self, order: OrderORMModel) -> OrderORMModel:
        order.total = sum(item.sum_price for item in order.items)
        return order

    def add_to_cart(self, item_id: int, user_id: int, quantity: int = 1):
        with self.session_scope() as session:
            order = self._get_active_order_by_user_id(session, user_id)

            if order is None:
                order = self._create_order(session, user_id)

            item = self._get_delivery_item_by_id(session, item_id)
            item_order = self._get_item_order(session, order.id, item_id)

            if item_order:
                item_order.quantity += quantity
            else:
                item_order = ItemOrder(
                    item_id=item_id,
                    order_id=order.id,
                    quantity=quantity,
                    price=item.price
                )
                session.add(item_order)
                session.commit()
                session.refresh(item_order)

            session.refresh(order)
            order = self._update_order_total(order)
            session.add(order)
            session.commit()
            session.refresh(order)

    def remove_from_cart(self, item_id: int, user_id: int, quantity: int = 1):
        with self.session_scope() as session:
            order = self._get_active_order_by_user_id(session, user_id)

            if not order:
                return

            item_order = self._get_item_order(session, order.id, item_id)

            if item_order:
                if item_order.quantity > quantity:
                    item_order.quantity -= quantity
                else:
                    session.delete(item_order)

            session.refresh(order)
            order = self._update_order_total(order)
            session.add(order)
            session.commit()
            session.refresh(order)

    def checkout(self, user_id: int, name: str | None = None, address: str | None = None, phone: str | None = None) -> OrderORMModel:
        with self.session_scope() as session:

            order = self._get_active_order_by_user_id(session, user_id)

            if not order:
                raise ValueError("No active order to checkout.")

            if order.cart_count == 0:
                raise NoItemsInCartException("No items in cart. Please add items to checkout.")

            order.user.name = name
            order.user.phone_number = phone
            order.user.last_address = address



            session.add(order.user)
            session.flush()
            session.refresh(order.user)

            if order.address != address:
                order.address = address
            order.total = sum(item.sum_price for item in order.items)
            order.status = OrderStatus.CONFIRMED
            order.created_at = datetime.now()

            session.add(order)
            session.commit()
            session.refresh(order)
            return order

    def _get_confirmed_orders(self, session: Session, user_id: int) -> list[OrderORMModel]:
        statement = select(OrderORMModel).where(
                OrderORMModel.user_id == user_id,
                OrderORMModel.status == OrderStatus.CONFIRMED
            )
        return list(session.exec(statement).all())

    def get_order_history(self, user_id: int) -> list[OrderDTO]:
        with self.session_scope() as session:
            orders = self._get_confirmed_orders(session, user_id)
            orders.reverse()
            if not orders:
                raise NoOrderHistoryException()

            return [OrderDTO.model_validate(order) for order in orders]