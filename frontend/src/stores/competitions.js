import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from '@/axios'

export const useCompetitionStore = defineStore('competitions', () => {
    const competitions = ref([])
    const currentCompetition = ref(null)
    const standings = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Computed
    const activeCompetitions = computed(() =>
        competitions.value.filter(c => c.is_active)
    )

    const competitionsByType = computed(() => {
        const grouped = {}
        competitions.value.forEach(c => {
            const type = c.competition_type || 'other'
            if (!grouped[type]) grouped[type] = []
            grouped[type].push(c)
        })
        return grouped
    })

    const competitionsByCountry = computed(() => {
        const grouped = {}
        competitions.value.forEach(c => {
            const country = c.country || 'Unknown'
            if (!grouped[country]) grouped[country] = []
            grouped[country].push(c)
        })
        return grouped
    })

    const liveCompetitions = computed(() =>
        competitions.value.filter(c =>
            c.current_season?.status === 'live'
        )
    )

    // Actions
    async function fetchCompetitions(params = {}) {
        loading.value = true
        error.value = null
        try {
            const response = await axios.get('/api/v1/competitions/competitions/', { params })
            const data = response.data
            competitions.value = data.results || data
            return competitions.value
        } catch (err) {
            error.value = err.message
            console.error('Failed to fetch competitions:', err)
            return []
        } finally {
            loading.value = false
        }
    }

    async function fetchCompetition(id) {
        loading.value = true
        error.value = null
        try {
            const response = await axios.get(`/api/v1/competitions/competitions/${id}/`)
            currentCompetition.value = response.data
            return response.data
        } catch (err) {
            error.value = err.message
            console.error('Failed to fetch competition:', err)
            return null
        } finally {
            loading.value = false
        }
    }

    async function fetchStandings(competitionId) {
        try {
            const response = await axios.get(
                `/api/v1/competitions/competitions/${competitionId}/standings/`
            )
            standings.value = response.data || []
            return standings.value
        } catch (err) {
            console.error('Failed to fetch standings:', err)
            return []
        }
    }

    async function fetchSeasons(competitionId) {
        try {
            const response = await axios.get(
                `/api/v1/competitions/competitions/${competitionId}/seasons/`
            )
            return response.data.results || response.data || []
        } catch (err) {
            console.error('Failed to fetch seasons:', err)
            return []
        }
    }

    function clearCurrentCompetition() {
        currentCompetition.value = null
        standings.value = []
    }

    return {
        competitions,
        currentCompetition,
        standings,
        loading,
        error,
        activeCompetitions,
        competitionsByType,
        competitionsByCountry,
        liveCompetitions,
        fetchCompetitions,
        fetchCompetition,
        fetchStandings,
        fetchSeasons,
        clearCurrentCompetition,
    }
})