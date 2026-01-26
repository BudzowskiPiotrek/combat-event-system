from pydantic import BaseModel
from typing import Optional
from enum import Enum

class MatchStatus(str, Enum):
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"

class MatchResponse(BaseModel):
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
    winner_id: int
