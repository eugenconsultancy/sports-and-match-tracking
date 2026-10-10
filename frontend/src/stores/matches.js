import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from '@/axios'

export const useMatchStore = defineStore('matches', () => {
    const matches = ref([])
    const liveMatches = ref([])
    const currentMatch = ref(null)
    const loading = ref(false)
    const wsConnection = ref(null)

    // WebSocket connection for live matches
    function connectToLiveMatches() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        const wsUrl = `${protocol}//localhost:8001/ws/matches/live`

        wsConnection.value = new WebSocket(wsUrl)

        wsConnection.value.onopen = () => {
            console.log('Connected to live matches WebSocket')
        }

        wsConnection.value.onmessage = (event) => {
            const data = JSON.parse(event.data)

            if (data.type === 'initial_live_matches' || data.type === 'live_matches_update') {
                liveMatches.value = data.data
            }
        }

        wsConnection.value.onclose = () => {
            console.log('WebSocket disconnected, reconnecting in 5s...')
            setTimeout(() => connectToLiveMatches(), 5000)
        }

        wsConnection.value.onerror = (error) => {
            console.error('WebSocket error:', error)
        }
    }

    function connectToMatch(matchId, onUpdate, onEvent) {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        const wsUrl = `${protocol}//localhost:8001/ws/match/${matchId}`

        const ws = new WebSocket(wsUrl)

        ws.onopen = () => {
            console.log(`Connected to match ${matchId} WebSocket`)
        }

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data)

            if (data.type === 'match_state' || data.type === 'match_update') {
                currentMatch.value = data.data
                if (onUpdate) onUpdate(data.data)
            }

            if (data.type === 'match_event') {
                if (onEvent) onEvent(data.data)
            }

            if (data.type === 'live_state_update') {
                currentMatch.value = {
                    ...currentMatch.value,
                    live_state: data.data,
                }
                if (onUpdate) onUpdate(currentMatch.value)
            }
        }

        ws.onclose = () => {
            console.log(`Match ${matchId} WebSocket disconnected`)
        }

        return ws
    }

    async function fetchMatches(params = {}) {
        loading.value = true
        try {
            const response = await axios.get('/api/v1/matches/matches/', { params })
            matches.value = response.data.results || response.data
            return matches.value
        } catch (error) {
            console.error('Failed to fetch matches:', error)
            return []
        } finally {
            loading.value = false
        }
    }

    async function fetchLiveMatches() {
        try {
            const response = await axios.get('/api/v1/matches/matches/live/')
            liveMatches.value = response.data.matches || response.data
            return liveMatches.value
        } catch (error) {
            console.error('Failed to fetch live matches:', error)
            return []
        }
    }

    async function fetchMatchDetail(matchId) {
        loading.value = true
        try {
            const response = await axios.get(`/api/v1/matches/matches/${matchId}/`)
            currentMatch.value = response.data
            return response.data
        } catch (error) {
            console.error('Failed to fetch match detail:', error)
            return null
        } finally {
            loading.value = false
        }
    }

    async function fetchTodayMatches() {
        try {
            const response = await axios.get('/api/v1/matches/matches/today/')
            return response.data
        } catch (error) {
            console.error('Failed to fetch today matches:', error)
            return []
        }
    }

    return {
        matches,
        liveMatches,
        currentMatch,
        loading,
        connectToLiveMatches,
        connectToMatch,
        fetchMatches,
        fetchLiveMatches,
        fetchMatchDetail,
        fetchTodayMatches,
    }
})