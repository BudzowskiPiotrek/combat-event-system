import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Match, MatchStatus } from '../../../../models/match.model';
import { Player } from '../../../../models/player.model';

@Component({
    standalone: false,
    selector: 'app-match-card',
    templateUrl: './match-card.component.html',
    styleUrls: ['./match-card.component.css']
})
export class MatchCardComponent {
    @Input() match!: Match;
    @Input() participants: Player[] = [];
    @Output() winnerSelected = new EventEmitter<number>();

    get player1(): Player | undefined {
        return this.participants.find(p => p.id === this.match.player1_id);
    }

    get player2(): Player | undefined {
        return this.participants.find(p => p.id === this.match.player2_id);
    }

    get isBye(): boolean {
        return !!(this.match.player1_id && !this.match.player2_id && this.match.status === MatchStatus.RESOLVED);
    }

    selectWinner(playerId: number | null) {
        if (!playerId) return;
        if (this.match.status === MatchStatus.RESOLVED) return;

        if (confirm(`¿Confirmar a ${this.getPlayerNick(playerId)} como ganador?`)) {
            this.winnerSelected.emit(playerId);
        }
    }

    getPlayerNick(playerId: number | null): string {
        if (!playerId) return 'TBD';
        const player = this.participants.find(p => p.id === playerId);
        return player ? player.nick : 'BYE';
    }

    isWinner(playerId: number | null): boolean {
        return this.match.status === MatchStatus.RESOLVED && this.match.winner_id === playerId;
    }
}
