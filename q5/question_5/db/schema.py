from typing import List
from pydantic import BaseModel

class User(BaseModel):
    name: str
    password: str

class CreateUser(BaseModel):
    name: str
    password: str
    salt: str

    def __init__(self, name: str, password: str, salt: str):
        self.name = name
        self.password = password
        self.salt = salt

class AuthenticateUser(BaseModel):
    name: str
    password: str
    salt: str

    def __init__(self, name: str, password: str, salt: str):
        self.name = name
        self.password = password
        self.salt = salt