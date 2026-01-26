import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Match } from '../../../../models/match.model';
import { Player } from '../../../../models/player.model';

@Component({
    standalone: false,
    selector: 'app-bracket-view',
    templateUrl: './bracket-view.component.html',
    styleUrls: ['./bracket-view.component.css']
})
export class BracketViewComponent {
    @Input() matches: Match[] = [];
    @Input() participants: Player[] = [];
    @Output() winnerSelected = new EventEmitter<{ matchId: number, winnerId: number }>();

    get rounds(): number[] {
        const roundNumbers = this.matches.map(m => m.round);
        return Array.from(new Set(roundNumbers)).sort((a, b) => a - b);
    }

    getMatchesByRound(round: number): Match[] {
        return this.matches.filter(m => m.round === round).sort((a, b) => a.position - b.position);
    }

    onWinnerSelected(event: { matchId: number, winnerId: number }) {
        this.winnerSelected.emit(event);
    }
}
