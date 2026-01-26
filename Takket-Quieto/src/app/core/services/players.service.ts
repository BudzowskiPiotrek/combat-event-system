import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { API_CONFIG } from '../api/api.config';
import { Player } from '../../models/player.model';

@Injectable({
    providedIn: 'root'
})
export class PlayersService {

    constructor(private http: HttpClient) { }

    /**
     * Mapea un objeto del backend (snake_case) al frontend (camelCase).
     */
    private mapToFrontend(p: any): Player {
        return {
            id: p.id,
            nick: p.nick,
            logoUrl: p.logo_url,
            active: p.active
        };
    }

    /**
     * Obtiene todos los jugadores del backend.
     */
    getAll(): Observable<Player[]> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}`;
        return this.http.get<any[]>(url).pipe(
            map(players => players.map(p => this.mapToFrontend(p)))
        );
    }

    /**
     * Obtiene un jugador por su ID.
     * @param id ID del jugador
     */
    getById(id: number): Observable<Player> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}/${id}`;
        return this.http.get<any>(url).pipe(
            map(p => this.mapToFrontend(p))
        );
    }


    /**
     * Crea un nuevo jugador.
     * @param player Datos del jugador a crear
     */
    create(player: any): Observable<Player> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}`;
        // Mapeo de camelCase a snake_case para el backend
        const body = {
            nick: player.nick,
            logo_url: player.logoUrl || '',
            active: player.active !== undefined ? player.active : true
        };
        return this.http.post<any>(url, body).pipe(
            map(p => this.mapToFrontend(p))
        );
    }

    /**
     * Actualiza los datos básicos de un jugador.
     * @param player Jugador con datos actualizados
     */
    update(player: any): Observable<Player> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}/${player.id}`;
        // Mapeo de camelCase a snake_case para el backend
        const body = {
            nick: player.nick,
            logo_url: player.logoUrl,
            active: player.active
        };
        return this.http.put<any>(url, body).pipe(
            map(p => this.mapToFrontend(p))
        );
    }

    /**
     * Cambia el estado activo/inactivo de un jugador.
     * @param id ID del jugador
     */
    toggleActive(id: number): Observable<Player> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}/${id}/toggle`;
        return this.http.patch<any>(url, {}).pipe(
            map(p => this.mapToFrontend(p))
        );
    }
}

