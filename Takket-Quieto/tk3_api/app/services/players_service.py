from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.player import Player
from ..schemas.player_schemas import PlayerCreate, PlayerUpdate

class PlayersService:
    """
    Servicio para gestionar la logica de negocio de jugadores.
    Sprint 1: Gestion de participantes.
    """

    def get_all(self, db: Session) -> List[Player]:
        """Obtiene todos los jugadores de la base de datos."""
        return db.query(Player).all()

    def get_by_id(self, db: Session, player_id: int) -> Optional[Player]:
        """Busca un jugador por su ID."""
        return db.query(Player).filter(Player.id == player_id).first()

    def create_player(self, db: Session, player: PlayerCreate) -> Player:
        """Crea un nuevo jugador en la base de datos."""
        db_player = Player(
            nick=player.nick,
            logo_url=player.logo_url,
            active=player.active
        )
        db.add(db_player)
        db.commit()
        db.refresh(db_player)
        return db_player

    def update_player(self, db: Session, player_id: int, player_update: PlayerUpdate) -> Optional[Player]:
        """Actualiza los datos de un jugador existente."""
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
        """Invierte el estado activo/inactivo de un jugador."""
        db_player = self.get_by_id(db, player_id)
        if not db_player:
            return None
            
        db_player.active = not db_player.active
        db.commit()
        db.refresh(db_player)
        return db_player

