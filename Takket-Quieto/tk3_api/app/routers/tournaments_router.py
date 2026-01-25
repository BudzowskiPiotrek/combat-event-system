from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.db import get_db
from ..schemas.tournament_schemas import TournamentResponse, TournamentCreate, ParticipantCreate
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
    Obtener todos los torneos.
    """
    return service.get_all(db)

@router.get("/{tournament_id}", response_model=TournamentResponse)
def read_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """
    Obtener un torneo por su ID.
    """
    tournament = service.get_by_id(db, tournament_id)
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament

@router.post("/", response_model=TournamentResponse)
def create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo torneo (estado inicial DRAFT).
    """
    try:
        return service.create_tournament(db, tournament)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{tournament_id}/participants", response_model=PlayerResponse)
def add_participant(tournament_id: int, participant: ParticipantCreate, db: Session = Depends(get_db)):
    """
    Añadir un participante al torneo.
    """
    try:
        return service.add_participant(db, tournament_id, participant)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tournament_id}/participants", response_model=List[PlayerResponse])
def read_participants(tournament_id: int, db: Session = Depends(get_db)):
    """
    Listar participantes de un torneo.
    """
    return service.get_participants(db, tournament_id)
