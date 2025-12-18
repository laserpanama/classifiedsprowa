from pydantic import BaseModel, Field
from typing import Optional, Literal
import uuid

class AccountBase(BaseModel):
    email: str
    is_active: bool = True
    wanuncios_password: str # This will be stored in clear text for automation
    captcha_solving_method: Literal['api', 'manual', 'script'] = 'api'

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        from_attributes = True
