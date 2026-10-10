<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    @click="$emit('click')"
    class="inline-flex items-center justify-center gap-2 font-semibold transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed select-none"
    :class="[buttonClasses, animationClass]"
  >
    <!-- Loading Spinner -->
    <svg v-if="loading" class="animate-spin" :class="iconSizeClass" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
    </svg>

    <!-- Left Icon -->
    <span v-if="$slots.iconLeft && !loading" class="flex-shrink-0">
      <slot name="iconLeft" />
    </span>

    <!-- Content -->
    <span :class="{ 'opacity-0': loading }">
      <slot />
    </span>

    <!-- Right Icon -->
    <span v-if="$slots.iconRight && !loading" class="flex-shrink-0">
      <slot name="iconRight" />
    </span>

    <!-- Hover Arrow (for primary variant) -->
    <svg v-if="variant === 'primary' && !loading && showArrow" 
         class="transition-transform duration-300 group-hover:translate-x-1"
         :class="iconSizeClass"
         fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
    </svg>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (v) => [
      'primary', 'secondary', 'outline', 'ghost', 'danger',
      'success', 'warning', 'info', 'light', 'dark', 'gradient'
    ].includes(v),
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(v),
  },
  type: {
    type: String,
    default: 'button',
  },
  disabled: Boolean,
  loading: Boolean,
  fullWidth: Boolean,
  rounded: {
    type: String,
    default: 'lg',
    validator: (v) => ['md', 'lg', 'xl', 'full'].includes(v),
  },
  showArrow: {
    type: Boolean,
    default: false,
  },
  animation: {
    type: String,
    default: 'scale',
    validator: (v) => ['none', 'scale', 'slide', 'pulse'].includes(v),
  },
})

defineEmits(['click'])

const sizeClasses = {
  xs: 'px-2.5 py-1 text-xs rounded-lg gap-1.5',
  sm: 'px-3.5 py-2 text-sm rounded-lg gap-2',
  md: 'px-5 py-2.5 text-sm rounded-xl gap-2',
  lg: 'px-6 py-3 text-base rounded-xl gap-2.5',
  xl: 'px-8 py-4 text-lg rounded-2xl gap-3',
}

const roundedClasses = {
  md: 'rounded-md',
  lg: 'rounded-lg',
  xl: 'rounded-xl',
  full: 'rounded-full',
}

const iconSizeClass = computed(() => {
  const sizes = {
    xs: 'w-3 h-3',
    sm: 'w-3.5 h-3.5',
    md: 'w-4 h-4',
    lg: 'w-5 h-5',
    xl: 'w-6 h-6',
  }
  return sizes[props.size]
})

const variantClasses = {
  primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500 shadow-sm hover:shadow-md active:shadow-sm border border-primary-600',
  secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500 shadow-sm hover:shadow-md active:shadow-sm border border-gray-600',
  outline: 'border-2 border-gray-300 text-gray-700 hover:border-gray-400 hover:bg-gray-50 focus:ring-gray-500 bg-white hover:shadow-sm active:bg-gray-100',
  ghost: 'text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:ring-gray-500 active:bg-gray-200',
  danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500 shadow-sm hover:shadow-md active:shadow-sm border border-red-600',
  success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500 shadow-sm hover:shadow-md active:shadow-sm border border-green-600',
  warning: 'bg-yellow-500 text-white hover:bg-yellow-600 focus:ring-yellow-500 shadow-sm hover:shadow-md active:shadow-sm border border-yellow-500',
  info: 'bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-500 shadow-sm hover:shadow-md active:shadow-sm border border-blue-500',
  light: 'bg-white text-gray-700 hover:bg-gray-50 focus:ring-gray-300 shadow-sm border border-gray-200 hover:border-gray-300',
  dark: 'bg-gray-900 text-white hover:bg-gray-800 focus:ring-gray-700 shadow-sm hover:shadow-md active:shadow-sm border border-gray-900',
  gradient: 'bg-gradient-to-r from-primary-600 to-purple-600 text-white hover:from-primary-700 hover:to-purple-700 focus:ring-primary-500 shadow-md hover:shadow-lg active:shadow-sm border border-transparent',
}

const animationClasses = {
  none: '',
  scale: 'hover:scale-105 active:scale-95',
  slide: 'hover:-translate-y-0.5 active:translate-y-0',
  pulse: 'hover:animate-pulse',
}

const buttonClasses = computed(() => [
  sizeClasses[props.size],
  variantClasses[props.variant],
  animationClasses[props.animation],
  props.fullWidth ? 'w-full' : '',
  props.rounded ? roundedClasses[props.rounded] : '',
  'group', // For hover effects on child elements
])
</script>

<style scoped>
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>