import random

from classes.custom_exceptions import UserAlreadyExistsException, UserNotFoundException, PasswordIsTooShortException, \
	InvalidPasswordException
from classes.jwt_manager import JWTManager
from classes.password_manager import PasswordManager
from orm_managers import UserORMManager, CartOrderORMManager, DeliveryItemORMManager
from orm_models import DeliveryItemORMModel, UserORMModel


class AppManager:
	def __init__(self):
		self.user_manager = UserORMManager()
		self.cart_manager = CartOrderORMManager()
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

