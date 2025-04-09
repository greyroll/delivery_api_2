from pydantic import BaseModel, computed_field

from pydantic_models import ItemDTO


class ItemOrderDTO(BaseModel):
	id: int | None
	item_id: int
	order_id: int
	quantity: int
	price: float

	item: ItemDTO

	@computed_field
	@property
	def sum_price(self) -> float:
		return self.quantity * self.price

	class Config:
		from_attributes = True