import pydantic 
from typing import Optional, Type



class AbstractAdv(pydantic.BaseModel):
    title: str
    description: str

    @pydantic.field_validator("title")
    @classmethod
    def title_len(cls, v:str) -> str:
        if len(v) >100:
            raise ValueError("")
        return v
    
    @pydantic.field_validator("description")
    @classmethod
    def desc_len(cls, v:str) -> str:
        if len(v) > 1000:
            raise ValueError("")
        return v
    
class CreateAdv(AbstractAdv):
    title: str
    description: str
    owner_id: int


class UpdateAdv(AbstractAdv):
    title: Optional[str] = None
    description:  Optional[str] = None
    owner_id: Optional[str] = None

class CreateUser(pydantic.BaseModel):
    name: str
    email: str
    password: str

    @classmethod
    def secure_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError(f"Minimal length of password is 8")
        return v
    
SCHEMA_CLASS = Type[CreateAdv | UpdateAdv]
SCHEMA_CLASS = CreateAdv | UpdateAdv