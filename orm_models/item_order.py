from sqlmodel import SQLModel, Field, Relationship


class ItemOrder(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="delivery_items.id")
    order_id: int = Field(foreign_key="orders.id")
    quantity: int
    price: float

    order: "OrderORMModel" = Relationship(back_populates="items")