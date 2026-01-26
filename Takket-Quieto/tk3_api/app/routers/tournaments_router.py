from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.db import get_db
from ..schemas.tournament_schemas import TournamentResponse, TournamentCreate, ParticipantCreate, TournamentUpdate
from ..schemas.match_schemas import MatchResponse
from ..schemas.player_schemas import PlayerResponse
from ..services.tournaments_service import TournamentsService

router = APIRouter(
    prefix="/tournaments",
    tags=["tournaments"]
)

service = TournamentsService()

@router.get("/", response_model=List[TournamentResponse])
def read_tournaments(db: Session = Depends(get_db)):
    """
    Obtiene el listado de todos los torneos registrados.

    :param db: Sesión de base de datos inyectada.
    :return: Lista de torneos disponibles.
    """
    return service.get_all(db)

@router.get("/{tournament_id}", response_model=TournamentResponse)
def read_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """
    Recupera la información detallada de un torneo por su identificador.

    :param tournament_id: ID del torneo.
    :param db: Sesión de base de datos inyectada.
    :return: Datos del torneo o error 404 si no se encuentra.
    """
    tournament = service.get_by_id(db, tournament_id)
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament

@router.post("/", response_model=TournamentResponse)
def create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo torneo en el sistema con estado inicial DRAFT.

    :param tournament: Esquema con los datos del nuevo torneo.
    :param db: Sesión de base de datos inyectada.
    :return: El torneo creado o error 400.
    """
    try:
        return service.create_tournament(db, tournament)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{tournament_id}", response_model=TournamentResponse)
def update_tournament(tournament_id: int, tournament: TournamentUpdate, db: Session = Depends(get_db)):
    """
    Actualiza la información básica de un torneo.

    :param tournament_id: ID del torneo a actualizar.
    :param tournament: Esquema con los nuevos datos.
    :param db: Sesión de base de datos inyectada.
    :return: Torneo actualizado o error 404.
    """
    updated_tournament = service.update_tournament(db, tournament_id, tournament)
    if updated_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return updated_tournament

@router.post("/{tournament_id}/participants", response_model=PlayerResponse)
def add_participant(tournament_id: int, participant: ParticipantCreate, db: Session = Depends(get_db)):
    """
    Inscribe a un jugador existente en un torneo determinado.

    :param tournament_id: ID del torneo de destino.
    :param participant: Identificador del jugador a inscribir.
    :param db: Sesión de base de datos inyectada.
    :return: Los datos del jugador inscrito o error 400 por validación.
    """
    try:
        return service.add_participant(db, tournament_id, participant)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tournament_id}/participants", response_model=List[PlayerResponse])
def read_participants(tournament_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el listado de todos los jugadores inscritos en un torneo específico.

    :param tournament_id: ID del torneo.
    :param db: Sesión de base de datos inyectada.
    :return: Lista de participantes.
    """
    return service.get_participants(db, tournament_id)

@router.post("/{tournament_id}/generate", response_model=List[MatchResponse])
def generate_bracket(tournament_id: int, db: Session = Depends(get_db)):
    """
    Genera automáticamente el cuadro de combates (bracket) para el torneo.
    Establece los emparejamientos de la ronda 1 y gestiona BYEs.

    :param tournament_id: ID del torneo.
    :param db: Sesión de base de datos inyectada.
    :return: Lista de combates generados.
    """
    try:
        return service.generate_bracket(db, tournament_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{tournament_id}/next-round", response_model=List[MatchResponse])
def generate_next_round(tournament_id: int, db: Session = Depends(get_db)):
    """
    Crea los emparejamientos para la siguiente ronda basándose en los ganadores actuales.

    :param tournament_id: ID del torneo.
    :param db: Sesión de base de datos inyectada.
    :return: Lista de nuevos combates generados.
    """
    try:
        return service.generate_next_round(db, tournament_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tournament_id}/bracket", response_model=List[MatchResponse])
def read_bracket(tournament_id: int, db: Session = Depends(get_db)):
    """
    Recupera el cuadro completo del torneo (todos los combates de todas las rondas).

    :param tournament_id: ID del torneo.
    :param db: Sesión de base de datos inyectada.
    :return: Listado de combates del torneo.
    """
    return service.get_bracket(db, tournament_id)
