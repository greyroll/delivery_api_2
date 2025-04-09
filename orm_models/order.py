from datetime import datetime

from sqlmodel import Field, SQLModel, Relationship

from orm_models.item_order import ItemOrder
from orm_models.user import UserORMModel


class OrderORMModel(SQLModel, table=True):
	__tablename__ = "orders"

	id: int | None = Field(default=None, primary_key=True)
	user_id: int = Field(foreign_key="users.id")
	created_at: datetime = Field(default_factory=datetime.now)
	status: str = "pending"
	address: str | None
	total: float

	user: UserORMModel = Relationship(back_populates="orders", sa_relationship_kwargs={"lazy": "selectin"})
	items: list[ItemOrder] = Relationship(back_populates="order", sa_relationship_kwargs={"lazy": "selectin"})

	@property
	def cart_count(self):
		return len(self.items)