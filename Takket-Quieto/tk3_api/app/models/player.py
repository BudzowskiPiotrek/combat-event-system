from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from ..core.db import Base

class Player(Base):
    """
    Modelo de Jugador.
    Representa a un participante en el sistema Takket-Quieto.
    """
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True)
    nick = Column(String(50), unique=True, index=True, nullable=False)
    logo_url = Column(String(255), nullable=True)
    
    # Campo active: controla si el jugador puede participar en torneos.
    # False implica baja logica, pero los datos persisten.
    active = Column(Boolean, default=True)
    

