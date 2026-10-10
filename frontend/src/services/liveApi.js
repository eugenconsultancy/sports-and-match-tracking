import axios from '@/axios'

class LiveApiService {
    constructor() {
        this.baseURL = '/api/v1'
    }

    // ============ DATABASE ENDPOINTS ============

    async getDatabaseLiveMatches() {
        try {
            const response = await axios.get(`${this.baseURL}/matches/live/`)
            return response.data.matches || []
        } catch (error) {
            console.error('Failed to fetch database live matches:', error)
            return []
        }
    }

    async getTodayMatches() {
        try {
            const response = await axios.get(`${this.baseURL}/matches/today/`)
            return response.data
        } catch (error) {
            console.error('Failed to fetch today matches:', error)
            return []
        }
    }

    async getUpcomingMatches() {
        try {
            const response = await axios.get(`${this.baseURL}/matches/upcoming/`)
            return response.data.results || response.data || []
        } catch (error) {
            console.error('Failed to fetch upcoming matches:', error)
            return []
        }
    }

    // ============ ESPN FREE API ENDPOINTS ============

    async getLiveMatches(sport = 'soccer') {
        try {
            const response = await axios.get(`${this.baseURL}/matches/live_external/`, {
                params: { sport }
            })
            return response.data.matches || []
        } catch (error) {
            console.error('ESPN live matches failed:', error)
            return []
        }
    }

    async refreshLiveMatches(sport = 'soccer') {
        try {
            const response = await axios.get(`${this.baseURL}/matches/refresh_live/`, {
                params: { sport }
            })
            return response.data.matches || []
        } catch (error) {
            console.error('ESPN refresh failed:', error)
            return []
        }
    }

    async searchTeams(query, sport = 'soccer') {
        try {
            const response = await axios.get(`${this.baseURL}/matches/search_teams/`, {
                params: { q: query, sport }
            })
            return response.data.teams || []
        } catch (error) {
            console.error('ESPN team search failed:', error)
            return []
        }
    }

    // ============ FLASHSCORE API ENDPOINTS (Disabled) ============

    async searchFlashScore(query) {
        console.warn('FlashScore API is disabled. Use searchTeams() instead.')
        return []
    }

    async getFlashScoreLiveMatches() {
        console.warn('FlashScore API is disabled. Use getLiveMatches() instead.')
        return []
    }

    async getFlashScoreFixtures(date = null) {
        console.warn('FlashScore API is disabled. Use getUpcomingMatches() instead.')
        return []
    }

    async getFlashScoreMatchDetails(matchId) {
        console.warn('FlashScore API is disabled. Use getMatchDetails() instead.')
        return null
    }

    async getFlashScoreStandings(tournamentId) {
        console.warn('FlashScore API is disabled. Use standings endpoint instead.')
        return []
    }

    async getFlashScoreTeamInfo(teamId) {
        console.warn('FlashScore API is disabled. Use teams endpoint instead.')
        return null
    }

    // ============ GENERAL MATCH METHODS ============

    async getMatchDetails(matchId) {
        try {
            const response = await axios.get(`${this.baseURL}/matches/${matchId}/`)
            return response.data
        } catch (error) {
            console.error('Failed to fetch match details:', error)
            return null
        }
    }

    async getMatchEvents(matchId) {
        try {
            const response = await axios.get(`${this.baseURL}/matches/${matchId}/events/`)
            return response.data
        } catch (error) {
            console.error('Failed to fetch match events:', error)
            return []
        }
    }

    async getMatchLineups(matchId) {
        try {
            const response = await axios.get(`${this.baseURL}/matches/${matchId}/lineups/`)
            return response.data
        } catch (error) {
            console.error('Failed to fetch match lineups:', error)
            return []
        }
    }

    async getMatchStats(matchId) {
        try {
            const response = await axios.get(`${this.baseURL}/matches/${matchId}/stats/`)
            return response.data
        } catch (error) {
            console.error('Failed to fetch match stats:', error)
            return []
        }
    }
}

export const liveApi = new LiveApiService()
export default liveApi