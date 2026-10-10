<template>
  <div v-if="matches.length > 0" class="card overflow-hidden">
    <div class="flex items-center gap-3">
      <!-- Live Label -->
      <div class="flex-shrink-0 flex items-center gap-2 pr-4 border-r border-gray-200">
        <span class="live-indicator text-red-600 text-lg">●</span>
        <span class="text-sm font-bold text-red-600">LIVE</span>
      </div>

      <!-- Scrolling Matches -->
      <div class="flex-1 overflow-hidden">
        <div class="flex items-center gap-6 animate-scroll">
          <div v-for="match in duplicatedMatches" :key="match.id + '-' + match._key"
               class="flex items-center gap-3 flex-shrink-0 cursor-pointer hover:bg-gray-50 rounded-lg px-3 py-1 transition-colors"
               @click="$router.push(`/match/${match.id}`)">
            <!-- Home -->
            <div class="flex items-center gap-2">
              <img v-if="match.home_team_logo" :src="match.home_team_logo" class="w-5 h-5 object-contain" />
              <span class="text-sm font-medium">{{ match.home_team_name }}</span>
            </div>

            <!-- Score -->
            <span class="text-lg font-bold tabular-nums text-red-600">
              {{ match.home_score }} - {{ match.away_score }}
            </span>

            <!-- Away -->
            <div class="flex items-center gap-2">
              <img v-if="match.away_team_logo" :src="match.away_team_logo" class="w-5 h-5 object-contain" />
              <span class="text-sm font-medium">{{ match.away_team_name }}</span>
            </div>

            <!-- Minute -->
            <span class="text-xs text-gray-400">{{ match.minute }}'</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  matches: { type: Array, default: () => [] },
})

// Duplicate matches for seamless infinite scroll effect
const duplicatedMatches = computed(() => {
  return [
    ...props.matches.map((m, i) => ({ ...m, _key: `a-${i}` })),
    ...props.matches.map((m, i) => ({ ...m, _key: `b-${i}` })),
  ]
})
</script>

<style scoped>
@keyframes scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.animate-scroll {
  animation: scroll 30s linear infinite;
}
.animate-scroll:hover {
  animation-play-state: paused;
}
</style>