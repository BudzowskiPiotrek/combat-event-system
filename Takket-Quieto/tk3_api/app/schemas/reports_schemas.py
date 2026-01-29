"""
Esquemas Pydantic para los endpoints de informes.

Este módulo define las estructuras de datos (DTOs) que se utilizan
para serializar las respuestas de los endpoints de informes, incluyendo
el ranking global de jugadores y el historial de combates.

Propósito académico: Separación clara entre modelos de base de datos
y modelos de transferencia de datos (DTO pattern).
"""

from pydantic import BaseModel
from typing import Optional


class LeaderboardEntry(BaseModel):
    """
    Representa una entrada en el ranking global de jugadores.

    Contiene las estadísticas de un jugador basadas en sus participaciones
    en combates resueltos. Se utiliza para mostrar la tabla de clasificación
    general del sistema.

    Atributos:
        player_id: Identificador único del jugador.
        nick: Nombre o apodo del jugador.
        wins: Número total de victorias (combates donde fue el ganador).
        losses: Número total de derrotas (combates donde participó pero no ganó).
    """

    player_id: int
    nick: str
    wins: int
    losses: int

    class Config:
        """Configuración para permitir la conversión desde objetos ORM."""

        from_attributes = True


class MatchHistoryEntry(BaseModel):
    """
    Representa un combate en el historial de un torneo.

    Contiene toda la información relevante de un enfrentamiento específico,
    incluyendo los participantes, el resultado y su ubicación en el cuadro.

    Atributos:
        match_id: Identificador único del combate.
        round: Número de ronda del torneo (1 = primera ronda, etc.).
        position: Posición del combate dentro de la ronda.
        player1_id: ID del primer participante (puede ser None si es hueco vacío).
        player1_nick: Nick del primer participante (puede ser None).
        player2_id: ID del segundo participante (None indica BYE).
        player2_nick: Nick del segundo participante (None indica BYE).
        winner_id: ID del ganador del combate (None si aún no está resuelto).
        winner_nick: Nick del ganador (None si aún no está resuelto).
        status: Estado del combate (PENDING o RESOLVED).
    """

    match_id: int
    round: int
    position: int
    player1_id: Optional[int]
    player1_nick: Optional[str]
    player2_id: Optional[int]
    player2_nick: Optional[str]
    winner_id: Optional[int]
    winner_nick: Optional[str]
    status: str

    class Config:
        """Configuración para permitir la conversión desde objetos ORM."""

        from_attributes = True
