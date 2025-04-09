from pydantic import BaseModel, Field


class UserDTO(BaseModel):

	id: int | None
	name: str | None
	email: str
	phone_number: str | None
	password: str

	class Config:
		from_attributes = True