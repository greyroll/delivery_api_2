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


