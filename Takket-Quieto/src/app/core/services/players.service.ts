import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_CONFIG } from '../api/api.config';
import { Player } from '../../features/players/models/player.model';

@Injectable({
    providedIn: 'root'
})
export class PlayersService {

    constructor(private http: HttpClient) { }
    /**
     * Obtiene todos los jugadores del backend.
     */
    getAll(): Observable<Player[]> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}`;
        return this.http.get<Player[]>(url);
    }


    /**
     * Crea un nuevo jugador.
     * @param player Datos del jugador a crear
     */
    create(player: Player): Observable<Player> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}`;
        return this.http.post<Player>(url, player);
    }

    /**
     * Actualiza los datos básicos de un jugador.
     * @param player Jugador con datos actualizados
     */
    update(player: Player): Observable<Player> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}/${player.id}`;
        return this.http.put<Player>(url, player);
    }

    /**
     * Cambia el estado activo/inactivo de un jugador.
     * @param id ID del jugador
     */
    toggleActive(id: number): Observable<Player> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}/${id}/toggle`;
        return this.http.patch<Player>(url, {});
    }
}

