import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TournamentsService } from '../../../core/services/tournaments.service';
import { Tournament } from '../../../models/tournament.model';
import { Player } from '../../../models/player.model';

@Component({
    selector: 'app-tournament-detail-page',
    templateUrl: './tournament-detail-page.component.html',
    styleUrls: ['./tournament-detail-page.component.css']
})
export class TournamentDetailPageComponent implements OnInit {
    tournament?: Tournament;
    participants: Player[] = [];
    loading = true;

    constructor(
        private route: ActivatedRoute,
        private tournamentsService: TournamentsService
    ) { }

    ngOnInit(): void {
        const id = Number(this.route.snapshot.paramMap.get('id'));
        if (id) {
            this.loadTournamentData(id);
        }
    }

    private loadTournamentData(id: number): void {
        this.tournamentsService.getById(id).subscribe({
            next: (data) => {
                this.tournament = data;
                this.loadParticipants(id);
            },
            error: (err) => {
                console.error('Error loading tournament details:', err);
                this.loading = false;
            }
        });
    }

    loadParticipants(id: number): void {
        this.tournamentsService.getParticipants(id).subscribe({
            next: (data) => {
                this.participants = data;
                this.loading = false;
            },
            error: (err) => {
                console.error('Error loading participants:', err);
                this.loading = false;
            }
        });
    }
}
