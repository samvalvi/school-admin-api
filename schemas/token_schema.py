from pydantic import BaseModel
from typing import Optional


class TokenBase(BaseModel):
    """Base token model."""
    access_token: str
    token_type: str


class TokenCreate(TokenBase):
    """Token create model."""
    pass


class TokenData(TokenBase):
    """Token data model."""
    username: Optional[str] = None
