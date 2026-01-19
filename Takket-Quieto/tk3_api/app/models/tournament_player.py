from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from ..core.db import Base

class TournamentPlayer(Base):
    """
    Tabla intermedia para la relación Torneo - Jugadores.
    Define quién participa en cada torneo.
    """
    __tablename__ = "tournament_player"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournament.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)

    # Evitamos duplicados: un jugador no puede estar dos veces en el mismo torneo.
    __table_args__ = (UniqueConstraint('tournament_id', 'player_id', name='_tournament_player_uc'),)
