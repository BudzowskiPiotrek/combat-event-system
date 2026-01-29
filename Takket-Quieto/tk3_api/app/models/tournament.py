from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime
import enum
from ..core.db import Base


class TournamentStatus(str, enum.Enum):
    """
    Enumeración que define los posibles estados de un torneo.

    DRAFT: El torneo está en creación y se pueden añadir participantes.
    GENERATED: El cuadro ha sido generado y el torneo está en curso.
    FINISHED: El torneo ha finalizado y tiene un campeón.
    """

    DRAFT = "DRAFT"
    GENERATED = "GENERATED"
    FINISHED = "FINISHED"


class Tournament(Base):
    """
    Entidad que representa un torneo de eliminación directa.

    Gestiona el ciclo de vida de la competición, desde la fase de borrador
    hasta la determinación del campeón final.
    """

    __tablename__ = "tournament"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(
        Enum(TournamentStatus), default=TournamentStatus.DRAFT, nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    winner_id = Column(Integer, nullable=True)
