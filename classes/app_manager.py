import random

from classes.custom_exceptions import UserAlreadyExistsException, UserNotFoundException, PasswordIsTooShortException, \
	InvalidPasswordException
from classes.jwt_manager import JWTManager
from classes.password_manager import PasswordManager
from orm_managers import UserORMManager, OrderORMManager, DeliveryItemORMManager
from orm_models import DeliveryItemORMModel, UserORMModel
from pydantic_models.order_dto import OrderDTO


class AppManager:
	def __init__(self):
		self.user_manager = UserORMManager()
		self.order_manager = OrderORMManager()
		self.items_manager = DeliveryItemORMManager()
		self.password_manager = PasswordManager()
		self.jwt_manager = JWTManager()

	def create_menu_for_index(self) -> dict[str, list[DeliveryItemORMModel | None]]:
		menu = {}
		for category in self.items_manager.get_all_categories():
			menu[category.title] = random.sample(self.items_manager.get_by_category(category.title), 3)
		return menu

	def validate_login(self, email: str, password: str) -> bool:
		user: UserORMModel = self.user_manager.get_by_email(email)
		if user is None:
			raise UserNotFoundException()
		if self.password_manager.verify_password(password, user.password) is False:
			raise InvalidPasswordException()
		return True

	def register_user(self, email: str, password: str) -> bool:
		if self.user_manager.get_by_email(email):
			raise UserAlreadyExistsException()
		if len(password) < 3:
			raise PasswordIsTooShortException(min_length=3)
		user = UserORMModel(email=email, password=self.password_manager.hash_password(password))
		self.user_manager.add(user)
		return True

	def get_auth_context(self, token: str | None) -> dict:
		"""
		Возвращает контекст авторизации для шаблона.
		"""
		payload = self.jwt_manager.get_payload_or_none(token)
		return {
			"is_logged_in": payload is not None,
			"user_id": int(payload.get("sub")) if payload else None
		}

	def get_order_by_auth_context(self, context: dict) -> OrderDTO | None:
		user_id = context.get("user_id")
		if user_id is None:
			raise UserNotFoundException()
		order: OrderDTO = self.order_manager.get_active_order_by_user_id(user_id)
		if order is None:
			order = self.order_manager.create_order(user_id)
		return order

	def get_order_history(self, user_id: int, limit: int = 3) -> list[OrderDTO]:
		orders_history = self.order_manager.get_order_history(user_id)
		return orders_history[:limit]

