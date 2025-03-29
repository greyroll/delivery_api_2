from passlib.context import CryptContext


class PasswordManager:
	"""
	Менеджер для работы с хэшированием паролей.
	Использует passlib с алгоритмом bcrypt.
	"""

	def __init__(self):
		self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

	def hash_password(self, password: str) -> str:
		"""
		Хэширует пароль.

		:param password: Исходный пароль в виде строки.
		:return: Хэш пароля.
		"""
		return self.pwd_context.hash(password)

	def verify_password(self, plain_password: str, hashed_password: str) -> bool:
		"""
		Проверяет, соответствует ли открытый пароль его хэшу.

		:param plain_password: Пароль в открытом виде.
		:param hashed_password: Сохранённый хэш пароля.
		:return: True, если пароли совпадают, иначе False.
		"""
		return self.pwd_context.verify(plain_password, hashed_password)
