from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.tournament import Tournament, TournamentStatus
from ..models.tournament_player import TournamentPlayer
from ..models.player import Player
from ..schemas.tournament_schemas import TournamentCreate, ParticipantCreate

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

    def add_participant(self, db: Session, tournament_id: int, participant: ParticipantCreate) -> Optional[Player]:
        """
        Añade un jugador al torneo.
        Valida que el torneo exista, el jugador exista, esté activo y no esté ya inscrito.
        """
        # Validar torneo
        tournament = self.get_by_id(db, tournament_id)
        if not tournament:
            raise Exception("Tournament not found")

        # Validar jugador
        player = db.query(Player).filter(Player.id == participant.player_id).first()
        if not player:
            raise Exception("Player not found")
        
        if not player.active:
            raise Exception("Only active players can participate in tournaments")

        # Validar duplicados
        exists = db.query(TournamentPlayer).filter(
            TournamentPlayer.tournament_id == tournament_id,
            TournamentPlayer.player_id == participant.player_id
        ).first()
        
        if exists:
            raise Exception("Player already registered in this tournament")

        # Registrar participación
        db_participant = TournamentPlayer(
            tournament_id=tournament_id,
            player_id=participant.player_id
        )
        db.add(db_participant)
        db.commit()
        
        return player

    def get_participants(self, db: Session, tournament_id: int) -> List[Player]:
        """Obtiene la lista de jugadores inscritos en un torneo."""
        return db.query(Player).join(TournamentPlayer).filter(TournamentPlayer.tournament_id == tournament_id).all()
