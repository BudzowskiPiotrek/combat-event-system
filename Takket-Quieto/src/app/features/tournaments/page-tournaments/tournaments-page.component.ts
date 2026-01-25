import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TournamentsService } from '../../../core/services/tournaments.service';
import { Tournament } from '../../../models/tournament.model';

@Component({
    standalone: false,
    selector: 'app-tournaments-page',
    templateUrl: './tournaments-page.component.html',
    styleUrls: ['./tournaments-page.component.css']
})
export class TournamentsPageComponent implements OnInit {
    tournaments: Tournament[] = [];

    constructor(
        private tournamentsService: TournamentsService,
        private router: Router
    ) { }

    ngOnInit(): void {
        this.loadTournaments();
    }

    loadTournaments(): void {
        this.tournamentsService.getAll().subscribe({
            next: (data) => {
                this.tournaments = data;
            },
            error: (err) => {
                console.error('Error loading tournaments:', err);
            }
        });
    }

    onNewTournament(): void {
        this.router.navigate(['/tournaments/new']);
    }

    onViewDetails(id: number): void {
        this.router.navigate(['/tournaments', id]);
    }
}
