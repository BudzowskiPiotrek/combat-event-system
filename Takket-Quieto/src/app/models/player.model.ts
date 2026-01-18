export interface Player {
    id: number;
    nick: string;
    logoUrl: string;
    /**
     * Indica si el jugador esta habilitado para participar en torneos.
     * true = activo, false = inactivo (baja logica)
     */
    active: boolean;

}
