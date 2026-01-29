import { Component, OnInit } from '@angular/core';
import { ReportsService } from '../../../../core/services/reports.service';
import { TournamentsService } from '../../../../core/services/tournaments.service';
import { Tournament } from '../../../../models/tournament.model';
import { Match, MatchStatus } from '../../../../models/match.model';
import { Player } from '../../../../models/player.model';

@Component({
    standalone: false,
    selector: 'app-history',
    templateUrl: './history.component.html',
    styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {
    tournaments: Tournament[] = [];
    selectedTournamentId: number | null = null;
    matches: Match[] = [];
    participants: Player[] = [];
    loading = false;
    error: string | null = null;

    constructor(
        private reportsService: ReportsService,
        private tournamentsService: TournamentsService
    ) { }

    ngOnInit(): void {
        this.loadTournaments();
    }

    loadTournaments(): void {
        this.loading = true;
        this.tournamentsService.getAll().subscribe({
            next: (data) => {
                this.tournaments = data;
                this.loading = false;
            },
            error: (err) => {
                console.error('Error loading tournaments:', err);
                this.error = 'Error al cargar lista de torneos.';
                this.loading = false;
            }
        });
    }

    onTournamentChange(event: Event): void {
        const select = event.target as HTMLSelectElement;
        const id = Number(select.value);
        if (id) {
            this.selectedTournamentId = id;
            this.loadTournamentData(id);
        } else {
            this.selectedTournamentId = null;
            this.matches = [];
            this.participants = [];
        }
    }

    loadTournamentData(id: number): void {
        this.loading = true;
        this.error = null;

        // Load participants first to map names, then matches
        this.tournamentsService.getParticipants(id).subscribe({
            next: (players) => {
                this.participants = players;
                this.reportsService.getTournamentMatches(id).subscribe({
                    next: (matches) => {
                        this.matches = matches;
                        this.loading = false;
                    },
                    error: (err) => {
                        console.error('Error loading matches:', err);
                        this.error = 'Error al cargar el historial de combates.';
                        this.loading = false;
                    }
                });
            },
            error: (err) => {
                console.error('Error loading participants:', err);
                this.error = 'Error al cargar participantes.';
                this.loading = false;
            }
        });
    }

    getPlayerName(id: number | null): string {
        if (id === null) return 'BYE';
        const player = this.participants.find(p => p.id === id);
        return player ? player.nick : 'Desconocido';
    }

    getWinnerName(match: Match): string {
        if (match.status !== MatchStatus.RESOLVED || !match.winner_id) return '-';
        return this.getPlayerName(match.winner_id);
    }
}
