<template>
  <div class="flex items-center justify-center" :class="[sizeClasses[size], fullPage ? 'min-h-screen' : '']">
    <div class="relative">
      <!-- Variant 1: Default Spinner -->
      <div v-if="variant === 'spinner'" class="relative">
        <!-- Outer Ring -->
        <div class="absolute inset-0 rounded-full border-4 border-primary-100 animate-pulse"></div>
        
        <!-- Spinning Ring -->
        <div class="animate-spin rounded-full border-4 border-transparent border-t-primary-600 border-r-primary-400" 
             :class="spinnerSizeClasses[size]" />
        
        <!-- Inner Dot (for lg size) -->
        <div v-if="size === 'lg'" 
             class="absolute inset-0 flex items-center justify-center">
          <div class="w-3 h-3 bg-primary-600 rounded-full animate-ping"></div>
        </div>
      </div>

      <!-- Variant 2: Dots -->
      <div v-else-if="variant === 'dots'" class="flex items-center gap-1.5">
        <div v-for="i in 3" :key="i" 
             class="rounded-full bg-primary-600 animate-bounce"
             :class="dotSizeClasses[size]"
             :style="{ animationDelay: `${i * 0.15}s` }" />
      </div>

      <!-- Variant 3: Pulse -->
      <div v-else-if="variant === 'pulse'" class="relative">
        <div class="rounded-full bg-primary-600 animate-ping opacity-75" 
             :class="spinnerSizeClasses[size]" />
        <div class="rounded-full bg-primary-600" 
             :class="spinnerSizeClasses[size]" />
      </div>

      <!-- Variant 4: Football -->
      <div v-else-if="variant === 'football'" class="relative">
        <div class="text-4xl animate-bounce" :class="iconSizeClasses[size]">
          <span class="inline-block animate-spin">⚽</span>
        </div>
        <div class="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-8 h-1 bg-gray-200 rounded-full animate-pulse blur-sm"></div>
      </div>

      <!-- Variant 5: Gradient Ring -->
      <div v-else-if="variant === 'gradient'" class="relative">
        <svg class="animate-spin" :class="spinnerSizeClasses[size]" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="url(#gradient)" stroke-width="4" fill="none" />
          <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#3B82F6" />
              <stop offset="50%" stop-color="#8B5CF6" />
              <stop offset="100%" stop-color="#EC4899" />
            </linearGradient>
          </defs>
        </svg>
      </div>

      <!-- Variant 6: Skeleton Pulse -->
      <div v-else-if="variant === 'skeleton'" class="space-y-2">
        <div class="flex items-center gap-3">
          <div class="rounded-full bg-gray-200 animate-pulse" 
               :class="skeletonCircleClasses[size]" />
          <div class="space-y-1.5">
            <div class="rounded-full bg-gray-200 animate-pulse" 
                 :class="skeletonLineClasses[size]" />
            <div class="rounded-full bg-gray-200 animate-pulse w-3/4" 
                 :class="skeletonLineClasses[size]" />
          </div>
        </div>
      </div>

      <!-- Text -->
      <div v-if="text" 
           class="text-center font-medium animate-pulse"
           :class="textSizeClasses[size]">
        {{ text }}
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  size: { 
    type: String, 
    default: 'md', 
    validator: (v) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(v) 
  },
  text: {
    type: String,
    default: ''
  },
  fullPage: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String,
    default: 'spinner',
    validator: (v) => ['spinner', 'dots', 'pulse', 'football', 'gradient', 'skeleton'].includes(v)
  }
})

const sizeClasses = {
  xs: 'p-1',
  sm: 'p-2',
  md: 'p-4',
  lg: 'p-6',
  xl: 'p-8',
}

const spinnerSizeClasses = {
  xs: 'w-4 h-4',
  sm: 'w-6 h-6',
  md: 'w-10 h-10',
  lg: 'w-16 h-16',
  xl: 'w-20 h-20',
}

const dotSizeClasses = {
  xs: 'w-1.5 h-1.5',
  sm: 'w-2 h-2',
  md: 'w-3 h-3',
  lg: 'w-4 h-4',
  xl: 'w-5 h-5',
}

const iconSizeClasses = {
  xs: 'text-lg',
  sm: 'text-2xl',
  md: 'text-3xl',
  lg: 'text-5xl',
  xl: 'text-6xl',
}

const textSizeClasses = {
  xs: 'text-xs mt-1',
  sm: 'text-xs mt-1.5',
  md: 'text-sm mt-2',
  lg: 'text-base mt-3',
  xl: 'text-lg mt-4',
}

const skeletonCircleClasses = {
  xs: 'w-6 h-6',
  sm: 'w-8 h-8',
  md: 'w-10 h-10',
  lg: 'w-12 h-12',
  xl: 'w-16 h-16',
}

const skeletonLineClasses = {
  xs: 'h-1.5 w-20',
  sm: 'h-2 w-24',
  md: 'h-2.5 w-32',
  lg: 'h-3 w-40',
  xl: 'h-4 w-48',
}
</script>

<style scoped>
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.animate-bounce {
  animation: bounce 0.6s ease-in-out infinite;
}

.animate-ping {
  animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>