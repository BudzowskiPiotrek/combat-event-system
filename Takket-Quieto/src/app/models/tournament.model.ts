/**
 * Represents the status of a tournament in the combat event system.
 * @enum {string} TournamentStatus
 * @property {string} DRAFT - The tournament is in draft status and not yet finalized.
 * @property {string} GENERATED - The tournament has been generated and is ready for participation.
 * @property {string} FINISHED - The tournament has concluded and results are finalized.
 */


export enum TournamentStatus {
    DRAFT = 'DRAFT',
    GENERATED = 'GENERATED',
    FINISHED = 'FINISHED'
}
/**
 * Represents a tournament in the combat event system.
 * @interface Tournament
 * @property {number} id - The unique identifier for the tournament.
 * @property {string} name - The name of the tournament.
 * @property {TournamentStatus} status - The current status of the tournament.
 * @property {string} created_at - The timestamp when the tournament was created.
 * @property {number | null} [winner_id] - The unique identifier of the tournament's winner, if applicable.
 */
export interface Tournament {
    id: number;
    name: string;
    status: TournamentStatus;
    created_at: string;
    winner_id?: number | null;
}
