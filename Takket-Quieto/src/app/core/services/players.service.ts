import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { API_CONFIG } from '../api/api.config';
import { Player } from '../../models/player.model';

@Injectable({
    providedIn: 'root'
})
/**
 * Servicio de gestión de jugadores.
 * 
 * Maneja la comunicación con el backend para operaciones CRUD de jugadores,
 * transformando automáticamente entre el formato snake_case del backend
 * y camelCase del frontend.
 */
export class PlayersService {

    constructor(private http: HttpClient) { }

    /**
     * Transforma un objeto del backend al modelo de dominio del frontend.
     * 
     * @param p Objeto sin procesar del backend en snake_case
     * @returns Objeto jugador con propiedades en camelCase
     */
    private mapToFrontend(p: any): Player {
        return {
            id: p.id,
            nick: p.nick,
            logoUrl: p.logo_url,
            active: p.active
        };
    }

    getAll(): Observable<Player[]> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}`;
        return this.http.get<any[]>(url).pipe(
            map(players => players.map(p => this.mapToFrontend(p)))
        );
    }

    getById(id: number): Observable<Player> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}/${id}`;
        return this.http.get<any>(url).pipe(
            map(p => this.mapToFrontend(p))
        );
    }

    /**
     * Crea un nuevo jugador con valores por defecto.
     * 
     * Si no se proporciona logoUrl, se envía un string vacío al backend.
     * El campo active defaults a true si no se especifica.
     * 
     * @param player Datos del jugador a crear
     */
    create(player: any): Observable<Player> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}`;
        const body = {
            nick: player.nick,
            logo_url: player.logoUrl || '',
            active: player.active !== undefined ? player.active : true
        };
        return this.http.post<any>(url, body).pipe(
            map(p => this.mapToFrontend(p))
        );
    }

    update(player: any): Observable<Player> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}/${player.id}`;
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
     * Alterna el estado activo/inactivo de un jugador en el backend.
     * 
     * El backend es responsable de calcular el nuevo estado.
     * 
     * @param id Identificador único del jugador
     */
    toggleActive(id: number): Observable<Player> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.players}/${id}/toggle`;
        return this.http.patch<any>(url, {}).pipe(
            map(p => this.mapToFrontend(p))
        );
    }
}

