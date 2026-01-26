"""
Router de endpoints para la funcionalidad de informes.

Este módulo expone los endpoints HTTP que permiten consultar estadísticas
y reportes del sistema, como el ranking global de jugadores y el historial
de combates por torneo.

Propósito académico: Separación de responsabilidades entre controlador (router),
lógica de negocio (service) y acceso a datos (models).
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.db import get_db
from ..services.reports_service import ReportsService
from ..schemas.reports_schemas import LeaderboardEntry, MatchHistoryEntry


router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

# Instancia del servicio de informes
reports_service = ReportsService()


@router.get("/leaderboard", response_model=List[LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):
    """
    Obtiene el ranking global de jugadores.
    
    Devuelve una lista ordenada de jugadores con sus estadísticas de victorias
    y derrotas, calculadas a partir de todos los combates resueltos en el sistema.
    
    Criterios de cálculo:
    - Solo se cuentan combates con status = RESOLVED
    - Victorias: combates donde el jugador es el ganador
    - Derrotas: combates donde participó pero no ganó (excluyendo BYE)
    - Ordenado por victorias descendente
    
    :param db: Sesión de base de datos inyectada automáticamente.
    :return: Lista de entradas del ranking con player_id, nick, wins y losses.
    """
    try:
        leaderboard = reports_service.get_leaderboard(db)
        return leaderboard
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el ranking: {str(e)}")


@router.get("/tournaments/{tournament_id}/matches", response_model=List[MatchHistoryEntry])
def get_tournament_matches(tournament_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el historial de combates de un torneo específico.
    
    Devuelve todos los combates asociados a un torneo, incluyendo información
    de los participantes, el ganador y el estado del combate. Los resultados
    están ordenados por ronda y posición para facilitar la visualización
    del cuadro de eliminación.
    
    :param tournament_id: Identificador del torneo a consultar.
    :param db: Sesión de base de datos inyectada automáticamente.
    :return: Lista de combates con información completa de participantes y resultado.
    """
    try:
        matches = reports_service.get_tournament_matches(db, tournament_id)
        return matches
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener el historial del torneo: {str(e)}"
        )
