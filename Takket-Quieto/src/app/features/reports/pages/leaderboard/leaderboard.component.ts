import { Component, OnInit } from '@angular/core';
import { forkJoin, map, switchMap } from 'rxjs';
import { ReportsService, LeaderboardEntry } from '../../../../core/services/reports.service';
import { PlayersService } from '../../../../core/services/players.service';
import { TournamentsService } from '../../../../core/services/tournaments.service';
import { Match, MatchStatus } from '../../../../models/match.model';
import { Player } from '../../../../models/player.model';

@Component({
    standalone: false,
    selector: 'app-leaderboard',
    templateUrl: './leaderboard.component.html',
    styleUrls: ['./leaderboard.component.css']
})
export class LeaderboardComponent implements OnInit {
    leaderboard: LeaderboardEntry[] = [];
    loading = true;
    error: string | null = null;

    constructor(
        private reportsService: ReportsService,
        private playersService: PlayersService,
        private tournamentsService: TournamentsService
    ) { }

    ngOnInit(): void {
        this.loadData();
    }

    private loadData(): void {
        this.loading = true;

        forkJoin({
            players: this.playersService.getAll(),
            tournaments: this.tournamentsService.getAll()
        }).pipe(
            switchMap(({ players, tournaments }) => {
                const matchRequests = tournaments.map(t =>
                    this.reportsService.getTournamentMatches(t.id)
                );
                return forkJoin(matchRequests).pipe(
                    map(matchesArrays => {
                        const allMatches = matchesArrays.flat();
                        return { players, allMatches };
                    })
                );
            })
        ).subscribe({
            next: (data) => {
                this.calculateLeaderboard(data.players, data.allMatches);
                this.loading = false;
            },
            error: (err) => {
                console.error('Error calculating leaderboard:', err);
                this.error = 'Error al cargar el ranking de jugadores.';
                this.loading = false;
            }
        });
    }

    private calculateLeaderboard(players: Player[], matches: Match[]): void {
        const statsMap = new Map<number, { wins: number, defeats: number }>();

        // Initialize players in map
        players.forEach(p => {
            statsMap.set(p.id, { wins: 0, defeats: 0 });
        });

        matches.forEach(match => {
            if (match.status !== MatchStatus.RESOLVED || !match.winner_id) return;

            // Count Win
            const winnerStats = statsMap.get(match.winner_id);
            if (winnerStats) {
                winnerStats.wins++;
            }

            // Count Defeat
            // Logic: Participation + Not Winner + Not against BYE (Optional check, but mainly match must have 2 actual players to really be a "defeat" in some contexts? 
            // User said: "solo cuando el jugador participó en un match y no fue el ganador excluyendo BYEs")
            // A match against a BYE effectively has one player NULL.
            // If I am P1, and P2 is NULL -> I win. I don't lose.
            // If I am P1, and P2 is NOT NULL -> I play against real player.
            // If I lose (winner != me) -> It is a defeat.

            const isByeMatch = match.player1_id === null || match.player2_id === null;

            if (!isByeMatch) {
                // If it is not a bye match, the loser gets a defeat.
                if (match.player1_id && match.player1_id !== match.winner_id) {
                    const loserStats = statsMap.get(match.player1_id);
                    if (loserStats) loserStats.defeats++;
                }
                if (match.player2_id && match.player2_id !== match.winner_id) {
                    const loserStats = statsMap.get(match.player2_id);
                    if (loserStats) loserStats.defeats++;
                }
            }
        });

        // Convert to array and sort
        this.leaderboard = players.map(p => {
            const stats = statsMap.get(p.id) || { wins: 0, defeats: 0 };
            return {
                nick: p.nick,
                wins: stats.wins,
                defeats: stats.defeats
            };
        }).sort((a, b) => {
            // Sort by Wins desc, then Defeats asc (or just wins? Usually Wins).
            // User didn't specify sort order, assuming classic leaderboard.
            if (b.wins !== a.wins) return b.wins - a.wins;
            return a.defeats - b.defeats; // Less defeats is better? or just alphabetical?
        });

        // Filter out players with 0 games? Or keep all? 
        // User requested "Leaderboard", usually implies everyone or at least active. 
        // Existing implementation showed everyone. I'll keep everyone.
    }
}
