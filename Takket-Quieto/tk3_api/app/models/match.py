from sqlalchemy import Column, Integer, ForeignKey, Enum
import enum
from ..core.db import Base


class MatchStatus(str, enum.Enum):
    """
    Define el estado de resolución de un combate.

    PENDING: El combate aún no se ha disputado o el resultado no ha sido registrado.
    RESOLVED: El combate ha finalizado y se ha determinado un ganador.
    """

    PENDING = "PENDING"
    RESOLVED = "RESOLVED"


class Match(Base):
    """
    Entidad que representa un combate (enfrentamiento) en el sistema.

    Almacena la información de los participantes, la ronda del torneo,
    su posición en el cuadro y el resultado final.
    """

    __tablename__ = "match"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournament.id"), nullable=False)
    round = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    player1_id = Column(
        Integer, nullable=True
    )  # Puede ser NULL si es un hueco pendiete o BYE
    player2_id = Column(Integer, nullable=True)
    winner_id = Column(Integer, nullable=True)
    status = Column(Enum(MatchStatus), default=MatchStatus.PENDING, nullable=False)
