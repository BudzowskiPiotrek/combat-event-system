/**
 * Represents a player in the combat event system.
 * @interface Player
 * @property {number} id - The unique identifier for the player.
 * @property {string} nick - The player's nickname or display name.
 * @property {string} logoUrl - The URL pointing to the player's logo or avatar image.
 * @property {boolean} active - Indicates whether the player is currently active in the system.
 */
export interface Player {
    id: number;
    nick: string;
    logoUrl: string;
    active: boolean;

}
