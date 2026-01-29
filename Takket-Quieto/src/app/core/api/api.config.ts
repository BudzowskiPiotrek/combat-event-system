/**
 * Configuración centralizada de la API.
 * Define la URL base y los endpoints para acceder a los recursos del sistema de combate.
 */
export const API_CONFIG = {
    baseUrl: 'http://localhost:8000',
    endpoints: {
        players: '/players',
        tournaments: '/tournaments',
        matches: '/matches'
    }
};
