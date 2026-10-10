<template>
  <div v-if="loading" class="flex justify-center py-12">
    <Loader size="lg" />
  </div>

  <div v-else-if="team" class="space-y-6">
    <!-- Team Header -->
    <div class="card p-6">
      <div class="flex flex-col md:flex-row items-center gap-6">
        <img v-if="team.logo_url" :src="team.logo_url" :alt="team.name" class="w-28 h-28 object-contain" />
        <div class="flex-1 text-center md:text-left">
          <h1 class="text-3xl font-bold">{{ team.name }}</h1>
          <div class="flex flex-wrap items-center justify-center md:justify-start gap-3 mt-2">
            <Badge variant="default">{{ team.country }}</Badge>
            <Badge :variant="team.team_type === 'club' ? 'info' : 'success'">{{ team.team_type }}</Badge>
            <span class="text-sm text-gray-500">Founded {{ team.founded_year }}</span>
          </div>
          <div class="mt-3 flex flex-wrap gap-4 text-sm">
            <span>🏟️ Stadium: {{ team.venue?.name || 'N/A' }}</span>
            <span>👥 Squad: {{ team.squad_size || 0 }} players</span>
          </div>
        </div>
        <button @click="toggleFavorite" class="p-3 rounded-full transition-colors"
                :class="isFavorited ? 'bg-red-50 text-red-600' : 'bg-gray-100 text-gray-400 hover:text-red-500'">
          <svg class="w-6 h-6" :fill="isFavorited ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Season Stats Overview -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="card text-center p-4">
        <p class="text-2xl font-bold text-primary-600">{{ seasonStats.matches_played }}</p>
        <p class="text-xs text-gray-500">Matches</p>
      </div>
      <div class="card text-center p-4">
        <p class="text-2xl font-bold text-green-600">{{ seasonStats.wins }}</p>
        <p class="text-xs text-gray-500">Wins</p>
      </div>
      <div class="card text-center p-4">
        <p class="text-2xl font-bold text-yellow-600">{{ seasonStats.draws }}</p>
        <p class="text-xs text-gray-500">Draws</p>
      </div>
      <div class="card text-center p-4">
        <p class="text-2xl font-bold text-red-600">{{ seasonStats.losses }}</p>
        <p class="text-xs text-gray-500">Losses</p>
      </div>
    </div>

    <!-- Tabs -->
    <Tabs :tabs="tabs" v-model="activeTab">
      <template #default="{ activeTab: tab }">
        <!-- Squad Tab -->
        <div v-if="tab === 'squad'" class="space-y-4">
          <div v-for="position in positions" :key="position.key" class="card overflow-hidden">
            <div class="p-3 bg-gray-50 border-b border-gray-100">
              <h3 class="font-semibold">{{ position.label }}</h3>
            </div>
            <div class="divide-y divide-gray-100">
              <div v-for="player in getPlayersByPosition(position.key)" :key="player.id"
                   class="flex items-center justify-between p-3 hover:bg-gray-50 cursor-pointer"
                   @click="$router.push(`/player/${player.id}`)">
                <div class="flex items-center gap-3">
                  <img v-if="player.image_url" :src="player.image_url" class="w-10 h-10 rounded-full object-cover" />
                  <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center text-primary-600 font-bold" v-else>
                    {{ player.full_name?.charAt(0) }}
                  </div>
                  <div>
                    <p class="font-medium">{{ player.full_name }}</p>
                    <p class="text-xs text-gray-500">#{{ player.jersey_number }} • {{ player.nationality }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <p class="text-sm font-semibold text-green-600">{{ formatNumber(player.market_value) }}M</p>
                  <p class="text-xs text-gray-400">{{ player.position }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Matches Tab -->
        <div v-if="tab === 'matches'" class="space-y-8">
          <div>
            <h3 class="text-lg font-bold mb-3">Upcoming Matches</h3>
            <div v-if="matches.upcoming?.length" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <MatchWidget v-for="match in matches.upcoming" :key="match.id" :match="match" />
            </div>
            <div v-else class="card text-center py-4 text-gray-500">No upcoming matches</div>
          </div>
          <div>
            <h3 class="text-lg font-bold mb-3">Recent Results</h3>
            <div v-if="matches.recent?.length" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <MatchWidget v-for="match in matches.recent" :key="match.id" :match="match" />
            </div>
            <div v-else class="card text-center py-4 text-gray-500">No recent matches</div>
          </div>
        </div>

        <!-- Stats Tab -->
        <div v-if="tab === 'stats'" class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="card p-4">
            <h3 class="font-bold mb-3">Top Scorers</h3>
            <div class="space-y-2">
              <div v-for="(player, idx) in topScorers" :key="player.player_id"
                   class="flex items-center justify-between p-2 rounded hover:bg-gray-50 cursor-pointer"
                   @click="$router.push(`/player/${player.player_id}`)">
                <div class="flex items-center gap-2">
                  <span class="w-6 text-primary-600 font-bold">{{ idx + 1 }}</span>
                  <span>{{ player.player_name }}</span>
                </div>
                <span class="font-bold text-green-600">{{ player.goals }}</span>
              </div>
            </div>
          </div>
          <div class="card p-4">
            <h3 class="font-bold mb-3">Top Assisters</h3>
            <div class="space-y-2">
              <div v-for="(player, idx) in topAssisters" :key="player.player_id"
                   class="flex items-center justify-between p-2 rounded hover:bg-gray-50 cursor-pointer"
                   @click="$router.push(`/player/${player.player_id}`)">
                <div class="flex items-center gap-2">
                  <span class="w-6 text-primary-600 font-bold">{{ idx + 1 }}</span>
                  <span>{{ player.player_name }}</span>
                </div>
                <span class="font-bold text-blue-600">{{ player.assists }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Transfers Tab -->
        <div v-if="tab === 'transfers'" class="space-y-3">
          <div v-for="transfer in transfers" :key="transfer.id" class="card p-4">
            <div class="flex items-center justify-between flex-wrap gap-3">
              <div class="flex items-center gap-4">
                <div class="text-right">
                  <p class="font-medium">{{ transfer.player_name }}</p>
                  <p class="text-xs text-gray-500">{{ transfer.from_team_name || 'Free Agent' }}</p>
                </div>
                <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
                <div>
                  <p class="font-medium text-primary-600">{{ transfer.to_team_name }}</p>
                  <p class="text-xs text-gray-500">{{ formatDate(transfer.transfer_date) }}</p>
                </div>
              </div>
              <div>
                <Badge v-if="transfer.is_loan" variant="warning">Loan</Badge>
                <Badge v-else-if="transfer.transfer_fee" variant="success">
                  {{ transfer.transfer_fee_currency }} {{ formatCompactNumber(transfer.transfer_fee) }}
                </Badge>
                <Badge v-else variant="default">Free Transfer</Badge>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Tabs>
  </div>

  <div v-else class="card text-center py-16">
    <div class="text-6xl mb-4">⚽</div>
    <h3 class="text-xl font-semibold text-gray-700 mb-2">Team Not Found</h3>
    <router-link to="/competitions" class="btn-primary inline-block mt-4">Browse Teams</router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '@/services/api'
import { formatDate, formatNumber, formatCompactNumber } from '@/utils/formatters'
import Loader from '@/components/ui/Loader.vue'
import Badge from '@/components/ui/Badge.vue'
import Tabs from '@/components/ui/Tabs.vue'
import MatchWidget from '@/components/MatchWidget.vue'

const route = useRoute()
const teamId = route.params.id

const loading = ref(true)
const team = ref(null)
const players = ref([])
const matches = ref({ upcoming: [], recent: [] })
const transfers = ref([])
const isFavorited = ref(false)
const activeTab = ref('squad')
const topScorers = ref([])
const topAssisters = ref([])

const positions = [
  { key: 'GK', label: 'Goalkeepers' },
  { key: 'CB', label: 'Defenders' },
  { key: 'LB', label: 'Left Backs' },
  { key: 'RB', label: 'Right Backs' },
  { key: 'DM', label: 'Defensive Midfielders' },
  { key: 'CM', label: 'Central Midfielders' },
  { key: 'AM', label: 'Attacking Midfielders' },
  { key: 'LW', label: 'Left Wingers' },
  { key: 'RW', label: 'Right Wingers' },
  { key: 'CF', label: 'Forwards' },
  { key: 'ST', label: 'Strikers' },
]

const tabs = [
  { id: 'squad', label: 'Squad' },
  { id: 'matches', label: 'Matches' },
  { id: 'stats', label: 'Stats' },
  { id: 'transfers', label: 'Transfers' },
]

const seasonStats = computed(() => {
  if (!matches.value.recent?.length) return { matches_played: 0, wins: 0, draws: 0, losses: 0 }
  
  const finished = matches.value.recent.filter(m => m.status === 'finished')
  const wins = finished.filter(m => 
    (m.home_team === teamId && m.home_score > m.away_score) ||
    (m.away_team === teamId && m.away_score > m.home_score)
  ).length
  const draws = finished.filter(m => m.home_score === m.away_score).length
  const losses = finished.length - wins - draws
  
  return {
    matches_played: finished.length,
    wins,
    draws,
    losses,
  }
})

function getPlayersByPosition(position) {
  if (position === 'GK') return players.value.filter(p => p.position === 'GK')
  if (['CB', 'LB', 'RB'].includes(position)) return players.value.filter(p => p.position === position)
  if (['DM', 'CM', 'AM'].includes(position)) return players.value.filter(p => p.position === position)
  if (['LW', 'RW', 'CF', 'ST'].includes(position)) return players.value.filter(p => p.position === position)
  return []
}

function toggleFavorite() {
  isFavorited.value = !isFavorited.value
}

async function loadTeam() {
  try {
    const [teamRes, playersRes, matchesRes, transfersRes] = await Promise.all([
      api.getTeam(teamId),
      api.getTeamPlayers(teamId),
      api.getTeamMatches(teamId),
      api.getTeamTransfers?.(teamId) || Promise.resolve({ results: [] }),
    ])
    
    team.value = teamRes
    players.value = playersRes.results || playersRes || []
    matches.value = matchesRes || { upcoming: [], recent: [] }
    transfers.value = transfersRes.results || transfersRes || []
    
    // Calculate top scorers from players
    topScorers.value = players.value
      .map(p => ({ player_id: p.id, player_name: p.full_name, goals: p.stats?.goals || 0 }))
      .sort((a, b) => b.goals - a.goals)
      .slice(0, 10)
    
    topAssisters.value = players.value
      .map(p => ({ player_id: p.id, player_name: p.full_name, assists: p.stats?.assists || 0 }))
      .sort((a, b) => b.assists - a.assists)
      .slice(0, 10)
  } catch (error) {
    console.error('Failed to load team:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadTeam()
})
</script>