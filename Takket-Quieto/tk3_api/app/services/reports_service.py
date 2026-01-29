"""
Servicio de lógica de negocio para la generación de informes.

Este módulo implementa las operaciones necesarias para calcular estadísticas
y generar informes basados en los datos de combates y torneos almacenados
en la base de datos.

Propósito académico: Encapsular la lógica de negocio compleja separada
de los controladores (routers), siguiendo el principio de responsabilidad única (SOLID).
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.match import Match, MatchStatus
from ..models.player import Player
from ..schemas.reports_schemas import LeaderboardEntry, MatchHistoryEntry


class ReportsService:
    """
    Servicio encargado de generar informes y estadísticas del sistema.

    Proporciona métodos para calcular el ranking global de jugadores
    y obtener el historial detallado de combates de un torneo específico.
    """

    def get_leaderboard(self, db: Session) -> List[LeaderboardEntry]:
        """
        Genera el ranking global de jugadores basado en sus victorias y derrotas.

        Calcula las estadísticas de cada jugador contabilizando únicamente
        los combates que han sido resueltos (status = RESOLVED). No se cuentan
        como derrotas los combates BYE (donde player2_id es NULL).

        Lógica de conteo:
        - Victoria: El jugador es el winner_id del combate.
        - Derrota: El jugador participó (player1_id o player2_id) pero no ganó,
          y el combate NO es BYE (player2_id no es NULL).

        :param db: Sesión de la base de datos.
        :return: Lista de entradas del ranking ordenadas por victorias descendente.
        """
        # Obtener todos los jugadores activos
        players = db.query(Player).all()

        leaderboard = []

        for player in players:
            # Contar victorias: combates resueltos donde este jugador ganó
            wins = (
                db.query(Match)
                .filter(
                    and_(
                        Match.winner_id == player.id,
                        Match.status == MatchStatus.RESOLVED,
                    )
                )
                .count()
            )

            # Contar derrotas: combates resueltos donde participó pero no ganó
            # y que NO sean BYE (player2_id no es NULL)
            losses = (
                db.query(Match)
                .filter(
                    and_(
                        Match.status == MatchStatus.RESOLVED,
                        Match.player2_id.isnot(None),  # NO contar BYE
                        Match.winner_id != player.id,  # No ganó
                        # Participó como player1 o player2
                        (
                            (Match.player1_id == player.id)
                            | (Match.player2_id == player.id)
                        ),
                    )
                )
                .count()
            )

            # Solo incluir jugadores que han participado en al menos un combate
            if wins > 0 or losses > 0:
                leaderboard.append(
                    LeaderboardEntry(
                        player_id=player.id, nick=player.nick, wins=wins, losses=losses
                    )
                )

        # Ordenar por victorias descendente, luego por derrotas ascendente
        leaderboard.sort(key=lambda x: (-x.wins, x.losses))

        return leaderboard

    def get_tournament_matches(
        self, db: Session, tournament_id: int
    ) -> List[MatchHistoryEntry]:
        """
        Obtiene el historial completo de combates de un torneo específico.

        Recupera todos los combates asociados a un torneo, incluyendo
        la información de los participantes y el resultado, ordenados
        por ronda y posición para facilitar la visualización del cuadro.

        :param db: Sesión de la base de datos.
        :param tournament_id: Identificador del torneo a consultar.
        :return: Lista de combates ordenados por ronda y posición.
        """
        # Obtener todos los combates del torneo ordenados
        matches = (
            db.query(Match)
            .filter(Match.tournament_id == tournament_id)
            .order_by(Match.round, Match.position)
            .all()
        )

        history = []

        for match in matches:
            # Obtener información del jugador 1
            player1 = None
            if match.player1_id:
                player1 = db.query(Player).filter(Player.id == match.player1_id).first()

            # Obtener información del jugador 2 (puede ser None si es BYE)
            player2 = None
            if match.player2_id:
                player2 = db.query(Player).filter(Player.id == match.player2_id).first()

            # Obtener información del ganador (puede ser None si está pendiente)
            winner = None
            if match.winner_id:
                winner = db.query(Player).filter(Player.id == match.winner_id).first()

            history.append(
                MatchHistoryEntry(
                    match_id=match.id,
                    round=match.round,
                    position=match.position,
                    player1_id=match.player1_id,
                    player1_nick=player1.nick if player1 else None,
                    player2_id=match.player2_id,
                    player2_nick=player2.nick if player2 else None,
                    winner_id=match.winner_id,
                    winner_nick=winner.nick if winner else None,
                    status=match.status.value,
                )
            )

        return history
