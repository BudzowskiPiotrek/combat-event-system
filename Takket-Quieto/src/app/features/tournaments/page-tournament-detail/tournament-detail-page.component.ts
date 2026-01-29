import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TournamentsService } from '../../../core/services/tournaments.service';
import { Tournament, TournamentStatus } from '../../../models/tournament.model';
import { Player } from '../../../models/player.model';
import { Match, MatchStatus } from '../../../models/match.model';
import { MatchesService } from '../../../core/services/matches.service';

@Component({
    standalone: false,
    selector: 'app-tournament-detail-page',
    templateUrl: './tournament-detail-page.component.html',
    styleUrls: ['./tournament-detail-page.component.css']
})
export class TournamentDetailPageComponent implements OnInit {
    tournament?: Tournament;
    participants: Player[] = [];
    matches: Match[] = [];
    loading = true;
    TournamentStatus = TournamentStatus;

    constructor(
        private route: ActivatedRoute,
        private tournamentsService: TournamentsService,
        private matchesService: MatchesService
    ) { }

    ngOnInit(): void {
        const id = Number(this.route.snapshot.paramMap.get('id'));
        if (id) {
            this.loadTournamentData(id);
        }
    }

    private loadTournamentData(id: number): void {
        this.tournamentsService.getById(id).subscribe({
            next: (data: Tournament) => {
                this.tournament = data;
                this.loadParticipants(id);
                if (this.tournament.status !== TournamentStatus.DRAFT) {
                    this.loadBracket(id);
                }
            },
            error: (err: any) => {
                console.error('Error loading tournament details:', err);
                this.loading = false;
            }
        });
    }

    loadParticipants(id: number): void {
        this.tournamentsService.getParticipants(id).subscribe({
            next: (data: Player[]) => {
                this.participants = data;
                this.loading = false;
            },
            error: (err: any) => {
                console.error('Error loading participants:', err);
                this.loading = false;
            }
        });
    }

    loadBracket(id: number): void {
        this.tournamentsService.getBracket(id).subscribe({
            next: (data: Match[]) => {
                this.matches = data;
                this.checkAndResolveByes();
            },
            error: (err: any) => console.error('Error loading bracket:', err)
        });
    }

    private checkAndResolveByes(): void {
        const byeMatches = this.matches.filter(m =>
            m.status === MatchStatus.PENDING &&
            m.player1_id &&
            !m.player2_id
        );

        if (byeMatches.length > 0) {
            byeMatches.forEach(match => {
                if (match.player1_id) {
                    this.matchesService.setWinner(match.id, match.player1_id).subscribe({
                        next: () => {
                            console.log(`Auto-resolved BYE match ${match.id}`);
                            // Reload data to reflect changes
                            if (this.tournament) {
                                this.loadBracket(this.tournament.id);
                            }
                        },
                        error: (err) => console.error(`Error auto-resolving BYE for match ${match.id}`, err)
                    });
                }
            });
        }
    }

    generateBracket(): void {
        if (!this.tournament) return;
        this.tournamentsService.generateBracket(this.tournament.id).subscribe({
            next: () => this.loadTournamentData(this.tournament!.id),
            error: (err: any) => alert('Error al generar bracket: ' + err.error.detail)
        });
    }

    generateNextRound(): void {
        if (!this.tournament) return;
        this.tournamentsService.generateNextRound(this.tournament.id).subscribe({
            next: () => this.loadTournamentData(this.tournament!.id),
            error: (err: any) => alert('Error al avanzar ronda: ' + err.error.detail)
        });
    }

    onWinnerSelected(event: { matchId: number, winnerId: number }): void {
        if (!this.tournament) return;
        this.matchesService.setWinner(event.matchId, event.winnerId).subscribe({
            next: () => this.loadTournamentData(this.tournament!.id),
            error: (err: any) => alert('Error al registrar ganador: ' + err.error.detail)
        });
    }

    get isNextRoundAvailable(): boolean {
        if (!this.tournament || this.matches.length === 0) return false;

        const lastRound = Math.max(...this.matches.map(m => m.round));
        const currentRoundMatches = this.matches.filter(m => m.round === lastRound);

        // Solo validamos los combates que REALMENTE tienen participantes.
        // Si un combate es TBD vs TBD, no debería bloquear el avance si el resto están listos.
        return currentRoundMatches.every(m => {
            const isGhostMatch = (m.player1_id === null && m.player2_id === null);
            return m.status === MatchStatus.RESOLVED || isGhostMatch;
        }) && currentRoundMatches.length > 0;
    }

    get winner(): Player | undefined {
        if (!this.tournament || !this.tournament.winner_id) return undefined;
        return this.participants.find(p => p.id === this.tournament?.winner_id);
    }
}
