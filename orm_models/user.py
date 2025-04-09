
from sqlmodel import SQLModel, Field, Relationship


class UserORMModel(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    name: str | None
    email: str
    phone_number: str | None
    password: str
    last_address: str | None

    orders: list['OrderORMModel'] = Relationship(back_populates="user")