<template>
  <div class="group relative bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
       @click="goToMatch">
    
    <!-- Top Gradient Bar (Live matches get animated gradient) -->
    <div class="h-1 w-full transition-all duration-300"
         :class="isLive ? 'bg-gradient-to-r from-red-500 via-red-600 to-red-500 animate-gradient' : 'bg-gradient-to-r from-gray-300 to-gray-400'">
    </div>

    <!-- Match Content -->
    <div class="p-5">
      <!-- Match Header -->
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center gap-2 min-w-0">
          <span class="text-xs font-medium text-gray-500 truncate">{{ competitionName }}</span>
        </div>
        
        <!-- Status Badge -->
        <div class="flex-shrink-0">
          <!-- Live Status -->
          <div v-if="isLive" 
               class="px-2.5 py-1 bg-red-50 rounded-lg flex items-center gap-1.5">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
            </span>
            <span class="text-xs font-bold text-red-700">{{ match.minute || 0 }}'</span>
          </div>
          
          <!-- Finished Status -->
          <div v-else-if="isFinished" 
               class="px-2.5 py-1 bg-gray-100 rounded-lg">
            <span class="text-xs font-semibold text-gray-500">FT</span>
          </div>
          
          <!-- Scheduled Status -->
          <div v-else 
               class="px-2.5 py-1 bg-blue-50 rounded-lg">
            <span class="text-xs font-semibold text-blue-600">{{ formatTime(match.kickoff_time) }}</span>
          </div>
        </div>
      </div>
      
      <!-- Teams and Scores -->
      <div class="space-y-3">
        <!-- Home Team -->
        <div class="flex items-center justify-between group/row">
          <div class="flex items-center gap-3 min-w-0 flex-1">
            <!-- Team Logo -->
            <div class="w-10 h-10 relative flex-shrink-0">
              <div class="absolute inset-0 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl group-hover/row:scale-110 transition-transform duration-300"></div>
              <div class="relative w-full h-full rounded-xl p-1.5 flex items-center justify-center">
                <img v-if="match.home_team_logo" 
                     :src="match.home_team_logo" 
                     :alt="match.home_team_name"
                     class="w-7 h-7 object-contain relative z-10" />
                <div v-else 
                     class="w-7 h-7 bg-primary-100 rounded-lg flex items-center justify-center relative z-10">
                  <span class="text-xs font-bold text-primary-600">{{ match.home_team_name?.charAt(0) }}</span>
                </div>
              </div>
            </div>
            
            <!-- Team Name -->
            <span class="text-sm font-semibold text-gray-900 truncate group-hover/row:text-primary-600 transition-colors">
              {{ match.home_team_name }}
            </span>
          </div>
          
          <!-- Score -->
          <span class="text-2xl font-black ml-4 flex-shrink-0"
                :class="isLive ? 'text-red-600' : 'text-gray-900'">
            {{ match.home_score ?? 0 }}
          </span>
        </div>
        
        <!-- Away Team -->
        <div class="flex items-center justify-between group/row">
          <div class="flex items-center gap-3 min-w-0 flex-1">
            <!-- Team Logo -->
            <div class="w-10 h-10 relative flex-shrink-0">
              <div class="absolute inset-0 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl group-hover/row:scale-110 transition-transform duration-300"></div>
              <div class="relative w-full h-full rounded-xl p-1.5 flex items-center justify-center">
                <img v-if="match.away_team_logo" 
                     :src="match.away_team_logo" 
                     :alt="match.away_team_name"
                     class="w-7 h-7 object-contain relative z-10" />
                <div v-else 
                     class="w-7 h-7 bg-gray-200 rounded-lg flex items-center justify-center relative z-10">
                  <span class="text-xs font-bold text-gray-600">{{ match.away_team_name?.charAt(0) }}</span>
                </div>
              </div>
            </div>
            
            <!-- Team Name -->
            <span class="text-sm font-semibold text-gray-900 truncate group-hover/row:text-primary-600 transition-colors">
              {{ match.away_team_name }}
            </span>
          </div>
          
          <!-- Score -->
          <span class="text-2xl font-black ml-4 flex-shrink-0"
                :class="isLive ? 'text-red-600' : 'text-gray-900'">
            {{ match.away_score ?? 0 }}
          </span>
        </div>
      </div>

      <!-- Possession Bar (Live matches only) -->
      <div v-if="isLive && match.live_state?.possession" class="mt-4 pt-4 border-t border-gray-100">
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-xs text-gray-500">Possession</span>
          <span class="text-xs font-medium text-gray-600">
            {{ match.live_state.possession?.home || 50 }}% - {{ match.live_state.possession?.away || 50 }}%
          </span>
        </div>
        <div class="relative h-2 bg-gray-100 rounded-full overflow-hidden">
          <!-- Home Possession -->
          <div class="absolute inset-y-0 left-0 bg-gradient-to-r from-primary-500 to-primary-600 transition-all duration-700"
               :style="{ width: `${match.live_state.possession?.home || 50}%` }">
          </div>
          <!-- Center Line -->
          <div class="absolute inset-y-0 left-1/2 w-0.5 bg-white transform -translate-x-1/2"></div>
        </div>
      </div>

      <!-- Match Events (Goals, Cards) -->
      <div v-if="isLive && match.events?.length" class="mt-4 pt-4 border-t border-gray-100">
        <div class="flex items-center gap-2 overflow-x-auto pb-1 custom-scrollbar">
          <div v-for="event in match.events.slice(0, 5)" :key="event.id"
               class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center text-sm"
               :class="getEventStyle(event.type)"
               :title="`${event.player_name} - ${event.type} (${event.minute}')`">
            {{ getEventIcon(event.type) }}
          </div>
          <span v-if="match.events.length > 5" 
                class="text-xs text-gray-400 ml-1">
            +{{ match.events.length - 5 }}
          </span>
        </div>
      </div>

      <!-- Footer: View Details -->
      <div v-if="isLive" class="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between">
        <span class="text-xs text-gray-400">{{ getMatchStatusText }}</span>
        <span class="text-xs font-medium text-primary-600 opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">
          View Details
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </span>
      </div>
    </div>

    <!-- Hover Overlay -->
    <div class="absolute inset-0 bg-gradient-to-t from-primary-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none rounded-2xl"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  match: {
    type: Object,
    required: true,
  },
})

const router = useRouter()

const isLive = computed(() => props.match.status === 'live' || props.match.status === 'half_time')
const isFinished = computed(() => props.match.status === 'finished')
const competitionName = computed(() => props.match.competition_name || props.match.competition || 'Friendly')

const getMatchStatusText = computed(() => {
  if (props.match.status === 'half_time') return 'Half Time'
  if (props.match.status === 'live') return 'Second Half'
  return ''
})

function formatTime(dateString) {
  if (!dateString) return 'TBD'
  const date = new Date(dateString)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function getEventStyle(eventType) {
  const styles = {
    'goal': 'bg-green-100 text-green-700',
    'own_goal': 'bg-red-100 text-red-700',
    'penalty': 'bg-orange-100 text-orange-700',
    'yellow_card': 'bg-yellow-100 text-yellow-700',
    'red_card': 'bg-red-100 text-red-700',
    'substitution': 'bg-blue-100 text-blue-700',
    'assist': 'bg-purple-100 text-purple-700',
  }
  return styles[eventType] || 'bg-gray-100 text-gray-600'
}

function getEventIcon(eventType) {
  const icons = {
    'goal': '⚽',
    'own_goal': '😱',
    'penalty': '🎯',
    'yellow_card': '🟨',
    'red_card': '🟥',
    'substitution': '🔄',
    'assist': '👟',
  }
  return icons[eventType] || '•'
}

function goToMatch() {
  router.push(`/match/${props.match.id}`)
}
</script>

<style scoped>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.custom-scrollbar::-webkit-scrollbar {
  height: 3px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 20px;
}

@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.animate-gradient {
  background-size: 200% 200%;
  animation: gradient 2s ease infinite;
}

@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

.animate-ping {
  animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
}
</style>