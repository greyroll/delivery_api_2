from fastapi import Form
from pydantic import BaseModel

class UserLoginDTO(BaseModel):
    email: str
    password: str

    @classmethod
    def as_form(cls, email: str = Form(...), password: str = Form(...)):
        return cls(email=email, password=password)
