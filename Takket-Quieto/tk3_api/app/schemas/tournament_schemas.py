from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class TournamentStatus(str, Enum):
    """
    Estados posibles de un torneo para validación en esquemas.
    """
    DRAFT = "DRAFT"
    GENERATED = "GENERATED"
    FINISHED = "FINISHED"

class TournamentBase(BaseModel):
    """Esquema base que contiene los atributos principales de un Torneo."""
    name: str

class TournamentCreate(TournamentBase):
    """Esquema para la creación de torneos."""
    pass

class TournamentUpdate(TournamentBase):
    """Esquema para la actualización de torneos."""
    pass

class TournamentResponse(TournamentBase):
    """Esquema de respuesta completo para la entidad Torneo."""
    id: int
    status: TournamentStatus
    created_at: datetime
    winner_id: Optional[int] = None

    class Config:
        from_attributes = True

class ParticipantCreate(BaseModel):
    """Esquema para inscribir un jugador en un torneo."""
    player_id: int
