from sqlmodel import Session, select

from orm_models import DeliveryItemORMModel, DeliveryCategoryORMModel
from .base_manager import BaseORMManager


class DeliveryItemORMManager(BaseORMManager):
	model = DeliveryItemORMModel

	def get_all_items(self) -> list[DeliveryItemORMModel]:
		"""
		Fetches all items from the database joined with their categories.
		"""
		with Session(self.engine) as session:
			return list(session.exec(select(self.model).join(DeliveryCategoryORMModel)).all())

	def get_by_id(self, item_id: int) -> DeliveryItemORMModel | None:
		"""
		Fetches a delivery item joined with its category by item id.
		"""
		with Session(self.engine) as session:
			return session.exec(select(self.model).join(DeliveryCategoryORMModel).where(self.model.id == item_id)).first()

	def get_by_category(self, category_name: str) -> list[DeliveryItemORMModel] | None:
		"""
		Fetches all delivery items joined with their categories by category name.
		"""
		with Session(self.engine) as session:
			return list(session.exec(select(self.model).join(DeliveryCategoryORMModel).where(DeliveryCategoryORMModel.title == category_name)).fetchall())

	def get_all_categories(self) -> list[DeliveryCategoryORMModel]:
		"""Fetches all delivery categories from the database."""
		with Session(self.engine) as session:
			return list(session.exec(select(DeliveryCategoryORMModel)).all())

