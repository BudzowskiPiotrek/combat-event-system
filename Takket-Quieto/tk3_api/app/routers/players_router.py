from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.db import get_db
from ..schemas.player_schemas import PlayerResponse, PlayerCreate, PlayerUpdate
from ..services.players_service import PlayersService

router = APIRouter(
    prefix="/players",
    tags=["players"]
)

service = PlayersService()

@router.get("/", response_model=List[PlayerResponse])
def read_players(db: Session = Depends(get_db)):
    """
    Obtener todos los jugadores.
    """
    return service.get_all(db)

@router.get("/{player_id}", response_model=PlayerResponse)
def read_player(player_id: int, db: Session = Depends(get_db)):
    """
    Obtener un jugador por su ID.
    """
    player = service.get_by_id(db, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.post("/", response_model=PlayerResponse)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo jugador.
    """
    # En un escenario real validariamos si el nick ya existe aqui o capturariamos la excepcion de integridad
    try:
        return service.create_player(db, player)
    except Exception as e:
        # Simplificacion para el ejercicio
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{player_id}", response_model=PlayerResponse)
def update_player(player_id: int, player: PlayerUpdate, db: Session = Depends(get_db)):
    """
    Actualizar datos de un jugador.
    """
    updated_player = service.update_player(db, player_id, player)
    if updated_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return updated_player

@router.patch("/{player_id}/toggle", response_model=PlayerResponse)
def toggle_player_status(player_id: int, db: Session = Depends(get_db)):
    """
    Cambiar el estado activo/inactivo de un jugador.
    """
    updated_player = service.toggle_active(db, player_id)

    if updated_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return updated_player

