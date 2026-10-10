import axios from '@/axios'

class ApiService {
    constructor() {
        this.baseURL = '/api/v1'
    }

    // Competitions
    async getCompetitions(params = {}) {
        try {
            const response = await axios.get(`${this.baseURL}/competitions/`, { params })
            return response.data
        } catch (error) {
            console.error('API Error - getCompetitions:', error)
            return { results: [], count: 0 }
        }
    }

    async getCompetition(id) {
        try {
            const response = await axios.get(`${this.baseURL}/competitions/${id}/`)
            return response.data
        } catch (error) {
            console.error('API Error - getCompetition:', error)
            return null
        }
    }

    async getCompetitionStandings(competitionId) {
        try {
            // Primary endpoint: /api/v1/competitions/{id}/standings/
            let response
            try {
                response = await axios.get(`${this.baseURL}/competitions/${competitionId}/standings/`)
            } catch (firstError) {
                // Fallback: /api/v1/standings/ (with filter param)
                response = await axios.get(`${this.baseURL}/standings/`, {
                    params: { competition_season__competition: competitionId }
                })
            }
            return response.data
        } catch (error) {
            console.warn(`Standings not available for competition ${competitionId}:`, error.message)
            return []
        }
    }

    async getCompetitionSeasons(competitionId) {
        try {
            const response = await axios.get(`${this.baseURL}/competitions/${competitionId}/seasons/`)
            return response.data
        } catch (error) {
            console.error('API Error - getCompetitionSeasons:', error)
            return { results: [] }
        }
    }

    // Matches
    async getMatches(params = {}) {
        try {
            const response = await axios.get(`${this.baseURL}/matches/`, { params })
            return response.data
        } catch (error) {
            console.error('API Error - getMatches:', error)
            return { results: [] }
        }
    }

    async getLiveMatches() {
        try {
            const response = await axios.get(`${this.baseURL}/matches/live/`)
            return response.data
        } catch (error) {
            console.error('API Error - getLiveMatches:', error)
            return { matches: [] }
        }
    }

    async getMatch(id) {
        try {
            const response = await axios.get(`${this.baseURL}/matches/${id}/`)
            return response.data
        } catch (error) {
            console.error('API Error - getMatch:', error)
            return null
        }
    }

    async getTodayMatches() {
        try {
            const response = await axios.get(`${this.baseURL}/matches/today/`)
            return response.data
        } catch (error) {
            console.error('API Error - getTodayMatches:', error)
            return []
        }
    }

    // Teams
    async getTeams(params = {}) {
        try {
            const response = await axios.get(`${this.baseURL}/teams/`, { params })
            return response.data
        } catch (error) {
            console.error('API Error - getTeams:', error)
            return { results: [] }
        }
    }

    async getTeam(id) {
        try {
            const response = await axios.get(`${this.baseURL}/teams/${id}/`)
            return response.data
        } catch (error) {
            console.error('API Error - getTeam:', error)
            return null
        }
    }

    async getTeamPlayers(teamId) {
        try {
            const response = await axios.get(`${this.baseURL}/teams/${teamId}/players/`)
            return response.data
        } catch (error) {
            console.error('API Error - getTeamPlayers:', error)
            return { results: [] }
        }
    }

    async getTeamMatches(teamId) {
        try {
            const response = await axios.get(`${this.baseURL}/teams/${teamId}/matches/`)
            return response.data
        } catch (error) {
            console.error('API Error - getTeamMatches:', error)
            return { upcoming: [], recent: [] }
        }
    }

    async getTeamTransfers(teamId) {
        try {
            const response = await axios.get(`${this.baseURL}/teams/${teamId}/transfers/`)
            return response.data
        } catch (error) {
            console.error('API Error - getTeamTransfers:', error)
            return { results: [] }
        }
    }

    // Players
    async getPlayers(params = {}) {
        try {
            const response = await axios.get(`${this.baseURL}/players/`, { params })
            return response.data
        } catch (error) {
            console.error('API Error - getPlayers:', error)
            return { results: [] }
        }
    }

    async getPlayer(id) {
        try {
            const response = await axios.get(`${this.baseURL}/players/${id}/`)
            return response.data
        } catch (error) {
            console.error('API Error - getPlayer:', error)
            return null
        }
    }

    async getPlayerStats(playerId) {
        try {
            const response = await axios.get(`${this.baseURL}/players/${playerId}/stats/`)
            return response.data
        } catch (error) {
            console.error('API Error - getPlayerStats:', error)
            return { season_stats: [], recent_matches: [], transfers: [] }
        }
    }

    // News
    async getArticles(params = {}) {
        try {
            const response = await axios.get(`${this.baseURL}/news/articles/`, { params })
            return response.data
        } catch (error) {
            console.error('API Error - getArticles:', error)
            return { results: [] }
        }
    }

    async getArticle(id) {
        try {
            const response = await axios.get(`${this.baseURL}/news/articles/${id}/`)
            return response.data
        } catch (error) {
            console.error('API Error - getArticle:', error)
            return null
        }
    }

    async getBreakingNews() {
        try {
            const response = await axios.get(`${this.baseURL}/news/articles/breaking/`)
            return response.data
        } catch (error) {
            console.error('API Error - getBreakingNews:', error)
            return []
        }
    }

    async getFeaturedNews() {
        try {
            const response = await axios.get(`${this.baseURL}/news/articles/featured/`)
            return response.data
        } catch (error) {
            console.error('API Error - getFeaturedNews:', error)
            return []
        }
    }

    async getCategories() {
        try {
            const response = await axios.get(`${this.baseURL}/news/categories/`)
            return response.data
        } catch (error) {
            console.error('API Error - getCategories:', error)
            return { results: [] }
        }
    }

    // Favorites
    async getFavoriteTeams() {
        try {
            const response = await axios.get(`${this.baseURL}/favorites/teams/`)
            return response.data
        } catch (error) {
            console.error('API Error - getFavoriteTeams:', error)
            return { results: [] }
        }
    }

    async getFavoriteMatches() {
        try {
            const response = await axios.get(`${this.baseURL}/favorites/matches/`)
            return response.data
        } catch (error) {
            console.error('API Error - getFavoriteMatches:', error)
            return { results: [] }
        }
    }

    async addFavorite(type, id) {
        const endpoints = {
            team: `${this.baseURL}/favorites/teams/add/`,
            match: `${this.baseURL}/favorites/matches/add/`,
            competition: `${this.baseURL}/favorites/competitions/add/`,
        }
        try {
            const response = await axios.post(endpoints[type], { entity_type: type, entity_id: id })
            return response.data
        } catch (error) {
            console.error('API Error - addFavorite:', error)
            return null
        }
    }

    async removeFavorite(type, id) {
        const endpoints = {
            team: `${this.baseURL}/favorites/teams/remove/`,
            match: `${this.baseURL}/favorites/matches/remove/`,
            competition: `${this.baseURL}/favorites/competitions/remove/`,
        }
        try {
            const response = await axios.delete(endpoints[type], { data: { entity_id: id } })
            return response.data
        } catch (error) {
            console.error('API Error - removeFavorite:', error)
            return null
        }
    }

    // Polls
    async getPolls(params = {}) {
        try {
            const response = await axios.get(`${this.baseURL}/polls/`, { params })
            return response.data
        } catch (error) {
            console.error('API Error - getPolls:', error)
            return { results: [] }
        }
    }

    async getPoll(id) {
        try {
            const response = await axios.get(`${this.baseURL}/polls/${id}/`)
            return response.data
        } catch (error) {
            console.error('API Error - getPoll:', error)
            return null
        }
    }

    async vote(pollId, optionId) {
        try {
            const response = await axios.post(`${this.baseURL}/polls/${pollId}/vote/`, { option_id: optionId })
            return response.data
        } catch (error) {
            console.error('API Error - vote:', error)
            return null
        }
    }

    // Standings
    async getStandings(params = {}) {
        try {
            const response = await axios.get(`${this.baseURL}/standings/`, { params })
            return response.data
        } catch (error) {
            console.error('API Error - getStandings:', error)
            return { results: [] }
        }
    }

    // Search
    async search(query, types = ['teams', 'players', 'competitions']) {
        const results = {}

        if (types.includes('teams')) {
            try {
                const teams = await this.getTeams({ search: query, limit: 10 })
                results.teams = teams.results || teams
            } catch { results.teams = [] }
        }

        if (types.includes('players')) {
            try {
                const players = await this.getPlayers({ search: query, limit: 10 })
                results.players = players.results || players
            } catch { results.players = [] }
        }

        if (types.includes('competitions')) {
            try {
                const comps = await this.getCompetitions({ search: query, limit: 10 })
                results.competitions = comps.results || comps
            } catch { results.competitions = [] }
        }

        return results
    }
}

export const api = new ApiService()
export default api