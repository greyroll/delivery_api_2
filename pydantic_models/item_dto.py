from pydantic import BaseModel


class ItemDTO(BaseModel):
	id: int | None
	title: str
	price: int
	description: str
	picture: str
	category_id: int

	class Config:
		from_attributes = True