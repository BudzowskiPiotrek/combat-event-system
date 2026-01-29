import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_CONFIG } from '../api/api.config';
import { Match } from '../../models/match.model';

export interface LeaderboardEntry {
    nick: string;
    wins: number;
    defeats: number;
}

@Injectable({
    providedIn: 'root'
})
export class ReportsService {

    constructor(private http: HttpClient) { }

    getLeaderboard(): Observable<LeaderboardEntry[]> {
        const url = `${API_CONFIG.baseUrl}/reports/leaderboard`;
        return this.http.get<LeaderboardEntry[]>(url);
    }

    getTournamentMatches(tournamentId: number): Observable<Match[]> {
        const url = `${API_CONFIG.baseUrl}/reports/tournaments/${tournamentId}/matches`;
        return this.http.get<Match[]>(url);
    }
}
