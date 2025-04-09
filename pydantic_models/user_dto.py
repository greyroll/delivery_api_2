from pydantic import BaseModel


class UserDTO(BaseModel):

	id: int | None
	name: str | None
	email: str
	phone_number: str | None
	password: str
	last_address: str | None

	class Config:
		from_attributes = True