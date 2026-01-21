import re
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,32}$")

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("username")
    def validate_username(cls, v: str):
        v = v.strip().lower()
        if not USERNAME_REGEX.fullmatch(v):
            raise ValueError("Username must be 3–32 chars: letters, numbers, underscore")
        return v

    @field_validator("password")
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password too short")
        return v

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)