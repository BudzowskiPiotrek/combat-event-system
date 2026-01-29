import { Component, OnInit } from '@angular/core';
import { ReportsService, LeaderboardEntry } from '../../../../core/services/reports.service';

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

    constructor(private reportsService: ReportsService) { }

    ngOnInit(): void {
        this.reportsService.getLeaderboard().subscribe({
            next: (data) => {
                this.leaderboard = data;
                this.loading = false;
            },
            error: (err) => {
                console.error('Error loading leaderboard:', err);
                this.error = 'Error al cargar el ranking de jugadores.';
                this.loading = false;
            }
        });
    }
}
