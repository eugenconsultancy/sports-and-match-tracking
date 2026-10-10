<template>
  <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium"
        :class="badgeClasses">
    <slot />
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'success', 'warning', 'error', 'info', 'live'].includes(v),
  },
})

const badgeClasses = computed(() => {
  const variants = {
    default: 'bg-gray-100 text-gray-800',
    success: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    error: 'bg-red-100 text-red-800',
    info: 'bg-blue-100 text-blue-800',
    live: 'bg-red-600 text-white animate-pulse',
  }
  return variants[props.variant] || variants.default
})
</script>