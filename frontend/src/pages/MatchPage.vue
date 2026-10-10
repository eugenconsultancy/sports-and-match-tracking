<template>
  <div v-if="loading" class="flex justify-center py-12">
    <Loader size="lg" />
  </div>

  <div v-else-if="match" class="space-y-6">
    <!-- Match Header -->
    <div class="card p-6">
      <div class="text-center mb-6">
        <div class="flex items-center justify-center gap-2 mb-2">
          <Badge :variant="getStatusVariant(match.status)">
            {{ getMatchStatusLabel(match.status) }}
          </Badge>
          <span class="text-sm text-gray-500">{{ match.competition?.name }}</span>
        </div>
        
        <div class="flex flex-col md:flex-row items-center justify-center gap-8">
          <!-- Home Team -->
          <div class="text-center flex-1">
            <img v-if="match.home_team?.logo_url" :src="match.home_team.logo_url" class="w-20 h-20 mx-auto object-contain" />
            <h2 class="text-xl font-bold mt-3">{{ match.home_team?.name }}</h2>
          </div>
          
          <!-- Score -->
          <div class="text-center">
            <div class="text-5xl font-bold tabular-nums" :class="{ 'text-red-600': isLive }">
              {{ match.home_score }} - {{ match.away_score }}
            </div>
            <div v-if="match.home_score_halftime !== null" class="text-sm text-gray-400 mt-1">
              HT: {{ match.home_score_halftime }} - {{ match.away_score_halftime }}
            </div>
            <div v-if="isLive && match.minute" class="live-badge mt-2">LIVE {{ match.minute }}'</div>
            <div v-else-if="match.kickoff_time" class="text-sm text-gray-500 mt-2">
              {{ formatKickoffTime(match.kickoff_time) }}
            </div>
          </div>
          
          <!-- Away Team -->
          <div class="text-center flex-1">
            <img v-if="match.away_team?.logo_url" :src="match.away_team.logo_url" class="w-20 h-20 mx-auto object-contain" />
            <h2 class="text-xl font-bold mt-3">{{ match.away_team?.name }}</h2>
          </div>
        </div>
        
        <div class="flex items-center justify-center gap-4 mt-4 text-sm text-gray-500">
          <span v-if="match.venue?.name">🏟️ {{ match.venue.name }}</span>
          <span v-if="match.referee_name">👨‍⚖️ {{ match.referee_name }}</span>
          <span v-if="match.attendance">👥 {{ match.attendance.toLocaleString() }}</span>
        </div>
      </div>
    </div>

    <!-- Match Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left Column: Events & Lineups -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Live Stats Bar -->
        <div v-if="match.live_state" class="card p-4">
          <div class="flex items-center gap-4">
            <div class="flex-1">
              <div class="flex justify-between text-sm mb-1">
                <span>{{ match.home_team?.name }}</span>
                <span>{{ match.away_team?.name }}</span>
              </div>
              <div class="stat-bar h-3">
                <div class="stat-bar-fill" :style="{ width: `${match.live_state.possession?.home || 50}%` }"></div>
              </div>
              <div class="flex justify-between text-xs text-gray-500 mt-1">
                <span>{{ match.live_state.possession?.home || 50 }}%</span>
                <span>{{ match.live_state.possession?.away || 50 }}%</span>
              </div>
            </div>
            <div class="text-center">
              <div class="text-sm text-gray-500 mb-1">Momentum</div>
              <Badge :variant="getMomentumVariant(match.live_state.momentum)">
                {{ getMomentumLabel(match.live_state.momentum) }}
              </Badge>
            </div>
          </div>
        </div>

        <!-- Match Events Timeline -->
        <div class="card p-4">
          <h3 class="font-bold mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Match Timeline
          </h3>
          <div class="space-y-2 max-h-96 overflow-y-auto">
            <div v-for="event in match.events" :key="event.id"
                 class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50">
              <span class="text-sm font-mono w-12 font-bold">{{ event.minute }}'</span>
              <div class="text-2xl">{{ getEventIcon(event.event_type) }}</div>
              <div class="flex-1">
                <span class="font-medium">{{ event.player_name }}</span>
                <span class="text-sm text-gray-500 ml-2">{{ event.team_name }}</span>
                <div v-if="event.description" class="text-xs text-gray-400">{{ event.description }}</div>
              </div>
              <div v-if="event.score_home !== null" class="text-sm font-mono text-gray-500">
                {{ event.score_home }} - {{ event.score_away }}
              </div>
            </div>
            <div v-if="!match.events?.length" class="text-center py-4 text-gray-500">
              No events yet
            </div>
          </div>
        </div>

        <!-- Lineups -->
        <div class="card p-4">
          <h3 class="font-bold mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Lineups
          </h3>
          <div class="grid grid-cols-2 gap-6">
            <div>
              <h4 class="font-semibold text-primary-600 mb-2">{{ match.home_team?.name }}</h4>
              <div class="space-y-1">
                <div v-for="player in getLineups('home')" :key="player.id"
                     class="flex items-center justify-between text-sm">
                  <div class="flex items-center gap-2">
                    <span class="text-xs text-gray-400 w-6">{{ player.jersey_number }}</span>
                    <span>{{ player.player_name }}</span>
                    <span v-if="player.is_captain" class="text-xs text-yellow-500">(C)</span>
                  </div>
                  <span class="text-xs text-gray-400">{{ player.position }}</span>
                </div>
              </div>
            </div>
            <div>
              <h4 class="font-semibold text-primary-600 mb-2">{{ match.away_team?.name }}</h4>
              <div class="space-y-1">
                <div v-for="player in getLineups('away')" :key="player.id"
                     class="flex items-center justify-between text-sm">
                  <div class="flex items-center gap-2">
                    <span class="text-xs text-gray-400 w-6">{{ player.jersey_number }}</span>
                    <span>{{ player.player_name }}</span>
                    <span v-if="player.is_captain" class="text-xs text-yellow-500">(C)</span>
                  </div>
                  <span class="text-xs text-gray-400">{{ player.position }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Stats & Poll -->
      <div class="space-y-6">
        <!-- Poll Widget -->
        <PollWidget v-if="match.has_poll" :poll-id="match.id" :match-id="match.id" />

        <!-- Match Statistics -->
        <div v-if="match.stats?.length" class="card p-4">
          <h3 class="font-bold mb-4">Match Statistics</h3>
          <div class="space-y-4">
            <div v-for="stat in match.stats" :key="stat.team" class="border-b border-gray-100 pb-3 last:border-0">
              <h4 class="font-medium text-sm mb-2">{{ stat.team_name }}</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-600">Possession</span>
                  <span class="font-medium">{{ stat.possession_percentage }}%</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Shots (On Target)</span>
                  <span>{{ stat.shots_total }} ({{ stat.shots_on_target }})</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Pass Accuracy</span>
                  <span>{{ stat.pass_accuracy }}%</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Fouls</span>
                  <span>{{ stat.fouls }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Yellow/Red Cards</span>
                  <span>{{ stat.yellow_cards }} / {{ stat.red_cards }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Expected Goals (xG)</span>
                  <span>{{ stat.expected_goals_xg || '-' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="card text-center py-16">
    <div class="text-6xl mb-4">⚽</div>
    <h3 class="text-xl font-semibold text-gray-700 mb-2">Match Not Found</h3>
    <router-link to="/live" class="btn-primary inline-block mt-4">View Live Matches</router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useMatchStore } from '@/stores/matches'
import { useMatchWebSocket } from '@/composables/useWebSocket'
import { getMatchStatusLabel, getEventIcon, formatKickoffTime } from '@/utils/formatters'
import Loader from '@/components/ui/Loader.vue'
import Badge from '@/components/ui/Badge.vue'
import PollWidget from '@/components/PollWidget.vue'

const route = useRoute()
const matchStore = useMatchStore()

const loading = ref(true)
const match = ref(null)

const isLive = computed(() => match.value?.status === 'live' || match.value?.status === 'half_time')

function getStatusVariant(status) {
  const variants = {
    scheduled: 'default',
    live: 'error',
    half_time: 'warning',
    finished: 'success',
    postponed: 'warning',
  }
  return variants[status] || 'default'
}

function getMomentumVariant(momentum) {
  const variants = { home: 'error', away: 'info', balanced: 'default' }
  return variants[momentum] || 'default'
}

function getMomentumLabel(momentum) {
  const labels = { home: 'Home Dominant', away: 'Away Dominant', balanced: 'Balanced' }
  return labels[momentum] || 'Balanced'
}

function getLineups(teamSide) {
  if (!match.value?.lineups) return []
  const teamId = teamSide === 'home' ? match.value.home_team?.id : match.value.away_team?.id
  return match.value.lineups.filter(l => l.team === teamId && l.role === 'starter').sort((a, b) => a.sort_order - b.sort_order)
}

// WebSocket for real-time updates
const { isConnected, lastMessage } = useMatchWebSocket(
  route.params.id,
  (data) => {
    match.value = { ...match.value, ...data }
  },
  (event) => {
    match.value.events = [...(match.value.events || []), event]
  }
)

onMounted(async () => {
  try {
    match.value = await matchStore.fetchMatchDetail(route.params.id)
  } catch (error) {
    console.error('Failed to load match:', error)
  } finally {
    loading.value = false
  }
})
</script>