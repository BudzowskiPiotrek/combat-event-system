from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.tournament import Tournament, TournamentStatus
from ..schemas.tournament_schemas import TournamentCreate

class TournamentsService:
    """
    Servicio para gestionar la lógica de negocio de torneos.
    """

    def get_all(self, db: Session) -> List[Tournament]:
        """Obtiene todos los torneos de la base de datos."""
        return db.query(Tournament).all()

    def get_by_id(self, db: Session, tournament_id: int) -> Optional[Tournament]:
        """Busca un torneo por su ID."""
        return db.query(Tournament).filter(Tournament.id == tournament_id).first()

    def create_tournament(self, db: Session, tournament: TournamentCreate) -> Tournament:
        """Crea un nuevo torneo en la base de datos con estado DRAFT."""
        db_tournament = Tournament(
            name=tournament.name,
            status=TournamentStatus.DRAFT
        )
        db.add(db_tournament)
        db.commit()
        db.refresh(db_tournament)
        return db_tournament
