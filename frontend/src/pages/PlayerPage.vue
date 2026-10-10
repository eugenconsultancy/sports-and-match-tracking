<template>
  <div class="max-w-7xl mx-auto px-4 py-6">
    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full"></div>
    </div>

    <div v-else-if="player" class="space-y-6">
      <!-- Player Header -->
      <div class="card">
        <div class="flex flex-col sm:flex-row items-center gap-6">
          <img v-if="player.image_url"
               :src="player.image_url"
               :alt="player.full_name"
               class="w-28 h-28 rounded-full object-cover border-4 border-gray-200" />
          <div v-else
               class="w-28 h-28 rounded-full bg-primary-100 flex items-center justify-center text-4xl font-bold text-primary-600 border-4 border-gray-200">
            {{ player.full_name?.charAt(0) }}
          </div>
          <div class="flex-1 text-center sm:text-left">
            <div class="flex items-center justify-center sm:justify-start gap-3">
              <h1 class="text-3xl font-bold">{{ player.full_name }}</h1>
              <span class="text-2xl">{{ nationalityFlag }}</span>
            </div>
            <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2 mt-2">
              <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                {{ player.position }}
              </span>
              <span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                {{ player.preferred_foot }} foot
              </span>
              <span v-if="player.jersey_number" class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                #{{ player.jersey_number }}
              </span>
            </div>
            <div class="flex items-center justify-center sm:justify-start gap-4 mt-3">
              <div v-if="player.current_team_name" class="flex items-center gap-2">
                <img v-if="player.current_team_logo" :src="player.current_team_logo" class="w-6 h-6 object-contain" />
                <span class="text-sm text-gray-600">{{ player.current_team_name }}</span>
              </div>
              <span v-if="player.market_value" class="text-lg font-bold text-green-600">
                {{ player.market_value_currency }} {{ formatNumber(player.market_value) }}
              </span>
            </div>
            <div class="flex items-center justify-center sm:justify-start gap-4 mt-2 text-sm text-gray-500">
              <span v-if="player.date_of_birth">Born: {{ formatDate(player.date_of_birth) }}</span>
              <span v-if="player.height_cm">{{ player.height_cm }} cm</span>
              <span v-if="player.weight_kg">{{ player.weight_kg }} kg</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Grid -->
      <div v-if="stats" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Season Stats -->
        <div class="card">
          <h3 class="text-lg font-bold mb-4">Season Stats</h3>
          <div v-if="stats.season_stats?.length">
            <div v-for="stat in stats.season_stats" :key="stat.id" class="mb-4">
              <p class="text-sm text-gray-500 mb-2">{{ stat.season_name }} · {{ stat.team_name }}</p>
              <div class="grid grid-cols-3 gap-3">
                <div class="text-center bg-gray-50 rounded-lg p-2">
                  <p class="text-xl font-bold">{{ stat.appearances }}</p>
                  <p class="text-xs text-gray-500">Apps</p>
                </div>
                <div class="text-center bg-gray-50 rounded-lg p-2">
                  <p class="text-xl font-bold text-green-600">{{ stat.goals }}</p>
                  <p class="text-xs text-gray-500">Goals</p>
                </div>
                <div class="text-center bg-gray-50 rounded-lg p-2">
                  <p class="text-xl font-bold text-blue-600">{{ stat.assists }}</p>
                  <p class="text-xs text-gray-500">Assists</p>
                </div>
                <div class="text-center bg-gray-50 rounded-lg p-2">
                  <p class="text-xl font-bold">{{ stat.minutes_played }}</p>
                  <p class="text-xs text-gray-500">Mins</p>
                </div>
                <div class="text-center bg-gray-50 rounded-lg p-2">
                  <p class="text-xl font-bold text-yellow-600">{{ stat.yellow_cards }}</p>
                  <p class="text-xs text-gray-500">Yellow</p>
                </div>
                <div class="text-center bg-gray-50 rounded-lg p-2">
                  <p class="text-xl font-bold text-red-600">{{ stat.red_cards }}</p>
                  <p class="text-xs text-gray-500">Red</p>
                </div>
              </div>
              <div v-if="stat.average_rating" class="mt-2 text-center">
                <span class="text-sm font-medium">Avg Rating:</span>
                <span class="text-lg font-bold text-primary-600 ml-1">{{ stat.average_rating }}</span>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-4 text-gray-500">No season stats available</div>
        </div>

        <!-- Recent Matches -->
        <div class="card">
          <h3 class="text-lg font-bold mb-4">Recent Matches</h3>
          <div v-if="stats.recent_matches?.length" class="space-y-2 max-h-96 overflow-y-auto">
            <div v-for="matchStat in stats.recent_matches" :key="matchStat.id"
                 class="flex items-center justify-between p-2 rounded hover:bg-gray-50">
              <div>
                <p class="text-sm font-medium">{{ matchStat.match_info?.home_team }} vs {{ matchStat.match_info?.away_team }}</p>
                <p class="text-xs text-gray-500">{{ formatDate(matchStat.match_info?.kickoff_time) }}</p>
              </div>
              <div class="flex items-center gap-3">
                <span v-if="matchStat.rating" class="text-sm font-bold text-primary-600">{{ matchStat.rating }}</span>
                <span v-if="matchStat.goals" class="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full">
                  ⚽ {{ matchStat.goals }}
                </span>
                <span v-if="matchStat.assists" class="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">
                  🅰 {{ matchStat.assists }}
                </span>
                <span v-if="matchStat.yellow_card" class="text-xs bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded-full">🟨</span>
                <span v-if="matchStat.red_card" class="text-xs bg-red-100 text-red-800 px-2 py-0.5 rounded-full">🟥</span>
                <span v-if="matchStat.is_mvp" class="text-xs bg-purple-100 text-purple-800 px-2 py-0.5 rounded-full">⭐</span>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-4 text-gray-500">No recent matches</div>
        </div>
      </div>

      <!-- Transfers -->
      <div v-if="stats.transfers?.length" class="card">
        <h3 class="text-lg font-bold mb-4">Transfer History</h3>
        <div class="space-y-3">
          <div v-for="transfer in stats.transfers" :key="transfer.id"
               class="flex items-center justify-between p-3 rounded-lg border border-gray-100">
            <div class="flex items-center gap-4">
              <span class="text-sm font-medium">{{ transfer.from_team_name || 'Youth' }}</span>
              <span class="text-gray-400">→</span>
              <span class="text-sm font-medium text-primary-600">{{ transfer.to_team_name }}</span>
            </div>
            <div class="text-right">
              <p class="text-sm">{{ formatDate(transfer.transfer_date) }}</p>
              <p v-if="transfer.transfer_fee" class="text-xs text-gray-500">
                {{ transfer.transfer_fee_currency }} {{ formatNumber(transfer.transfer_fee) }}
              </p>
              <p v-else-if="transfer.is_loan" class="text-xs text-blue-600">Loan</p>
              <p v-else class="text-xs text-gray-400">Free</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Not Found -->
    <div v-else class="card text-center py-16">
      <div class="text-6xl mb-4">👤</div>
      <h3 class="text-xl font-semibold text-gray-700 mb-2">Player Not Found</h3>
      <router-link to="/" class="btn-primary inline-block mt-4">Go Home</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axios'
import { formatDate, formatNumber } from '@/utils/formatters'

const route = useRoute()
const playerId = route.params.id

const loading = ref(true)
const player = ref(null)
const stats = ref(null)

const nationalityFlag = ref('🏳️')

onMounted(async () => {
  try {
    const [playerRes, statsRes] = await Promise.all([
      axios.get(`/api/v1/players/players/${playerId}/`),
      axios.get(`/api/v1/players/players/${playerId}/stats/`),
    ])

    player.value = playerRes.data
    stats.value = statsRes.data

    // Simple country to flag mapping (production would use a proper library)
    const country = player.value?.nationality
    if (country) {
      const flags = {
        England: '🏴󠁧󠁢󠁥󠁮󠁧󠁿', Spain: '🇪🇸', France: '🇫🇷', Germany: '🇩🇪',
        Italy: '🇮🇹', Portugal: '🇵🇹', Netherlands: '🇳🇱', Belgium: '🇧🇪',
        Brazil: '🇧🇷', Argentina: '🇦🇷', Norway: '🇳🇴', Egypt: '🇪🇬',
      }
      nationalityFlag.value = flags[country] || '🏳️'
    }
  } catch (error) {
    console.error('Failed to load player:', error)
  } finally {
    loading.value = false
  }
})
</script>