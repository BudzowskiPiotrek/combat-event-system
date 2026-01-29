import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_CONFIG } from '../api/api.config';
import { Match } from '../../models/match.model';

/**
 * Servicio para gestionar operaciones relacionadas con partidas.
 * Proporciona métodos para interactuar con el API de matches.
 */
@Injectable({
    providedIn: 'root'
})
export class MatchesService {

    constructor(private http: HttpClient) { }

    setWinner(matchId: number, winnerId: number): Observable<Match> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.matches}/${matchId}/winner`;
        return this.http.post<Match>(url, { winner_id: winnerId });
    }
}
