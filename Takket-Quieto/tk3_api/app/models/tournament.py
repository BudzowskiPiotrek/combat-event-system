from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime
import enum
from ..core.db import Base

class TournamentStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    GENERATED = "GENERATED"
    FINISHED = "FINISHED"

class Tournament(Base):
    """
    Modelo de Torneo.
    Gestiona los torneos y su estado dentro del sistema.
    """
    __tablename__ = "tournament"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(Enum(TournamentStatus), default=TournamentStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    winner_id = Column(Integer, nullable=True)
