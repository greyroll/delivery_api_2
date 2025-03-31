from sqlmodel import Session, select

from orm_models import UserORMModel
from orm_managers import BaseORMManager


class UserORMManager(BaseORMManager):
	model = UserORMModel

	def get_by_id(self, user_id: int) -> UserORMModel:
		with Session(self.engine) as session:
			return session.exec(select(self.model).where(self.model.id == user_id)).first()

	def get_by_email(self, email: str) -> UserORMModel:
		with Session(self.engine) as session:
			return session.exec(select(self.model).where(self.model.email == email)).first()

	def get_user_id_by_email(self, email: str) -> int | None:
		user = self.get_by_email(email)
		if user:
			return user.id

	def set_user_info(self, user_id: int, user_name, user_address, user_phone):
		with Session(self.engine) as session:
			user = session.get(self.model, user_id)
			user.name = user_name
			user.address = user_address
			user.phone = user_phone
			session.add(user)
			session.commit()
			session.refresh(user)

