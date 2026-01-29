/**
 * Represents the possible statuses of a match in the combat event system.
 * @enum {string}
 * @property {string} PENDING - The match is pending and has not yet started.
 * @property {string} RESOLVED - The match has concluded and a winner has been determined.
 */
export enum MatchStatus {
    PENDING = 'PENDING',
    RESOLVED = 'RESOLVED'
}

/**
 * Represents a match in the combat event system.
 * @interface Match
 * @property {number} id - The unique identifier for the match.
 * @property {number} tournament_id - The identifier for the tournament to which the match belongs.
 * @property {number} round - The round number of the match.
 * @property {number} position - The position of the match in the tournament's round.
 * @property {number | null} player1_id - The identifier for the first player in the match, or null if not assigned.
 * @property {number | null} player2_id - The identifier for the second player in the match, or null if not assigned.
 * @property {number | null} winner_id - The identifier for the winning player, or null if the match is not yet concluded.
 * @property {MatchStatus} status - The current status of the match.
 */
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
