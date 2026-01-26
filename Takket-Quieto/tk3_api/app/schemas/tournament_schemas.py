from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class TournamentStatus(str, Enum):
    DRAFT = "DRAFT"
    GENERATED = "GENERATED"
    FINISHED = "FINISHED"

class TournamentBase(BaseModel):
    name: str

class TournamentCreate(TournamentBase):
    pass

class TournamentResponse(TournamentBase):
    id: int
    status: TournamentStatus
    created_at: datetime
    winner_id: Optional[int] = None

    class Config:
        from_attributes = True

class ParticipantCreate(BaseModel):
    player_id: int
