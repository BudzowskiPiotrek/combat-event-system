from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.player import Player
from ..schemas.player_schemas import PlayerCreate, PlayerUpdate


class PlayersService:
    """
    Servicio encargado de la lógica de negocio relacionada con los jugadores.

    Proporciona métodos para la gestión integral de participantes, incluyendo
    su creación, recuperación, actualización y gestión de su estado de activación.
    """

    def get_all(self, db: Session) -> List[Player]:
        """
        Recupera la lista completa de jugadores registrados en el sistema.

        :param db: Sesión de la base de datos.
        :return: Lista de objetos Player.
        """
        return db.query(Player).all()

    def get_by_id(self, db: Session, player_id: int) -> Optional[Player]:
        """
        Busca un jugador específico mediante su identificador único.

        :param db: Sesión de la base de datos.
        :param player_id: Identificador único del jugador.
        :return: El jugador encontrado o None si no existe.
        """
        return db.query(Player).filter(Player.id == player_id).first()

    def create_player(self, db: Session, player: PlayerCreate) -> Player:
        """
        Registra un nuevo jugador en el sistema.
        Incluye un workaround para el error de duplicidad de ID 0 si el auto-incremento falla.
        """
        # Obtenemos el ID mas alto actual para evitar el error 'Duplicate entry 0'
        # si la tabla no tiene AUTO_INCREMENT configurado correctamente.
        max_id = db.query(Player.id).order_by(Player.id.desc()).first()
        next_id = (max_id[0] + 1) if max_id else 1

        db_player = Player(
            id=next_id, nick=player.nick, logo_url=player.logo_url, active=player.active
        )
        db.add(db_player)
        db.commit()
        db.refresh(db_player)
        return db_player

    def update_player(
        self, db: Session, player_id: int, player_update: PlayerUpdate
    ) -> Optional[Player]:
        """
        Actualiza la información de un jugador existente de forma parcial.

        :param db: Sesión de la base de datos.
        :param player_id: Identificador del jugador a modificar.
        :param player_update: Objeto con los campos a actualizar.
        :return: El jugador actualizado o None si no se encontró.
        """
        db_player = self.get_by_id(db, player_id)
        if not db_player:
            return None

        # Actualizamos solo los campos provistos
        if player_update.nick is not None:
            db_player.nick = player_update.nick
        if player_update.logo_url is not None:
            db_player.logo_url = player_update.logo_url
        if player_update.active is not None:
            db_player.active = player_update.active

        db.commit()
        db.refresh(db_player)
        return db_player

    def toggle_active(self, db: Session, player_id: int) -> Optional[Player]:
        """
        Alterna el estado de activación de un jugador (baja lógica).

        :param db: Sesión de la base de datos.
        :param player_id: Identificador del jugador.
        :return: El jugador con su estado modificado o None si no existe.
        """
        db_player = self.get_by_id(db, player_id)
        if not db_player:
            return None

        db_player.active = not db_player.active
        db.commit()
        db.refresh(db_player)
        return db_player
