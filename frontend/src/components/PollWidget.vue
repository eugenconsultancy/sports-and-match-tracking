<template>
  <div class="card p-4">
    <div class="mb-3">
      <div class="flex items-center justify-between mb-1">
        <h3 class="font-bold text-lg">{{ poll.question || 'Who will win?' }}</h3>
        <Badge :variant="poll.status === 'active' ? 'live' : 'default'">
          {{ poll.status === 'active' ? 'LIVE' : 'Closed' }}
        </Badge>
      </div>
      <p class="text-sm text-gray-500">
        {{ matchName }} • {{ formatDate(poll.kickoff_time) }}
      </p>
    </div>
    
    <div class="space-y-3">
      <div v-for="option in pollOptions" :key="option.id"
           @click="canVote && handleVote(option.id)"
           class="relative rounded-lg border-2 p-3 transition-all"
           :class="[
             canVote ? 'hover:border-primary-300 cursor-pointer' : 'cursor-default',
             userVote === option.id ? 'border-green-500 bg-green-50' : 'border-gray-200'
           ]">
        
        <div class="flex items-center justify-between relative z-10">
          <div class="flex items-center gap-3">
            <img v-if="option.team_logo" :src="option.team_logo" class="w-5 h-5 object-contain" />
            <span class="font-medium">{{ option.label }}</span>
            <span v-if="userVote === option.id" class="text-xs text-green-600 font-medium">
              ✓ Your vote
            </span>
          </div>
          <span class="text-sm font-bold">{{ option.percentage || 0 }}%</span>
        </div>
        
        <!-- Progress Bar -->
        <div class="mt-2 stat-bar">
          <div class="stat-bar-fill" 
               :style="{ width: `${option.percentage || 0}%`, backgroundColor: getOptionColor(option.option_type) }"></div>
        </div>
        
        <div class="flex justify-between text-xs text-gray-500 mt-1">
          <span>{{ option.vote_count || 0 }} votes</span>
          <span>{{ option.percentage || 0 }}%</span>
        </div>
      </div>
    </div>
    
    <div class="mt-3 pt-2 border-t border-gray-100 flex justify-between text-xs text-gray-400">
      <span>Total: {{ totalVotes }} votes</span>
      <span v-if="!canVote && !userVote && poll.status === 'active'">
        Sign in to vote
      </span>
      <span v-else-if="userVote" class="text-green-600">
        ✓ Voted
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { api } from '@/services/api'
import { useWebSocket } from '@/composables/useWebSocket'
import Badge from '@/components/ui/Badge.vue'
import { formatDate } from '@/utils/formatters'
import { useMatchStore } from '@/stores/matches'

const props = defineProps({
  pollId: String,
  matchId: String,
  initialData: Object,
})

const authStore = useAuthStore()
const uiStore = useUIStore()
const matchStore = useMatchStore()

const poll = ref(props.initialData || {})
const pollOptions = ref([])
const totalVotes = ref(0)
const userVote = ref(null)
const loading = ref(false)

const matchName = computed(() => {
  if (poll.value.match_info) {
    return `${poll.value.match_info.home_team} vs ${poll.value.match_info.away_team}`
  }
  return 'Match Poll'
})

const canVote = computed(() => {
  return authStore.isAuthenticated && 
         poll.value.status === 'active' && 
         !userVote.value &&
         !loading.value
})

function getOptionColor(optionType) {
  const colors = {
    home: '#3b82f6',
    draw: '#eab308',
    away: '#ef4444',
  }
  return colors[optionType] || '#8b5cf6'
}

async function handleVote(optionId) {
  if (!authStore.isAuthenticated) {
    uiStore.showWarning('Please sign in to vote', 'Authentication Required')
    return
  }
  
  if (userVote.value) {
    uiStore.showInfo('You have already voted', 'Only one vote per poll')
    return
  }
  
  loading.value = true
  
  try {
    const result = await api.vote(props.pollId, optionId)
    if (result) {
      uiStore.showSuccess('Vote recorded!', 'Thank you for voting')
      await loadPollData()
    }
  } catch (error) {
    console.error('Vote failed:', error)
    uiStore.showError('Failed to record vote', 'Please try again')
  } finally {
    loading.value = false
  }
}

async function loadPollData() {
  try {
    let pollData = props.initialData
    
    if (!pollData && props.pollId) {
      pollData = await api.getPoll(props.pollId)
    }
    
    if (pollData) {
      poll.value = pollData
      pollOptions.value = pollData.options || []
      totalVotes.value = pollData.total_votes || 0
      
      // Check if user has voted
      if (authStore.isAuthenticated && pollData.user_vote) {
        userVote.value = pollData.user_vote.option_id
      }
    }
  } catch (error) {
    console.error('Failed to load poll:', error)
  }
}

// WebSocket for real-time updates
let unsubscribe = null

onMounted(() => {
  loadPollData()
  
  // Connect to WebSocket for real-time updates if we have a poll ID
  if (props.pollId) {
    const { addListener } = useWebSocket(`/ws/poll/${props.pollId}`, {
      autoConnect: true,
      onMessage: (data) => {
        if (data.type === 'poll_update' || data.type === 'initial_poll_results') {
          const updateData = data.data
          if (updateData.results) {
            pollOptions.value = updateData.results
            totalVotes.value = updateData.total_votes
            poll.value.total_votes = updateData.total_votes
          }
        }
      },
    })
  }
})

onUnmounted(() => {
  if (unsubscribe) unsubscribe()
})
</script>