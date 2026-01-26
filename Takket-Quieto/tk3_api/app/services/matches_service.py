from sqlalchemy.orm import Session
from typing import Optional
from ..models.match import Match, MatchStatus

class MatchesService:
    """
    Servicio encargado de la lógica de negocio de los combates (matches).
    
    Gestiona la recuperación de información de enfrentamientos individuales
    y el registro oficial de resultados y ganadores.
    """

    def get_by_id(self, db: Session, match_id: int) -> Optional[Match]:
        """
        Recupera los detalles de un combate específico.

        :param db: Sesión de la base de datos.
        :param match_id: Identificador único del combate.
        :return: Objeto Match o None si no existe.
        """
        return db.query(Match).filter(Match.id == match_id).first()

    def set_winner(self, db: Session, match_id: int, winner_id: int) -> Match:
        """
        Establece el ganador de un combate y actualiza su estado.
        
        Valida rigurosamente que:
        1. El combate exista.
        2. El combate no haya sido resuelto previamente.
        3. El ganador propuesto sea uno de los dos participantes del combate.

        :param db: Sesión de la base de datos.
        :param match_id: ID del combate.
        :param winner_id: ID del jugador que se declara ganador.
        :return: El combate actualizado con el ganador y estado RESOLVED.
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
