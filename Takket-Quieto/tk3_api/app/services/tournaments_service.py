from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.tournament import Tournament, TournamentStatus
from ..models.tournament_player import TournamentPlayer
from ..models.player import Player
from ..models.match import Match, MatchStatus
from ..schemas.tournament_schemas import TournamentCreate, ParticipantCreate, TournamentUpdate
import math
import random

class TournamentsService:
    """
    Servicio encargado de la lógica de negocio de los torneos.
    
    Gestiona el ciclo de vida completo de las competiciones: desde la creación
    en modo borrador, inscripción de participantes, generación del cuadro KO
    (bracket), hasta la progresión de rondas y finalización del torneo.
    """

    def get_all(self, db: Session) -> List[Tournament]:
        """
        Obtiene la lista de todos los torneos registrados.

        :param db: Sesión de la base de datos.
        :return: Lista de objetos Tournament.
        """
        return db.query(Tournament).all()

    def get_by_id(self, db: Session, tournament_id: int) -> Optional[Tournament]:
        """
        Recupera un torneo específico por su identificador único.

        :param db: Sesión de la base de datos.
        :param tournament_id: Identificador del torneo.
        :return: Objeto Tournament o None si no se encuentra.
        """
        return db.query(Tournament).filter(Tournament.id == tournament_id).first()

    def create_tournament(self, db: Session, tournament: TournamentCreate) -> Tournament:
        """
        Crea un nuevo torneo con el estado inicial DRAFT.

        :param db: Sesión de la base de datos.
        :param tournament: Datos del torneo a crear.
        :return: El torneo creado y persistido.
        """
        db_tournament = Tournament(
            name=tournament.name,
            status=TournamentStatus.DRAFT
        )
        db.add(db_tournament)
        db.commit()
        db.refresh(db_tournament)
        return db_tournament

    def update_tournament(self, db: Session, tournament_id: int, tournament_update: TournamentUpdate) -> Optional[Tournament]:
        """
        Actualiza los datos básicos de un torneo.

        :param db: Sesión de la base de datos.
        :param tournament_id: ID del torneo a actualizar.
        :param tournament_update: Datos a actualizar.
        :return: El torneo actualizado o None si no se encontró.
        """
        db_tournament = self.get_by_id(db, tournament_id)
        if not db_tournament:
            return None
        
        if tournament_update.name is not None:
            db_tournament.name = tournament_update.name
            
        db.commit()
        db.refresh(db_tournament)
        return db_tournament

    def add_participant(self, db: Session, tournament_id: int, participant: ParticipantCreate) -> Optional[Player]:
        """
        Inscribe a un jugador en un torneo específico.
        
        Realiza validaciones críticas: existencia del torneo, existencia del jugador,
        si el jugador está activo y si ya estaba inscrito previamente.
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
        """
        Obtiene la lista de los jugadores inscritos en un torneo particular.

        :param db: Sesión de la base de datos.
        :param tournament_id: Identificador del torneo.
        :return: Lista de objetos Player que participan.
        """
        return db.query(Player).join(TournamentPlayer).filter(TournamentPlayer.tournament_id == tournament_id).all()

    def generate_bracket(self, db: Session, tournament_id: int) -> List[Match]:
        """
        Genera la estructura inicial (ronda 1) de un torneo KO.
        
        El proceso incluye:
        1. Recuperar y barajar participantes de forma aleatoria.
        2. Determinar la potencia de 2 superior para dimensionar el cuadro.
        3. Crear los combates de la ronda 1.
        4. Gestionar automáticamente los BYEs (jugadores sin oponente pasan a ronda 2).
        5. Cambiar el estado del torneo a GENERATED.

        :param db: Sesión de la base de datos.
        :param tournament_id: ID del torneo a generar.
        :return: Lista de combates de la primera ronda.
        """
        tournament = self.get_by_id(db, tournament_id)
        if not tournament:
            raise Exception("Tournament not found")
        
        if tournament.status != TournamentStatus.DRAFT:
            raise Exception("Bracket can only be generated for tournaments in DRAFT status")

        participants = self.get_participants(db, tournament_id)
        if len(participants) < 2:
            raise Exception("At least 2 participants are required to generate a bracket")

        random.shuffle(participants)

        # Determinar tamaño de bracket (potencia de 2)
        n = len(participants)
        bracket_size = 2**math.ceil(math.log2(n))
        
        # Crear matches de ronda 1
        matches = []
        num_matches = bracket_size // 2
        
        for i in range(num_matches):
            p1 = participants[i*2] if i*2 < n else None
            p2 = participants[i*2+1] if i*2+1 < n else None
            
            # Si p2 no existe, es un BYE para p1
            # Si p1 no existe (no debería pasar por lógica de potencia), es vacío
            
            status = MatchStatus.PENDING
            winner_id = None
            
            if p1 and not p2: # BYE
                status = MatchStatus.RESOLVED
                winner_id = p1.id
            
            db_match = Match(
                tournament_id=tournament_id,
                round=1,
                position=i + 1,
                player1_id=p1.id if p1 else None,
                player2_id=p2.id if p2 else None,
                winner_id=winner_id,
                status=status
            )
            db.add(db_match)
            matches.append(db_match)

        tournament.status = TournamentStatus.GENERATED
        db.commit()
        return matches

    def generate_next_round(self, db: Session, tournament_id: int) -> List[Match]:
        """
        Avanza el torneo creando los emparejamientos de la siguiente ronda.
        
        Valida que todos los combates de la ronda actual hayan sido resueltos.
        Empareja a los ganadores según su posición en el cuadro. Si solo queda
        un ganador, finaliza el torneo determinando al campeón.

        :param db: Sesión de la base de datos.
        :param tournament_id: ID del torneo.
        :return: Lista de combates de la nueva ronda generada.
        """
        tournament = self.get_by_id(db, tournament_id)
        if not tournament:
            raise Exception("Tournament not found")

        # Buscar última ronda
        last_match = db.query(Match).filter(Match.tournament_id == tournament_id).order_by(Match.round.desc()).first()
        if not last_match:
            raise Exception("No bracket found for this tournament")
        
        current_round = last_match.round
        
        # Verificar que todos los matches de la ronda actual estén resueltos
        pending = db.query(Match).filter(
            Match.tournament_id == tournament_id,
            Match.round == current_round,
            Match.status == MatchStatus.PENDING
        ).count()
        
        if pending > 0:
            raise Exception(f"Cannot progress: there are {pending} pending matches in round {current_round}")

        # Obtener ganadores de la ronda actual ordenados por posición
        winners = db.query(Match).filter(
            Match.tournament_id == tournament_id,
            Match.round == current_round
        ).order_by(Match.position).all()

        if len(winners) == 1:
            # Ya tenemos un campeón
            tournament.status = TournamentStatus.FINISHED
            tournament.winner_id = winners[0].winner_id
            db.commit()
            return []

        # Crear nueva ronda
        new_matches = []
        next_round = current_round + 1
        num_new_matches = len(winners) // 2

        for i in range(num_new_matches):
            w1 = winners[i*2]
            w2 = winners[i*2+1]
            
            db_match = Match(
                tournament_id=tournament_id,
                round=next_round,
                position=i + 1,
                player1_id=w1.winner_id,
                player2_id=w2.winner_id,
                status=MatchStatus.PENDING
            )
            db.add(db_match)
            new_matches.append(db_match)

        db.commit()
        return new_matches

    def get_bracket(self, db: Session, tournament_id: int) -> List[Match]:
        """
        Recupera todos los combates asociados a un torneo, ordenados para su visualización.

        :param db: Sesión de la base de datos.
        :param tournament_id: ID del torneo.
        :return: Lista de objetos Match.
        """
        return db.query(Match).filter(Match.tournament_id == tournament_id).order_by(Match.round, Match.position).all()
