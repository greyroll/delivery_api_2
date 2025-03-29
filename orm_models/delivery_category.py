from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class DeliveryCategoryORMModel(SQLModel, table=True):
	__tablename__ = "delivery_categories"

	id: Optional[int] = Field(default=None, primary_key=True)
	title: str
	delivery_items: list["DeliveryItemORMModel"] = Relationship(back_populates="category")


	def __repr__(self):
		return f"DeliveryCategoryORMModel(id={self.id}, title={self.title})"
