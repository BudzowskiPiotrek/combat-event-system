from sqlalchemy import Column, Integer, ForeignKey, Enum
import enum
from ..core.db import Base

class MatchStatus(str, enum.Enum):
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"

class Match(Base):
    """
    Modelo de Match (Combate).
    Representa un enfrentamiento entre dos jugadores dentro de un torneo.
    """
    __tablename__ = "match"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournament.id"), nullable=False)
    round = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    player1_id = Column(Integer, nullable=True) # Puede ser NULL si es un hueco pendiete o BYE
    player2_id = Column(Integer, nullable=True)
    winner_id = Column(Integer, nullable=True)
    status = Column(Enum(MatchStatus), default=MatchStatus.PENDING, nullable=False)
