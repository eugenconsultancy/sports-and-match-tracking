<template>
  <div class="flex items-center gap-3 bg-white rounded-lg shadow-lg border p-4 min-w-[280px] max-w-sm animate-slide-in"
       :class="borderColor">
    <div :class="iconBgColor" class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0">
      <svg class="w-5 h-5" :class="iconColor" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path v-if="toast.type === 'success'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        <path v-else-if="toast.type === 'error'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        <path v-else-if="toast.type === 'warning'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    </div>
    <div class="flex-1">
      <p class="font-medium text-gray-900">{{ toast.title }}</p>
      <p class="text-sm text-gray-500">{{ toast.message }}</p>
    </div>
    <button @click="$emit('close')" class="p-1 rounded-lg hover:bg-gray-100 transition-colors flex-shrink-0">
      <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  toast: {
    type: Object,
    required: true,
    validator: (v) => ['success', 'error', 'warning', 'info'].includes(v.type),
  },
})
defineEmits(['close'])

const borderColor = computed(() => {
  const colors = {
    success: 'border-green-200',
    error: 'border-red-200',
    warning: 'border-yellow-200',
    info: 'border-blue-200',
  }
  return colors[props.toast.type]
})

const iconBgColor = computed(() => {
  const colors = {
    success: 'bg-green-100',
    error: 'bg-red-100',
    warning: 'bg-yellow-100',
    info: 'bg-blue-100',
  }
  return colors[props.toast.type]
})

const iconColor = computed(() => {
  const colors = {
    success: 'text-green-600',
    error: 'text-red-600',
    warning: 'text-yellow-600',
    info: 'text-blue-600',
  }
  return colors[props.toast.type]
})
</script>

<style scoped>
@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
.animate-slide-in {
  animation: slideIn 0.3s ease-out;
}
</style>