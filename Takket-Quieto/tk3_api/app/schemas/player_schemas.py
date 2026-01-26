from pydantic import BaseModel
from typing import Optional

class PlayerBase(BaseModel):
    """
    Esquema base para la entidad Jugador.
    Define los campos compartidos para creación, actualización y respuesta.
    """
    nick: str
    logo_url: Optional[str] = None
    active: bool = True

class PlayerCreate(PlayerBase):
    """Esquema para la creación de un nuevo jugador."""
    pass

class PlayerUpdate(PlayerBase):
    pass

class PlayerResponse(PlayerBase):
    """Esquema de respuesta que incluye el identificador único del jugador."""
    id: int

    class Config:
        from_attributes = True

