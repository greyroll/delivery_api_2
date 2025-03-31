from sqlmodel import SQLModel, Field, Relationship


class ItemOrder(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="delivery_items.id")
    order_id: int = Field(foreign_key="orders.id")
    quantity: int
    price: float

    item: "DeliveryItemORMModel" = Relationship(back_populates="orders", sa_relationship_kwargs={"lazy": "selectin"})
    order: "OrderORMModel" = Relationship(back_populates="items")

    @property
    def sum_price(self):
        return self.quantity * self.price