<template>
  <Modal :is-open="true" @close="$emit('close')" :close-on-backdrop="true">
    <div class="space-y-4">
      <div class="relative">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          v-model="query"
          type="text"
          placeholder="Search teams, players, competitions..."
          class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          autofocus
          @keyup.enter="search"
        />
      </div>
      
      <div v-if="loading" class="text-center py-8">
        <Loader size="sm" />
      </div>
      
      <div v-else-if="results">
        <div v-if="results.teams?.length" class="mb-4">
          <h4 class="text-sm font-semibold text-gray-500 mb-2">Teams</h4>
          <div class="space-y-2">
            <div v-for="team in results.teams.slice(0, 5)" :key="team.id"
                 class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                 @click="navigateTo(`/team/${team.id}`)">
              <img v-if="team.logo_url" :src="team.logo_url" class="w-8 h-8 object-contain" />
              <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center text-sm font-bold" v-else>
                {{ team.name?.charAt(0) }}
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ team.name }}</p>
                <p class="text-xs text-gray-500">{{ team.country }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="results.players?.length" class="mb-4">
          <h4 class="text-sm font-semibold text-gray-500 mb-2">Players</h4>
          <div class="space-y-2">
            <div v-for="player in results.players.slice(0, 5)" :key="player.id"
                 class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                 @click="navigateTo(`/player/${player.id}`)">
              <img v-if="player.image_url" :src="player.image_url" class="w-8 h-8 rounded-full object-cover" />
              <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center text-sm font-bold text-primary-600" v-else>
                {{ player.full_name?.charAt(0) }}
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ player.full_name }}</p>
                <p class="text-xs text-gray-500">{{ player.position }} • {{ player.current_team_name }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="results.competitions?.length" class="mb-4">
          <h4 class="text-sm font-semibold text-gray-500 mb-2">Competitions</h4>
          <div class="space-y-2">
            <div v-for="comp in results.competitions.slice(0, 5)" :key="comp.id"
                 class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                 @click="navigateTo(`/competition/${comp.id}`)">
              <img v-if="comp.logo_url" :src="comp.logo_url" class="w-8 h-8 object-contain" />
              <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center text-sm font-bold" v-else>
                {{ comp.name?.charAt(0) }}
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ comp.name }}</p>
                <p class="text-xs text-gray-500">{{ comp.country }} • {{ comp.competition_type }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Modal>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axios'
import Modal from '@/components/ui/Modal.vue'
import Loader from '@/components/ui/Loader.vue'

const emit = defineEmits(['close'])
const router = useRouter()

const query = ref('')
const loading = ref(false)
const results = ref({ teams: [], players: [], competitions: [] })

let searchTimeout = null

watch(query, () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    if (query.value.length >= 2) {
      performSearch()
    } else if (query.value.length === 0) {
      results.value = { teams: [], players: [], competitions: [] }
    }
  }, 400)
})

async function performSearch() {
  if (!query.value.trim()) return
  
  loading.value = true
  try {
    const [teamsRes, playersRes, compsRes] = await Promise.all([
      axios.get('/api/v1/teams/teams/', { params: { search: query.value, limit: 10 } }),
      axios.get('/api/v1/players/players/', { params: { search: query.value, limit: 10 } }),
      axios.get('/api/v1/competitions/competitions/', { params: { search: query.value, limit: 10 } }),
    ])
    
    results.value = {
      teams: teamsRes.data.results || teamsRes.data || [],
      players: playersRes.data.results || playersRes.data || [],
      competitions: compsRes.data.results || compsRes.data || [],
    }
  } catch (error) {
    console.error('Search failed:', error)
  } finally {
    loading.value = false
  }
}

function navigateTo(path) {
  router.push(path)
  emit('close')
}
</script>