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
/**
 * Servicio para gestionar torneos.
 * Proporciona operaciones CRUD, gestión de participantes y generación de brackets
 * para torneos de combate.
 */
export class TournamentsService {

    constructor(private http: HttpClient) { }

    getAll(): Observable<Tournament[]> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}`;
        return this.http.get<Tournament[]>(url);
    }


    create(tournament: Partial<Tournament>): Observable<Tournament> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}`;
        return this.http.post<Tournament>(url, tournament);
    }


    update(tournament: Partial<Tournament>): Observable<Tournament> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}/${tournament.id}`;
        return this.http.put<Tournament>(url, tournament);
    }


    getById(id: number): Observable<Tournament> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}/${id}`;
        return this.http.get<Tournament>(url);
    }


    getParticipants(id: number): Observable<Player[]> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}/${id}/participants`;
        return this.http.get<Player[]>(url);
    }


    addParticipant(tournamentId: number, playerId: number): Observable<Player> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}/${tournamentId}/participants`;
        return this.http.post<Player>(url, { player_id: playerId });
    }


    generateBracket(id: number): Observable<Match[]> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}/${id}/generate`;
        return this.http.post<Match[]>(url, {});
    }

    generateNextRound(id: number): Observable<Match[]> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}/${id}/next-round`;
        return this.http.post<Match[]>(url, {});
    }


    getBracket(id: number): Observable<Match[]> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.tournaments}/${id}/bracket`;
        return this.http.get<Match[]>(url);
    }
}
