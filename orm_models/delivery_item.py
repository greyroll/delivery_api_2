from sqlmodel import SQLModel, Field, Relationship

from orm_models import DeliveryCategoryORMModel


class DeliveryItemORMModel(SQLModel, table=True):
	__tablename__ = "delivery_items"

	id: int | None = Field(default=None, primary_key=True)
	title: str
	price: int
	description: str
	picture: str
	category_id: int = Field(foreign_key='delivery_categories.id')
	category: DeliveryCategoryORMModel | None = Relationship(back_populates="delivery_items")
	orders: list["ItemOrder"] = Relationship(back_populates="item")


	def __str__(self):
		return f"DeliveryItemORMModel(id={self.id}, title={self.title}, price={self.price}, description={self.description}, picture={self.picture}, category_id={self.category_id})"