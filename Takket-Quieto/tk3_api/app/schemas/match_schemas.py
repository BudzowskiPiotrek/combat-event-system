from pydantic import BaseModel
from typing import Optional
from enum import Enum


class MatchStatus(str, Enum):
    """Estados del combate para validación en esquemas."""

    PENDING = "PENDING"
    RESOLVED = "RESOLVED"


class MatchResponse(BaseModel):
    """Esquema de respuesta detallado para un combate."""

    id: int
    tournament_id: int
    round: int
    position: int
    player1_id: Optional[int] = None
    player2_id: Optional[int] = None
    winner_id: Optional[int] = None
    status: MatchStatus

    class Config:
        from_attributes = True


class MatchWinnerUpdate(BaseModel):
    """Esquema para la actualización del ganador de un combate."""

    winner_id: int
