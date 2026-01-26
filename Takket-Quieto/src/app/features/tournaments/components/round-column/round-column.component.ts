import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Match } from '../../../../models/match.model';
import { Player } from '../../../../models/player.model';

@Component({
    standalone: false,
    selector: 'app-round-column',
    templateUrl: './round-column.component.html',
    styleUrls: ['./round-column.component.css']
})
export class RoundColumnComponent {
    @Input() roundNumber!: number;
    @Input() matches: Match[] = [];
    @Input() participants: Player[] = [];
    @Output() winnerSelected = new EventEmitter<{ matchId: number, winnerId: number }>();

    onWinnerSelected(matchId: number, winnerId: number) {
        this.winnerSelected.emit({ matchId, winnerId });
    }

    get roundName(): string {
        return `Ronda ${this.roundNumber}`;
    }
}
