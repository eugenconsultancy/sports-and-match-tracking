<template>
  <div class="group relative bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
       @click="$emit('click')">
    
    <!-- Top Gradient Bar -->
    <div class="h-1.5 w-full bg-gradient-to-r opacity-80 group-hover:opacity-100 transition-opacity"
         :style="{ backgroundImage: `linear-gradient(to right, ${competition.primary_color || '#3b82f6'}, ${competition.secondary_color || '#8b5cf6'})` }">
    </div>

    <!-- Card Content -->
    <div class="p-5">
      <!-- Logo Section -->
      <div class="relative mb-4">
        <div class="w-20 h-20 mx-auto relative">
          <!-- Background Glow -->
          <div class="absolute inset-0 bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl group-hover:scale-110 transition-transform duration-300"
               :style="{ boxShadow: `0 0 20px ${competition.primary_color || '#3b82f6'}10` }">
          </div>
          
          <!-- Logo Image -->
          <div class="relative w-full h-full rounded-2xl p-2 flex items-center justify-center">
            <img v-if="competition.logo_url"
                 :src="competition.logo_url"
                 :alt="competition.name"
                 class="w-16 h-16 object-contain relative z-10 group-hover:scale-110 transition-transform duration-300" />
            <div v-else
                 class="w-16 h-16 rounded-xl flex items-center justify-center text-2xl font-bold text-white relative z-10"
                 :style="{ backgroundColor: competition.primary_color || '#3b82f6' }">
              {{ competition.name?.charAt(0) }}
            </div>
          </div>

          <!-- Status Indicator -->
          <div v-if="competition.is_active" 
               class="absolute -top-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-white flex items-center justify-center shadow-sm">
            <span class="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>
          </div>
        </div>
      </div>

      <!-- Competition Info -->
      <div class="text-center">
        <!-- Name -->
        <h3 class="font-bold text-gray-900 group-hover:text-primary-600 transition-colors line-clamp-2 mb-2">
          {{ competition.name }}
        </h3>
        
        <!-- Country & Tier -->
        <div class="flex items-center justify-center gap-2 mb-3">
          <span class="text-xs text-gray-500 flex items-center gap-1">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064" />
            </svg>
            {{ competition.country }}
          </span>
          <span class="text-gray-300">•</span>
          <span class="text-xs text-gray-500">Tier {{ competition.tier }}</span>
        </div>

        <!-- Badges -->
        <div class="flex items-center justify-center gap-2">
          <span class="px-2.5 py-1 rounded-full text-xs font-semibold"
                :class="getTypeClasses(competition.competition_type)">
            {{ formatType(competition.competition_type) }}
          </span>
          
          <span v-if="competition.is_active"
                class="px-2.5 py-1 bg-green-50 text-green-700 rounded-full text-xs font-semibold flex items-center gap-1">
            <span class="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
            Active
          </span>
        </div>
      </div>

      <!-- Quick Stats (Optional - shown if data available) -->
      <div v-if="competition.teams_count || competition.matches_count" 
           class="mt-4 pt-4 border-t border-gray-100">
        <div class="grid grid-cols-2 gap-3">
          <div v-if="competition.teams_count" class="text-center">
            <p class="text-lg font-bold text-gray-900">{{ competition.teams_count }}</p>
            <p class="text-xs text-gray-500">Teams</p>
          </div>
          <div v-if="competition.matches_count" class="text-center">
            <p class="text-lg font-bold text-gray-900">{{ competition.matches_count }}</p>
            <p class="text-xs text-gray-500">Matches</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Hover Overlay -->
    <div class="absolute inset-0 bg-gradient-to-t from-primary-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none rounded-2xl"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  competition: { 
    type: Object, 
    required: true,
    validator: (obj) => {
      return obj.name && obj.competition_type
    }
  },
  showStats: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])

function getTypeClasses(type) {
  const classes = {
    league: 'bg-blue-50 text-blue-700',
    cup: 'bg-yellow-50 text-yellow-700',
    international: 'bg-purple-50 text-purple-700',
    friendly: 'bg-gray-50 text-gray-700',
  }
  return classes[type] || 'bg-gray-50 text-gray-700'
}

function formatType(type) {
  const formats = {
    league: 'League',
    cup: 'Cup',
    international: 'International',
    friendly: 'Friendly',
  }
  return formats[type] || type
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  overflow: hidden;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>