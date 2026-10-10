<template>
  <div class="space-y-8">
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold">Fan Polls</h1>
        <p class="text-gray-500 mt-1">Vote and see what other fans think</p>
      </div>
      <div class="flex gap-2">
        <button v-for="filter in statusFilters" :key="filter.value"
                @click="statusFilter = filter.value"
                class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                :class="statusFilter === filter.value 
                  ? 'bg-primary-600 text-white' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'">
          {{ filter.label }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="i in 4" :key="i" class="card p-6">
        <div class="skeleton h-6 w-48 mb-3"></div>
        <div class="skeleton h-4 w-32 mb-4"></div>
        <div class="space-y-3">
          <div class="skeleton h-12 w-full"></div>
          <div class="skeleton h-12 w-full"></div>
          <div class="skeleton h-12 w-full"></div>
        </div>
      </div>
    </div>

    <!-- Polls Grid -->
    <div v-else-if="filteredPolls.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="poll in filteredPolls" :key="poll.id" class="card p-6">
        <!-- Poll Header -->
        <div class="mb-4">
          <div class="flex items-center justify-between mb-2">
            <Badge :variant="poll.status === 'active' ? 'success' : 'default'">
              {{ poll.status === 'active' ? 'Active' : 'Closed' }}
            </Badge>
            <span class="text-xs text-gray-400">{{ poll.total_votes || 0 }} votes</span>
          </div>
          <h3 class="font-bold text-lg">{{ poll.question }}</h3>
          <p class="text-sm text-gray-500 mt-1">
            {{ poll.match_info?.home_team }} vs {{ poll.match_info?.away_team }}
          </p>
          <div class="flex items-center gap-2 mt-2 text-xs text-gray-400">
            <span>🏆 {{ poll.match_info?.competition_name || 'Match' }}</span>
            <span>•</span>
            <span>📅 {{ formatDate(poll.match_info?.kickoff_time) }}</span>
          </div>
        </div>

        <!-- Poll Options -->
        <div class="space-y-3">
          <div v-for="option in poll.options" :key="option.id"
               @click="poll.status === 'active' && !hasVoted(poll) && vote(poll.id, option.id)"
               class="relative cursor-pointer rounded-lg border-2 p-3 transition-all"
               :class="[
                 poll.status === 'active' && !hasVoted(poll) 
                   ? 'hover:border-primary-300 cursor-pointer' 
                   : 'cursor-default',
                 getUserVote(poll) === option.id 
                   ? 'border-green-500 bg-green-50' 
                   : 'border-gray-200'
               ]">
            
            <div class="flex items-center justify-between relative z-10">
              <div class="flex items-center gap-3">
                <img v-if="option.team_logo" :src="option.team_logo" class="w-6 h-6 object-contain" />
                <span class="font-medium">{{ option.label }}</span>
                <span v-if="getUserVote(poll) === option.id" class="text-xs text-green-600 font-medium">
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
            
            <span class="text-xs text-gray-500 mt-1 block">{{ option.vote_count || 0 }} votes</span>
          </div>
        </div>

        <!-- Poll Footer -->
        <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs text-gray-400">
          <span v-if="poll.end_time">Ends: {{ formatDate(poll.end_time) }}</span>
          <span v-else-if="poll.status === 'active'">No end date</span>
          <span v-else>Poll closed</span>
          <span>{{ (poll.total_votes || 0).toLocaleString() }} total votes</span>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="card text-center py-16">
      <div class="text-6xl mb-4">📊</div>
      <h3 class="text-xl font-semibold text-gray-700 mb-2">No Polls Found</h3>
      <p class="text-gray-500">Check back later for new polls on upcoming matches</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import Badge from '@/components/ui/Badge.vue'
import { formatDate } from '@/utils/formatters'

const authStore = useAuthStore()
const uiStore = useUIStore()

const loading = ref(true)
const polls = ref([])
const userVotes = ref({})
const statusFilter = ref('active')

const statusFilters = [
  { label: 'Active Polls', value: 'active' },
  { label: 'Closed Polls', value: 'closed' },
  { label: 'All Polls', value: 'all' },
]

const filteredPolls = computed(() => {
  if (statusFilter.value === 'all') return polls.value
  return polls.value.filter(p => p.status === statusFilter.value)
})

function hasVoted(poll) {
  return !!userVotes.value[poll.id]
}

function getUserVote(poll) {
  return userVotes.value[poll.id]
}

function getOptionColor(optionType) {
  const colors = {
    home: '#3b82f6',
    draw: '#eab308',
    away: '#ef4444',
  }
  return colors[optionType] || '#8b5cf6'
}

async function vote(pollId, optionId) {
  if (!authStore.isAuthenticated) {
    uiStore.showWarning('Please sign in to vote', 'Authentication Required')
    return
  }
  
  try {
    const result = await api.vote(pollId, optionId)
    if (result) {
      uiStore.showSuccess('Vote recorded!', 'Thank you for voting')
      await loadPolls()
    }
  } catch (error) {
    console.error('Vote failed:', error)
    uiStore.showError('Failed to record vote', 'Please try again')
  }
}

async function loadPolls() {
  loading.value = true
  try {
    const response = await api.getPolls({ limit: 50 })
    polls.value = response.results || response || []
    
    // Load user votes if authenticated
    if (authStore.isAuthenticated) {
      polls.value.forEach(poll => {
        if (poll.user_vote?.option_id) {
          userVotes.value[poll.id] = poll.user_vote.option_id
        }
      })
    }
  } catch (error) {
    console.error('Failed to load polls:', error)
    polls.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPolls()
})
</script>