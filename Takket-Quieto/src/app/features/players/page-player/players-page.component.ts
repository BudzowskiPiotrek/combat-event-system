import { Component, OnInit } from '@angular/core';
import { PlayersService } from '../../../core/services/players.service';
import { Router } from '@angular/router';
import { Player } from '../../../models/player.model';

/**
 * Pagina principal del modulo de jugadores.
 * Responsabilidad: Contenedor principal de la feature Players.
 */
@Component({
    standalone: false,
    selector: 'app-players-page',
    templateUrl: './players-page.component.html',
    styleUrls: ['./players-page.component.css']
})
export class PlayersPageComponent implements OnInit {

    allPlayers: Player[] = [];
    filterType: 'all' | 'active' | 'inactive' = 'active';

    constructor(
        private playersService: PlayersService,
        private router: Router
    ) { }

    ngOnInit(): void {
        this.loadPlayers();
    }

    loadPlayers(): void {
        this.playersService.getAll().subscribe({
            next: (players) => {
                this.allPlayers = players;
            },
            error: (err) => {
                console.error('Error loading players:', err);
            }
        });
    }

    get displayedPlayers(): Player[] {
        if (this.filterType === 'active') {
            return this.allPlayers.filter(p => p.active);
        } else if (this.filterType === 'inactive') {
            return this.allPlayers.filter(p => !p.active);
        }
        return this.allPlayers;
    }

    setFilter(type: 'all' | 'active' | 'inactive'): void {
        this.filterType = type;
    }

    onNewPlayer(): void {
        this.router.navigate(['/players/new']);
    }

    onEditPlayer(id: number): void {
        this.router.navigate(['/players/edit', id]);
    }

    onTogglePlayer(id: number): void {
        this.playersService.toggleActive(id).subscribe({
            next: () => {
                this.loadPlayers();
            },
            error: (err) => {
                console.error('Error toggling player status:', err);
            }
        });
    }
}
