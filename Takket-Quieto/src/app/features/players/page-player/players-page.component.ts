import { Component, OnInit } from '@angular/core';
import { PlayersService } from '../../../core/services/players.service';
import { Player } from '../../../models/player.model';

/**
 * Pagina principal del modulo de jugadores.
 * Responsabilidad: Contenedor principal de la feature Players.
 */
@Component({
    selector: 'app-players-page',
    templateUrl: './players-page.component.html',
    styleUrls: ['./players-page.component.css']
})
export class PlayersPageComponent implements OnInit {

    activePlayers: Player[] = [];
    inactivePlayers: Player[] = [];

    constructor(private playersService: PlayersService) { }

    ngOnInit(): void {
        this.loadPlayers();
    }

    loadPlayers(): void {
        this.playersService.getAll().subscribe({
            next: (players) => {
                this.activePlayers = players.filter(p => p.active);
                this.inactivePlayers = players.filter(p => !p.active);
            },
            error: (err) => {
                console.error('Error loading players:', err);
            }
        });
    }
}
