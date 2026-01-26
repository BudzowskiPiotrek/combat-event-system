export enum MatchStatus {
    PENDING = 'PENDING',
    RESOLVED = 'RESOLVED'
}

export interface Match {
    id: number;
    tournament_id: number;
    round: number;
    position: number;
    player1_id: number | null;
    player2_id: number | null;
    winner_id: number | null;
    status: MatchStatus;
}
