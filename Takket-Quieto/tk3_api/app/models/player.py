from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from ..core.db import Base


class Player(Base):
    """
    Entidad que representa a un jugador en el sistema.

    Un jugador es un participante que puede ser inscrito en distintos
    torneos. Se gestiona su identidad visual (logo) y su estado de disponibilidad.
    """

    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True)
    nick = Column(String(50), unique=True, index=True, nullable=False)
    logo_url = Column(String(255), nullable=True)

    # Campo active: controla si el jugador puede participar en torneos.
    # False implica baja logica, pero los datos persisten.
    active = Column(Boolean, default=True)
