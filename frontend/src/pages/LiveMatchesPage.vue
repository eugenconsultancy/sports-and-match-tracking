<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto px-4 py-8 space-y-8">
      <!-- Enhanced Hero Header -->
      <div class="relative overflow-hidden bg-gradient-to-br from-red-600 via-red-700 to-red-900 rounded-2xl p-8 text-white shadow-xl">
        <!-- Background Pattern -->
        <div class="absolute inset-0 opacity-10">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(255,255,255,0.3),rgba(255,255,255,0))]"></div>
          <div class="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-yellow-500/20 to-transparent rounded-full blur-3xl"></div>
          <div class="absolute bottom-0 left-0 w-64 h-64 bg-gradient-to-tr from-orange-500/20 to-transparent rounded-full blur-3xl"></div>
        </div>

        <div class="relative z-10">
          <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            <div>
              <div class="flex items-center gap-3 mb-2">
                <span class="relative flex h-4 w-4">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-4 w-4 bg-green-400"></span>
                </span>
                <h1 class="text-3xl sm:text-4xl font-bold tracking-tight">Live Matches</h1>
              </div>
              <p class="text-white/70 text-lg ml-7">
                {{ liveMatches.length > 0 
                  ? `${liveMatches.length} match${liveMatches.length !== 1 ? 'es' : ''} in progress` 
                  : 'No live matches at the moment'
                }}
              </p>
            </div>

            <!-- Controls -->
            <div class="flex flex-col sm:flex-row gap-3">
              <!-- Source Selector -->
              <div class="flex bg-white/10 backdrop-blur rounded-xl p-1 gap-1">
                <button v-for="source in sources" :key="source.value"
                        @click="selectedSource = source.value"
                        class="px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300 flex items-center gap-2"
                        :class="selectedSource === source.value 
                          ? 'bg-white text-red-700 shadow-lg' 
                          : 'text-white/80 hover:text-white hover:bg-white/10'">
                  <span>{{ source.icon }}</span>
                  {{ source.label }}
                </button>
              </div>

              <!-- Refresh Button -->
              <button @click="refreshMatches" 
                      class="group flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur border border-white/20 rounded-xl text-white font-medium hover:bg-white/20 transition-all duration-300"
                      :disabled="refreshing">
                <svg class="w-5 h-5" :class="{ 'animate-spin': refreshing }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                {{ refreshing ? 'Refreshing...' : 'Refresh' }}
              </button>
            </div>
          </div>

          <!-- Live Stats Bar -->
          <div class="mt-6 flex gap-4">
            <div class="bg-white/10 backdrop-blur rounded-xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer flex-1">
              <div class="text-2xl font-bold">{{ liveMatches.length }}</div>
              <div class="text-xs text-white/70">Live Now</div>
            </div>
            <div class="bg-white/10 backdrop-blur rounded-xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer flex-1">
              <div class="text-2xl font-bold">{{ totalGoalsScored }}</div>
              <div class="text-xs text-white/70">Goals Today</div>
            </div>
            <div class="bg-white/10 backdrop-blur rounded-xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer flex-1">
              <div class="text-2xl font-bold">{{ competitionsCount }}</div>
              <div class="text-xs text-white/70">Competitions</div>
            </div>
            <div class="bg-white/10 backdrop-blur rounded-xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer flex-1">
              <div class="text-xs text-white/70">Source</div>
              <div class="text-sm font-semibold">{{ selectedSource === 'flashscore' ? 'FlashScore' : 'ESPN' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Auto-Refresh Indicator -->
      <div v-if="liveMatches.length > 0 && !loading" class="flex items-center justify-between">
        <div class="flex items-center gap-2 text-sm text-gray-500">
          <div class="w-2 h-2 bg-green-500 rounded-full"></div>
          <span>Auto-refreshing every 30s</span>
          <span class="text-gray-400">· Last updated: {{ lastUpdated }}</span>
        </div>
        <button @click="toggleSound" 
                class="flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-700 transition-colors"
                :title="soundEnabled ? 'Mute goal alerts' : 'Enable goal alerts'">
          <svg v-if="soundEnabled" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
          </svg>
          <svg v-else class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>
          </svg>
          {{ soundEnabled ? 'Sound On' : 'Sound Off' }}
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 animate-pulse">
          <div class="flex items-center gap-2 mb-4">
            <div class="h-3 bg-gray-200 rounded-full w-20"></div>
            <div class="h-2 w-2 bg-gray-200 rounded-full"></div>
            <div class="h-3 bg-gray-200 rounded-full w-12"></div>
          </div>
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-gray-200 rounded-xl"></div>
                <div class="h-4 bg-gray-200 rounded-full w-28"></div>
              </div>
              <div class="h-8 w-8 bg-gray-200 rounded-lg"></div>
            </div>
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-gray-200 rounded-xl"></div>
                <div class="h-4 bg-gray-200 rounded-full w-28"></div>
              </div>
              <div class="h-8 w-8 bg-gray-200 rounded-lg"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Live Matches Grid -->
      <div v-else-if="liveMatches.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="match in liveMatches" :key="match.id"
             class="group relative bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer"
             @click="$router.push(`/match/${match.id}`)">
          
          <!-- Competition Header -->
          <div class="absolute top-0 left-0 right-0 bg-gradient-to-r from-gray-50 to-white px-5 py-2 border-b border-gray-100 flex items-center justify-between">
            <span class="text-xs font-semibold text-gray-600">{{ match.competition || 'Friendly' }}</span>
            <span class="flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
              <span class="text-xs font-bold text-green-600">LIVE</span>
            </span>
          </div>

          <!-- Match Content -->
          <div class="pt-12 p-5">
            <!-- Home Team -->
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-3 flex-1">
                <div class="w-12 h-12 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-1.5 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <img v-if="match.home_team_logo" :src="match.home_team_logo" 
                       class="w-10 h-10 object-contain" 
                       :alt="match.home_team" />
                  <div v-else class="w-10 h-10 bg-gray-200 rounded-lg flex items-center justify-center">
                    <span class="text-sm font-bold text-gray-500">{{ (match.home_team || 'H').charAt(0) }}</span>
                  </div>
                </div>
                <span class="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">{{ match.home_team }}</span>
              </div>
              <span class="text-3xl font-black text-gray-900 ml-4">{{ match.home_score || 0 }}</span>
            </div>

            <!-- Away Team -->
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-3 flex-1">
                <div class="w-12 h-12 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-1.5 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <img v-if="match.away_team_logo" :src="match.away_team_logo" 
                       class="w-10 h-10 object-contain" 
                       :alt="match.away_team" />
                  <div v-else class="w-10 h-10 bg-gray-200 rounded-lg flex items-center justify-center">
                    <span class="text-sm font-bold text-gray-500">{{ (match.away_team || 'A').charAt(0) }}</span>
                  </div>
                </div>
                <span class="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">{{ match.away_team }}</span>
              </div>
              <span class="text-3xl font-black text-gray-900 ml-4">{{ match.away_score || 0 }}</span>
            </div>

            <!-- Match Status Bar -->
            <div class="flex items-center justify-between pt-4 border-t border-gray-100">
              <div class="flex items-center gap-2">
                <!-- Minute with Animated Background -->
                <span class="px-3 py-1 bg-red-50 text-red-700 rounded-lg text-sm font-bold flex items-center gap-1.5">
                  <span class="relative flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
                  </span>
                  {{ match.minute || 0 }}'
                </span>
                
                <!-- Match Events -->
                <div v-if="match.events?.length" class="flex gap-1">
                  <span v-for="(event, idx) in match.events.slice(0, 3)" :key="idx"
                        class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold"
                        :class="getEventStyle(event.type)"
                        :title="event.type">
                    {{ getEventIcon(event.type) }}
                  </span>
                </div>
              </div>
              
              <!-- View Details -->
              <span class="text-sm font-medium text-primary-600 opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">
                Details
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </span>
            </div>
          </div>

          <!-- Hover Overlay -->
          <div class="absolute inset-0 bg-gradient-to-t from-primary-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"></div>
        </div>
      </div>

      <!-- No Live Matches State -->
      <div v-else class="text-center py-16">
        <div class="relative inline-block mb-6">
          <div class="w-32 h-32 bg-gradient-to-br from-gray-100 to-gray-200 rounded-3xl flex items-center justify-center shadow-lg">
            <span class="text-6xl">📺</span>
          </div>
          <div class="absolute -top-2 -right-2 w-8 h-8 bg-red-500 rounded-full border-4 border-white flex items-center justify-center">
            <span class="w-2 h-2 bg-white rounded-full"></span>
          </div>
        </div>
        
        <h3 class="text-2xl font-bold text-gray-900 mb-2">No Live Matches Right Now</h3>
        <p class="text-gray-500 mb-6 max-w-md mx-auto">
          There are no matches currently in progress. Check back soon or explore upcoming fixtures.
        </p>
        
        <!-- Quick Links -->
        <div class="flex flex-col sm:flex-row gap-3 justify-center mb-8">
          <router-link to="/" 
                       class="inline-flex items-center gap-2 px-6 py-2.5 bg-primary-600 text-white font-medium rounded-xl hover:bg-primary-700 transition-all duration-300 hover:shadow-lg">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            Today's Matches
          </router-link>
          <router-link to="/competitions" 
                       class="inline-flex items-center gap-2 px-6 py-2.5 bg-white border-2 border-gray-200 text-gray-700 font-medium rounded-xl hover:border-primary-300 hover:text-primary-600 transition-all duration-300">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            Browse Competitions
          </router-link>
        </div>

        <div class="text-center text-sm text-gray-400">
          <p>Source: {{ selectedSource === 'flashscore' ? 'FlashScore API' : 'ESPN API' }}</p>
          <p class="mt-1">Auto-refreshing every 30 seconds</p>
        </div>
        
        <button @click="refreshMatches" 
                class="mt-6 inline-flex items-center gap-2 px-6 py-2.5 bg-gray-100 text-gray-700 font-medium rounded-xl hover:bg-gray-200 transition-all duration-300">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh Now
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUIStore } from '@/stores/ui'
import { liveApi } from '@/services/liveApi'

const router = useRouter()
const uiStore = useUIStore()

const loading = ref(true)
const refreshing = ref(false)
const liveMatches = ref([])
const selectedSource = ref('flashscore')
const soundEnabled = ref(false)
const lastUpdated = ref('')
let refreshInterval = null
let previousScores = new Map()

const sources = [
  { value: 'flashscore', label: 'FlashScore', icon: '⚡' },
  { value: 'espn', label: 'ESPN', icon: '🏈' }
]

const totalGoalsScored = computed(() => {
  return liveMatches.value.reduce((total, match) => {
    const homeScore = parseInt(match.home_score) || 0
    const awayScore = parseInt(match.away_score) || 0
    return total + homeScore + awayScore
  }, 0)
})

const competitionsCount = computed(() => {
  const competitions = new Set(liveMatches.value.map(m => m.competition).filter(Boolean))
  return competitions.size
})

function getEventStyle(eventType) {
  const styles = {
    'goal': 'bg-green-100 text-green-700',
    'yellow_card': 'bg-yellow-100 text-yellow-700',
    'red_card': 'bg-red-100 text-red-700',
    'substitution': 'bg-blue-100 text-blue-700',
    'penalty': 'bg-orange-100 text-orange-700',
    'own_goal': 'bg-purple-100 text-purple-700',
  }
  return styles[eventType] || 'bg-gray-100 text-gray-600'
}

function getEventIcon(eventType) {
  const icons = {
    'goal': '⚽',
    'yellow_card': '🟨',
    'red_card': '🟥',
    'substitution': '🔄',
    'penalty': '🎯',
    'own_goal': '😱',
  }
  return icons[eventType] || '•'
}

function checkForGoals(currentMatches) {
  if (!soundEnabled.value) return
  
  currentMatches.forEach(match => {
    const prevScore = previousScores.get(match.id)
    const currentTotal = (parseInt(match.home_score) || 0) + (parseInt(match.away_score) || 0)
    
    if (prevScore !== undefined && currentTotal > prevScore) {
      playGoalSound()
      uiStore.showNotification(`⚽ Goal! ${match.home_team} ${match.home_score} - ${match.away_score} ${match.away_team}`, 'Goal Alert!')
    }
    
    previousScores.set(match.id, currentTotal)
  })
}

function playGoalSound() {
  try {
    const audio = new Audio('/sounds/goal.mp3')
    audio.volume = 0.5
    audio.play()
  } catch (error) {
    console.log('Sound not available')
  }
}

function toggleSound() {
  soundEnabled.value = !soundEnabled.value
  uiStore.showSuccess(
    soundEnabled.value ? 'Goal alerts enabled! 🔊' : 'Goal alerts muted 🔇',
    ''
  )
}

async function loadLiveMatches() {
  if (liveMatches.value.length === 0) loading.value = true
  
  try {
    let matches = []
    
    if (selectedSource.value === 'flashscore') {
      matches = await liveApi.getFlashScoreLiveMatches()
    } else {
      matches = await liveApi.getESPNLiveMatches('soccer')
    }
    
    // Check for new goals
    checkForGoals(matches)
    
    liveMatches.value = matches
    lastUpdated.value = new Date().toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    })
  } catch (error) {
    console.error('Failed to load live matches:', error)
    if (liveMatches.value.length === 0) {
      uiStore.showError('Failed to load live matches', 'Please try again')
    }
  } finally {
    loading.value = false
  }
}

async function refreshMatches() {
  refreshing.value = true
  try {
    await loadLiveMatches()
    uiStore.showSuccess('Live matches updated!', '')
  } catch (error) {
    console.error('Failed to refresh:', error)
    uiStore.showError('Failed to refresh', 'Please try again')
  } finally {
    refreshing.value = false
  }
}

// Watch for source changes
watch(selectedSource, () => {
  previousScores.clear()
  loadLiveMatches()
})

onMounted(() => {
  loadLiveMatches()
  refreshInterval = setInterval(loadLiveMatches, 30000)
})

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
})
</script>

<style scoped>
@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

.animate-ping {
  animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>