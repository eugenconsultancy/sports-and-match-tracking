<template>
  <div class="card p-6">
    <!-- Match Info Header -->
    <div class="flex items-center gap-3 mb-4 pb-3 border-b border-gray-100">
      <div class="flex-1 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <img v-if="matchInfo?.home_team_logo" :src="matchInfo.home_team_logo" class="w-8 h-8 object-contain" />
          <span class="font-semibold">{{ matchInfo?.home_team }}</span>
        </div>
        <span class="text-sm text-gray-400">vs</span>
        <div class="flex items-center gap-2">
          <span class="font-semibold">{{ matchInfo?.away_team }}</span>
          <img v-if="matchInfo?.away_team_logo" :src="matchInfo.away_team_logo" class="w-8 h-8 object-contain" />
        </div>
      </div>
      <Badge variant="live" v-if="isLiveMatch">LIVE</Badge>
    </div>

    <!-- Poll Question -->
    <h3 class="text-lg font-bold mb-4">{{ poll.question || 'Who will win?' }}</h3>

    <!-- Vote Options with Live Progress -->
    <div class="space-y-3">
      <div v-for="option in pollOptions" :key="option.id"
           @click="handleVote(option.id)"
           class="relative rounded-lg border-2 p-3 transition-all cursor-pointer hover:border-primary-300"
           :class="userVote === option.id ? 'border-green-500 bg-green-50' : 'border-gray-200'">
        
        <div class="flex items-center justify-between relative z-10">
          <div class="flex items-center gap-3">
            <img v-if="option.team_logo" :src="option.team_logo" class="w-6 h-6 object-contain" />
            <span class="font-medium">{{ option.label }}</span>
            <span v-if="userVote === option.id" class="text-xs text-green-600 font-medium">
              ✓ Your vote
            </span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-sm font-bold">{{ option.percentage || 0 }}%</span>
            <span class="text-xs text-gray-400">{{ formatCompactNumber(option.vote_count || 0) }} votes</span>
          </div>
        </div>
        
        <!-- Animated Progress Bar -->
        <div class="mt-2 stat-bar">
          <div class="stat-bar-fill transition-all duration-500 ease-out" 
               :style="{ width: `${option.percentage || 0}%`, backgroundColor: getOptionColor(option.option_type) }">
          </div>
        </div>
      </div>
    </div>

    <!-- Live Stats Footer -->
    <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs text-gray-400">
      <div class="flex items-center gap-2">
        <span class="live-indicator-small" v-if="isLiveMatch"></span>
        <span>{{ totalVotes.toLocaleString() }} total votes</span>
      </div>
      <div v-if="voteRate > 0">
        📊 {{ voteRate }} votes/min
      </div>
      <div v-if="!userVote && poll.status === 'active' && !isAuthenticated" class="text-primary-600">
        Sign in to vote
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { liveApi } from '@/services/liveApi'
import Badge from '@/components/ui/Badge.vue'
import { formatCompactNumber } from '@/utils/formatters'

const props = defineProps({
  pollId: {
    type: String,
    required: true
  }
})

const authStore = useAuthStore()
const uiStore = useUIStore()

const poll = ref({})
const pollOptions = ref([])
const totalVotes = ref(0)
const userVote = ref(null)
const matchInfo = ref(null)
const voteRate = ref(0)
let wsConnection = null
let refreshInterval = null

const isAuthenticated = computed(() => authStore.isAuthenticated)
const isLiveMatch = computed(() => matchInfo.value?.status === 'live' || matchInfo.value?.status === 'half_time')

function getOptionColor(optionType) {
  const colors = {
    home: '#3b82f6',
    draw: '#eab308',
    away: '#ef4444',
  }
  return colors[optionType] || '#8b5cf6'
}

async function loadPollData() {
  try {
    const data = await liveApi.getPollWithLiveStats(props.pollId)
    if (data) {
      poll.value = data
      pollOptions.value = data.options || []
      totalVotes.value = data.total_votes || 0
      matchInfo.value = data.match_info
      
      if (isAuthenticated.value && data.user_vote) {
        userVote.value = data.user_vote.option_id
      }
    }
  } catch (error) {
    console.error('Failed to load poll:', error)
  }
}

async function loadPollTrends() {
  try {
    const trends = await liveApi.getPollTrends(props.pollId, 1)
    if (trends.length > 0) {
      const lastHourVotes = trends.length
      voteRate.value = parseFloat((lastHourVotes / 60).toFixed(1))
    }
  } catch (error) {
    console.error('Failed to load trends:', error)
  }
}

async function handleVote(optionId) {
  if (!isAuthenticated.value) {
    uiStore.showWarning('Please sign in to vote', 'Authentication Required')
    return
  }
  
  if (userVote.value) {
    uiStore.showInfo('You have already voted', 'Only one vote per poll')
    return
  }
  
  try {
    await liveApi.vote(props.pollId, optionId)
    uiStore.showSuccess('Vote recorded!', 'Thank you for voting')
    await loadPollData()
    await loadPollTrends()
  } catch (error) {
    uiStore.showError('Failed to record vote', 'Please try again')
  }
}

// Connect to WebSocket for real-time updates
function connectWebSocket() {
  wsConnection = liveApi.connectToLivePoll(props.pollId, (data) => {
    if (data.results) {
      pollOptions.value = data.results
      totalVotes.value = data.total_votes
      poll.value.total_votes = data.total_votes
    }
  })
}

onMounted(() => {
  loadPollData()
  loadPollTrends()
  connectWebSocket()
  
  // Refresh data every 10 seconds
  refreshInterval = setInterval(() => {
    loadPollData()
    loadPollTrends()
  }, 10000)
})

onUnmounted(() => {
  if (wsConnection) wsConnection.close()
  if (refreshInterval) clearInterval(refreshInterval)
})
</script>

<style scoped>
.live-indicator-small {
  display: inline-block;
  width: 8px;
  height: 8px;
  background-color: #ef4444;
  border-radius: 50%;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>