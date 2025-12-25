from pydantic import UserBase

class UserModel(UserBase):
    user_input:str
