import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_CONFIG } from '../api/api.config';
import { Tournament } from '../../models/tournament.model';
import { Player } from '../../models/player.model';
import { Match } from '../../models/match.model';

@Injectable({
    providedIn: 'root'
})
export class TournamentsService {

    constructor(private http: HttpClient) { }

    /**
     * Obtiene todos los torneos del backend.
     */
    getAll(): Observable<Tournament[]> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}`;
        return this.http.get<Tournament[]>(url);
    }

    /**
     * Crea un nuevo torneo.
     * @param tournament Datos del torneo a crear (solo nombre por ahora)
     */
    create(tournament: Partial<Tournament>): Observable<Tournament> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}`;
        return this.http.post<Tournament>(url, tournament);
    }

    /**
     * Obtiene los detalles de un torneo.
     * @param id ID del torneo
     */
    getById(id: number): Observable<Tournament> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}/${id}`;
        return this.http.get<Tournament>(url);
    }

    /**
     * Obtiene los participantes inscritos en un torneo.
     * @param id ID del torneo
     */
    getParticipants(id: number): Observable<Player[]> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}/${id}/participants`;
        return this.http.get<Player[]>(url);
    }

    /**
     * Añade un participante al torneo.
     * @param tournamentId ID del torneo
     * @param playerId ID del jugador
     */
    addParticipant(tournamentId: number, playerId: number): Observable<Player> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}/${tournamentId}/participants`;
        return this.http.post<Player>(url, { player_id: playerId });
    }

    /**
     * Genera la primera ronda del torneo.
     * @param id ID del torneo
     */
    generateBracket(id: number): Observable<Match[]> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}/${id}/generate`;
        return this.http.post<Match[]>(url, {});
    }

    /**
     * Genera la siguiente ronda del torneo.
     * @param id ID del torneo
     */
    generateNextRound(id: number): Observable<Match[]> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}/${id}/next-round`;
        return this.http.post<Match[]>(url, {});
    }

    /**
     * Obtiene el bracket de un torneo.
     * @param id ID del torneo
     */
    getBracket(id: number): Observable<Match[]> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}/${id}/bracket`;
        return this.http.get<Match[]>(url);
    }
}
