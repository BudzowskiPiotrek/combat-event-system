import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { PlayersService } from '../../../../core/services/players.service';
import { TournamentsService } from '../../../../core/services/tournaments.service';
import { Player } from '../../../../models/player.model';
import { forkJoin } from 'rxjs';

@Component({
    selector: 'app-participant-picker',
    templateUrl: './participant-picker.component.html',
    styleUrls: ['./participant-picker.component.css']
})
export class ParticipantPickerComponent implements OnInit {
    @Input() tournamentId!: number;
    @Output() participantsAdded = new EventEmitter<void>();

    availablePlayers: Player[] = [];
    selectedPlayerIds: Set<number> = new Set();
    loading = true;
    saving = false;

    constructor(
        private playersService: PlayersService,
        private tournamentsService: TournamentsService
    ) { }

    ngOnInit(): void {
        this.loadAvailablePlayers();
    }

    loadAvailablePlayers(): void {
        this.playersService.getAll().subscribe({
            next: (players) => {
                // SOLO jugadores activos
                this.availablePlayers = players.filter(p => p.active);
                this.loading = false;
            },
            error: (err) => {
                console.error('Error loading players:', err);
                this.loading = false;
            }
        });
    }

    onToggleSelection(playerId: number | undefined): void {
        if (!playerId) return;

        if (this.selectedPlayerIds.has(playerId)) {
            this.selectedPlayerIds.delete(playerId);
        } else {
            this.selectedPlayerIds.add(playerId);
        }
    }

    onSave(): void {
        if (this.selectedPlayerIds.size === 0) return;

        this.saving = true;
        const requests = Array.from(this.selectedPlayerIds).map(id =>
            this.tournamentsService.addParticipant(this.tournamentId, id)
        );

        forkJoin(requests).subscribe({
            next: () => {
                this.saving = false;
                this.selectedPlayerIds.clear();
                this.participantsAdded.emit();
            },
            error: (err) => {
                console.error('Error adding participants:', err);
                this.saving = false;
            }
        });
    }
}
