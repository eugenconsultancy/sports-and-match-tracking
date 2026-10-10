<template>
  <div class="card cursor-pointer text-center hover:border-primary-300 hover:shadow-lg transition-all group"
       @click="$emit('click')">
    <img v-if="team.logo_url"
         :src="team.logo_url"
         :alt="team.name"
         class="w-16 h-16 mx-auto object-contain group-hover:scale-110 transition-transform" />
    <div v-else
         class="w-16 h-16 mx-auto rounded-full flex items-center justify-center text-2xl font-bold text-white mx-auto"
         :style="{ backgroundColor: team.primary_color || '#3b82f6' }">
      {{ team.name?.charAt(0) }}
    </div>
    <h3 class="font-semibold text-sm mt-2 line-clamp-2">{{ team.name }}</h3>
    <p class="text-xs text-gray-500">{{ team.country }}</p>
  </div>
</template>

<script setup>
defineProps({ team: { type: Object, required: true } })
defineEmits(['click'])
</script>