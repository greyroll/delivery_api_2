from sqlmodel import Session, select

from orm_models import UserORMModel
from orm_managers import BaseORMManager
from pydantic_models.user_dto import UserDTO


class UserORMManager(BaseORMManager):
	model = UserORMModel

	def _get_by_id(self, session: Session, user_id: int) -> UserORMModel | None:
		statement = select(self.model).where(self.model.id == user_id)
		return session.exec(statement).first()

	def get_by_id(self, user_id: int) -> UserDTO | None:
		with self.session_scope() as session:
			user = self._get_by_id(session, user_id)
			return UserDTO.model_validate(user) if user else None

	def _get_by_email(self, session: Session, email: str) -> UserORMModel | None:
		statement = select(self.model).where(self.model.email == email)
		return session.exec(statement).first()

	def get_by_email(self, email: str) -> UserDTO | None:
		with self.session_scope() as session:
			user = self._get_by_email(session, email)
			return UserDTO.model_validate(user) if user else None

	def get_user_id_by_email(self, email: str) -> int | None:
		with self.session_scope() as session:
			user = self._get_by_email(session, email)
			return user.id if user else None
