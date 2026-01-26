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
    Recupera el listado completo de jugadores.

    :param db: Sesión de base de datos inyectada.
    :return: Lista de jugadores (esquema PlayerResponse).
    """
    return service.get_all(db)

@router.get("/{player_id}", response_model=PlayerResponse)
def read_player(player_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de un jugador específico por ID.

    :param player_id: Identificador del jugador.
    :param db: Sesión de base de datos inyectada.
    :return: Datos del jugador o error 404 si no existe.
    """
    player = service.get_by_id(db, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.post("/", response_model=PlayerResponse)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo jugador en el sistema.

    :param player: Datos para la creación del jugador.
    :param db: Sesión de base de datos inyectada.
    :return: El jugador creado o error 400 si la operación falla.
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
    Actualiza la información de un jugador existente.

    :param player_id: ID del jugador a actualizar.
    :param player: Esquema con los nuevos datos.
    :param db: Sesión de base de datos inyectada.
    :return: Jugador actualizado o error 404.
    """
    updated_player = service.update_player(db, player_id, player)
    if updated_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return updated_player

@router.patch("/{player_id}/toggle", response_model=PlayerResponse)
def toggle_player_status(player_id: int, db: Session = Depends(get_db)):
    """
    Activa o desactiva a un jugador mediante su identificador.

    :param player_id: ID del jugador a modificar.
    :param db: Sesión de base de datos inyectada.
    :return: Jugador con estado toggleado o error 404.
    """
    updated_player = service.toggle_active(db, player_id)

    if updated_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return updated_player

