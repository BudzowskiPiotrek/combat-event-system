export enum TournamentStatus {
    DRAFT = 'DRAFT',
    GENERATED = 'GENERATED',
    FINISHED = 'FINISHED'
}

export interface Tournament {
    id: number;
    name: string;
    status: TournamentStatus;
    created_at: string;
    winner_id?: number | null;
}
