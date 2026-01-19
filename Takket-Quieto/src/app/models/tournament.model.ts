export enum TournamentStatus {
    DRAFT = 'DRAFT',
    GENERATED = 'GENERATED'
}

export interface Tournament {
    id: number;
    name: string;
    status: TournamentStatus;
    created_at: string;
}
