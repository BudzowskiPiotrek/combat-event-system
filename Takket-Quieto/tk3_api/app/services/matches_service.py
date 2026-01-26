from sqlalchemy.orm import Session
from typing import Optional
from ..models.match import Match, MatchStatus

class MatchesService:
    """
    Servicio para gestionar la lógica de los matches.
    """

    def get_by_id(self, db: Session, match_id: int) -> Optional[Match]:
        """Busca un match por su ID."""
        return db.query(Match).filter(Match.id == match_id).first()

    def set_winner(self, db: Session, match_id: int, winner_id: int) -> Match:
        """
        Registra el ganador de un combate.
        Valida que el match exista, esté pendiente y que el ganador sea uno de los jugadores.
        """
        match = self.get_by_id(db, match_id)
        if not match:
            raise Exception("Match not found")

        if match.status == MatchStatus.RESOLVED:
            raise Exception("Match is already resolved")

        if winner_id not in [match.player1_id, match.player2_id]:
            raise Exception("Winner must be one of the match players")

        match.winner_id = winner_id
        match.status = MatchStatus.RESOLVED
        
        db.commit()
        db.refresh(match)
        return match
