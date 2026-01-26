from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..schemas.match_schemas import MatchResponse, MatchWinnerUpdate
from ..services.matches_service import MatchesService

router = APIRouter(
    prefix="/matches",
    tags=["matches"]
)

service = MatchesService()

@router.post("/{match_id}/winner", response_model=MatchResponse)
def set_winner(match_id: int, winner: MatchWinnerUpdate, db: Session = Depends(get_db)):
    """
    Registra oficialmente el ganador de un combate particular.
    Actualiza el estado del combate a RESOLVED.

    :param match_id: Identificador único del combate.
    :param winner: Esquema conteniendo el ID del jugador ganador.
    :param db: Sesión de base de datos inyectada.
    :return: Los datos del combate actualizado o error 400.
    """
    try:
        return service.set_winner(db, match_id, winner.winner_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
