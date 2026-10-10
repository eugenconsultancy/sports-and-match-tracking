export const MATCH_STATUS = {
    SCHEDULED: 'scheduled',
    LIVE: 'live',
    HALF_TIME: 'half_time',
    FINISHED: 'finished',
    POSTPONED: 'postponed',
    CANCELLED: 'cancelled',
    SUSPENDED: 'suspended',
}

export const MATCH_STATUS_LABELS = {
    [MATCH_STATUS.SCHEDULED]: 'Scheduled',
    [MATCH_STATUS.LIVE]: 'Live',
    [MATCH_STATUS.HALF_TIME]: 'Half Time',
    [MATCH_STATUS.FINISHED]: 'Full Time',
    [MATCH_STATUS.POSTPONED]: 'Postponed',
    [MATCH_STATUS.CANCELLED]: 'Cancelled',
    [MATCH_STATUS.SUSPENDED]: 'Suspended',
}

export const MATCH_STATUS_COLORS = {
    [MATCH_STATUS.SCHEDULED]: 'blue',
    [MATCH_STATUS.LIVE]: 'red',
    [MATCH_STATUS.HALF_TIME]: 'orange',
    [MATCH_STATUS.FINISHED]: 'gray',
    [MATCH_STATUS.POSTPONED]: 'yellow',
    [MATCH_STATUS.CANCELLED]: 'red',
    [MATCH_STATUS.SUSPENDED]: 'yellow',
}

export const EVENT_TYPES = {
    GOAL: 'goal',
    PENALTY_GOAL: 'penalty_goal',
    OWN_GOAL: 'own_goal',
    PENALTY_MISS: 'penalty_miss',
    YELLOW_CARD: 'yellow_card',
    SECOND_YELLOW: 'second_yellow',
    RED_CARD: 'red_card',
    SUBSTITUTION_IN: 'substitution_in',
    SUBSTITUTION_OUT: 'substitution_out',
    ASSIST: 'assist',
    HALF_TIME: 'half_time',
    FULL_TIME: 'full_time',
}

export const EVENT_ICONS = {
    [EVENT_TYPES.GOAL]: '⚽',
    [EVENT_TYPES.PENALTY_GOAL]: '🥅',
    [EVENT_TYPES.OWN_GOAL]: '🔴',
    [EVENT_TYPES.PENALTY_MISS]: '❌',
    [EVENT_TYPES.YELLOW_CARD]: '🟨',
    [EVENT_TYPES.SECOND_YELLOW]: '🟨🟥',
    [EVENT_TYPES.RED_CARD]: '🟥',
    [EVENT_TYPES.SUBSTITUTION_IN]: '🟢',
    [EVENT_TYPES.SUBSTITUTION_OUT]: '🔴',
    [EVENT_TYPES.ASSIST]: '🅰️',
    [EVENT_TYPES.HALF_TIME]: '⏸️',
    [EVENT_TYPES.FULL_TIME]: '⏹️',
}

export const PLAYER_POSITIONS = {
    GK: 'Goalkeeper',
    CB: 'Center Back',
    LB: 'Left Back',
    RB: 'Right Back',
    DM: 'Defensive Midfielder',
    CM: 'Central Midfielder',
    AM: 'Attacking Midfielder',
    LW: 'Left Winger',
    RW: 'Right Winger',
    CF: 'Center Forward',
    ST: 'Striker',
}

export const COMPETITION_TYPES = {
    LEAGUE: 'league',
    CUP: 'cup',
    INTERNATIONAL: 'international',
    FRIENDLY: 'friendly',
}

export const COMPETITION_TYPE_LABELS = {
    [COMPETITION_TYPES.LEAGUE]: 'League',
    [COMPETITION_TYPES.CUP]: 'Cup',
    [COMPETITION_TYPES.INTERNATIONAL]: 'International',
    [COMPETITION_TYPES.FRIENDLY]: 'Friendly',
}

export const TEAM_TYPES = {
    CLUB: 'club',
    NATIONAL: 'national',
}

export const NOTIFICATION_TYPES = {
    MATCH_START: 'match_start',
    GOAL: 'goal',
    RED_CARD: 'red_card',
    HALF_TIME: 'half_time',
    FULL_TIME: 'full_time',
    BREAKING_NEWS: 'breaking_news',
    TRANSFER: 'transfer',
    LINEUP: 'lineup',
}

export const STORAGE_KEYS = {
    ACCESS_TOKEN: 'access_token',
    REFRESH_TOKEN: 'refresh_token',
    THEME: 'theme',
    FAVORITES: 'favorites',
    SEARCH_HISTORY: 'search_history',
}

export const API_ENDPOINTS = {
    AUTH: {
        LOGIN: '/api/v1/auth/login/',
        REGISTER: '/api/v1/auth/register/',
        REFRESH: '/api/v1/auth/token/refresh/',
        ME: '/api/v1/auth/users/me/',
    },
    COMPETITIONS: '/api/v1/competitions/competitions/',
    MATCHES: '/api/v1/matches/matches/',
    TEAMS: '/api/v1/teams/teams/',
    PLAYERS: '/api/v1/players/players/',
    NEWS: '/api/v1/news/articles/',
    FAVORITES: '/api/v1/favorites/',
    POLLS: '/api/v1/polls/polls/',
    STANDINGS: '/api/v1/standings/standings/',
}

export const PAGINATION = {
    DEFAULT_PAGE_SIZE: 20,
    MAX_PAGE_SIZE: 100,
}

export const CACHE_KEYS = {
    COMPETITIONS: 'competitions',
    LIVE_MATCHES: 'live_matches',
    STANDINGS: 'standings',
    NEWS_FEATURED: 'news_featured',
    TOP_SCORERS: 'top_scorers',
}