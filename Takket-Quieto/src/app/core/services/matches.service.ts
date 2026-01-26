import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_CONFIG } from '../api/api.config';
import { Match } from '../../models/match.model';

@Injectable({
    providedIn: 'root'
})
export class MatchesService {

    constructor(private http: HttpClient) { }

    /**
     * Describe el ganador de un match.
     * @param matchId ID del match
     * @param winnerId ID del ganador
     */
    setWinner(matchId: number, winnerId: number): Observable<Match> {
        const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.matches}/${matchId}/winner`;
        return this.http.post<Match>(url, { winner_id: winnerId });
    }
}
