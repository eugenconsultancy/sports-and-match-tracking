<template>
  <div class="card cursor-pointer hover:border-primary-300 transition-all group"
       @click="$router.push(`/player/${player.id}`)">
    <div class="flex items-center gap-4">
      <!-- Avatar -->
      <div class="flex-shrink-0">
        <img v-if="player.image_url"
             :src="player.image_url"
             :alt="player.full_name"
             class="w-14 h-14 rounded-full object-cover border-2 border-gray-200 group-hover:border-primary-300 transition-colors" />
        <div v-else
             class="w-14 h-14 rounded-full bg-primary-100 flex items-center justify-center text-xl font-bold text-primary-600">
          {{ player.full_name?.charAt(0) }}
        </div>
      </div>

      <!-- Info -->
      <div class="flex-1 min-w-0">
        <h4 class="font-semibold text-gray-900 truncate">{{ player.full_name }}</h4>
        <div class="flex items-center gap-2 mt-1">
          <span class="text-xs text-gray-500">{{ player.position }}</span>
          <span v-if="player.jersey_number" class="text-xs text-gray-400">#{{ player.jersey_number }}</span>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="flex-shrink-0 text-right">
        <div v-if="player.market_value" class="text-sm font-semibold text-green-600">
          {{ player.market_value_currency }} {{ formatNumber(player.market_value) }}
        </div>
        <div class="text-xs text-gray-400">{{ player.nationality }}</div>
      </div>
    </div>

    <!-- Expanded Stats (shown on team page) -->
    <div v-if="showStats && player.stats" class="mt-3 pt-3 border-t border-gray-100">
      <div class="grid grid-cols-4 gap-2 text-center text-xs">
        <div>
          <p class="font-bold text-gray-700">{{ player.stats.appearances || 0 }}</p>
          <p class="text-gray-400">Apps</p>
        </div>
        <div>
          <p class="font-bold text-green-600">{{ player.stats.goals || 0 }}</p>
          <p class="text-gray-400">Goals</p>
        </div>
        <div>
          <p class="font-bold text-blue-600">{{ player.stats.assists || 0 }}</p>
          <p class="text-gray-400">Assists</p>
        </div>
        <div>
          <p class="font-bold text-primary-600">{{ player.stats.average_rating || '-' }}</p>
          <p class="text-gray-400">Rating</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { formatNumber } from '@/utils/formatters'

defineProps({
  player: { type: Object, required: true },
  showStats: { type: Boolean, default: false },
})
</script>