<template>
  <div class="overflow-x-auto">
    <table class="table w-full">
      <thead>
        <tr v-if="!compact">
          <th class="w-10">#</th>
          <th>Team</th>
          <th class="text-center w-10">P</th>
          <th class="text-center w-10">W</th>
          <th class="text-center w-10">D</th>
          <th class="text-center w-10">L</th>
          <th class="text-center w-12">GF</th>
          <th class="text-center w-12">GA</th>
          <th class="text-center w-12">GD</th>
          <th class="text-center w-12 font-bold">Pts</th>
          <th class="text-center w-24">Form</th>
        </tr>
        <tr v-else>
          <th class="w-8">#</th>
          <th>Team</th>
          <th class="text-center w-8">P</th>
          <th class="text-center w-10 font-bold">Pts</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="entry in standings" :key="entry.id"
            class="cursor-pointer hover:bg-gray-50 transition-colors"
            :class="{
              'bg-green-50': entry.position <= promotionZone,
              'bg-red-50': entry.position > relegationZone && relegationZone > 0,
            }"
            @click="$emit('teamClick', entry.team)">
          
          <td class="text-center font-bold" :class="getPositionClass(entry.position)">
            {{ entry.position }}
          </td>
          
          <td>
            <div class="flex items-center gap-2">
              <img v-if="entry.team_logo" :src="entry.team_logo" class="w-5 h-5 object-contain" />
              <span class="font-medium text-sm">{{ entry.team_name }}</span>
            </div>
          </td>
          
          <td class="text-center">{{ entry.played }}</td>
          
          <template v-if="!compact">
            <td class="text-center">{{ entry.wins }}</td>
            <td class="text-center">{{ entry.draws }}</td>
            <td class="text-center">{{ entry.losses }}</td>
            <td class="text-center">{{ entry.goals_for }}</td>
            <td class="text-center">{{ entry.goals_against }}</td>
            <td class="text-center" :class="getGoalDiffClass(entry.goal_difference)">
              {{ entry.goal_difference }}
            </td>
          </template>
          
          <td class="text-center font-bold">{{ entry.points }}</td>
          
          <td v-if="!compact" class="text-center">
            <div class="flex items-center justify-center gap-0.5">
              <span v-for="(result, idx) in (entry.form || '').split('')" :key="idx"
                    class="w-5 h-5 rounded-full text-[10px] font-bold flex items-center justify-center text-white"
                    :class="getFormClass(result)">
                {{ result }}
              </span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  standings: { type: Array, required: true },
  title: { type: String, default: '' },
  compact: { type: Boolean, default: false },
  promotionZone: { type: Number, default: 0 },
  relegationZone: { type: Number, default: 0 },
})
defineEmits(['teamClick'])

function getPositionClass(position) {
  if (position <= 4) return 'text-green-600'
  if (position >= 17 && position <= 20) return 'text-red-600'
  return 'text-gray-700'
}

function getGoalDiffClass(gd) {
  if (gd > 0) return 'text-green-600'
  if (gd < 0) return 'text-red-600'
  return 'text-gray-500'
}

function getFormClass(result) {
  const classes = {
    'W': 'bg-green-500',
    'D': 'bg-yellow-500',
    'L': 'bg-red-500',
  }
  return classes[result] || 'bg-gray-400'
}
</script>