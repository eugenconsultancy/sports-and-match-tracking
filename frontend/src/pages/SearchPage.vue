<template>
  <div class="space-y-6">
    <h1 class="text-3xl font-bold">Search</h1>

    <div class="card">
      <div class="relative">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          v-model="query"
          type="text"
          placeholder="Search teams, players, competitions..."
          class="w-full pl-10 pr-4 py-3 text-lg border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          @keyup.enter="performSearch"
        />
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-12">
      <Loader size="lg" />
    </div>

    <div v-else-if="hasSearched && !hasResults" class="card text-center py-16">
      <div class="text-6xl mb-4">🔍</div>
      <h3 class="text-xl font-semibold text-gray-700 mb-2">No results found</h3>
      <p class="text-gray-500">We couldn't find any matches for "{{ query }}"</p>
      <button @click="clearSearch" class="btn-primary mt-4">Clear Search</button>
    </div>

    <div v-else-if="hasResults" class="space-y-8">
      <!-- Teams -->
      <section v-if="results.teams?.length">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold">Teams</h2>
          <button v-if="results.teams.length > 6" @click="showAllTeams = !showAllTeams" class="text-sm text-primary-600 hover:underline">
            {{ showAllTeams ? 'Show less' : 'Show all' }}
          </button>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          <TeamCard v-for="team in displayedTeams" :key="team.id" :team="team" @click="goToTeam(team.id)" />
        </div>
      </section>

      <!-- Players -->
      <section v-if="results.players?.length">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold">Players</h2>
          <button v-if="results.players.length > 6" @click="showAllPlayers = !showAllPlayers" class="text-sm text-primary-600 hover:underline">
            {{ showAllPlayers ? 'Show less' : 'Show all' }}
          </button>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <PlayerStatsCard v-for="player in displayedPlayers" :key="player.id" :player="player" />
        </div>
      </section>

      <!-- Competitions -->
      <section v-if="results.competitions?.length">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold">Competitions</h2>
          <button v-if="results.competitions.length > 6" @click="showAllComps = !showAllComps" class="text-sm text-primary-600 hover:underline">
            {{ showAllComps ? 'Show less' : 'Show all' }}
          </button>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          <CompetitionCard v-for="comp in displayedComps" :key="comp.id" :competition="comp" @click="goToCompetition(comp.id)" />
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '@/services/api'
import Loader from '@/components/ui/Loader.vue'
import TeamCard from '@/components/TeamCard.vue'
import PlayerStatsCard from '@/components/PlayerStatsCard.vue'
import CompetitionCard from '@/components/CompetitionCard.vue'

const route = useRoute()
const router = useRouter()

const query = ref('')
const loading = ref(false)
const hasSearched = ref(false)
const results = ref({ teams: [], players: [], competitions: [] })
const showAllTeams = ref(false)
const showAllPlayers = ref(false)
const showAllComps = ref(false)

const hasResults = computed(() => {
  return results.value.teams?.length > 0 || 
         results.value.players?.length > 0 || 
         results.value.competitions?.length > 0
})

const displayedTeams = computed(() => {
  if (showAllTeams.value) return results.value.teams
  return results.value.teams?.slice(0, 6) || []
})

const displayedPlayers = computed(() => {
  if (showAllPlayers.value) return results.value.players
  return results.value.players?.slice(0, 6) || []
})

const displayedComps = computed(() => {
  if (showAllComps.value) return results.value.competitions
  return results.value.competitions?.slice(0, 6) || []
})

async function performSearch() {
  if (!query.value.trim()) return
  
  loading.value = true
  hasSearched.value = true
  
  try {
    results.value = await api.search(query.value)
  } catch (error) {
    console.error('Search failed:', error)
  } finally {
    loading.value = false
  }
}

function clearSearch() {
  query.value = ''
  results.value = { teams: [], players: [], competitions: [] }
  hasSearched.value = false
}

function goToTeam(id) {
  router.push(`/team/${id}`)
}

function goToCompetition(id) {
  router.push(`/competition/${id}`)
}

onMounted(() => {
  const searchQuery = route.query.q
  if (searchQuery) {
    query.value = searchQuery
    performSearch()
  }
})
</script>