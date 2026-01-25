from pydantic import BaseModel
from typing import Optional

class PlayerBase(BaseModel):
    nick: str
    logo_url: Optional[str] = None
    active: bool = True

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    pass

class PlayerResponse(PlayerBase):
    id: int

    class Config:
        from_attributes = True

