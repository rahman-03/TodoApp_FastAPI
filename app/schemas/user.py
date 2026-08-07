from pydantic import BaseModel, EmailStr, Field, ConfigDict

class DetailsChange(BaseModel):
    password : str
    email : EmailStr | None = None
    firstname : str | None = None
    lastname : str | None = None
    phone_no : str | None = Field(default=None,pattern=r"^\d{10}$")

class UserRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=30)
    firstname: str = Field(min_length=2)
    lastname: str = Field(min_length=1)
    password: str = Field(min_length=8)
    phone_no: str = Field(pattern=r"^\d{10}$")

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : int
    email : EmailStr
    username : str
    firstname : str
    lastname : str
    role : str
    is_active : bool
    phone_no : str | None

class PassChange(BaseModel):
    old_pass : str = Field(min_length=8)
    new_pass : str = Field(min_length=8)
    conf_pass : str = Field(min_length=8)

class AdminUserProfileUpdate(BaseModel):
    username : str | None = None
    is_active : bool | None = None
    role : str | None = None
