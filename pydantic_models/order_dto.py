from datetime import datetime

from pydantic import BaseModel, Field

from pydantic_models.item_order_dto import ItemOrderDTO
from pydantic_models.user_dto import UserDTO


class OrderDTO(BaseModel):
    id: int | None
    user_id: int
    created_at: datetime = Field(default_factory=datetime.now)
    status: str
    address: str | None
    total: float

    user: UserDTO
    items: list[ItemOrderDTO]

    @property
    def cart_count(self):
        return len(self.items)

    class Config:
        from_attributes = True