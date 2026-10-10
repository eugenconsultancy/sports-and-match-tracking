<template>
  <div class="tabs-container">
    <!-- Tab Navigation -->
    <div :class="[variantClasses[variant].wrapper, fullWidth ? '' : '']">
      <nav :class="[variantClasses[variant].nav, fullWidth ? 'grid grid-cols-' + tabs.length : 'flex']">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="selectTab(tab)"
          :disabled="tab.disabled"
          :class="getTabClasses(tab)"
          class="group relative"
        >
          <!-- Tab Icon -->
          <span v-if="tab.icon" class="text-lg" :class="{ 'mr-1.5': $slots.default }">
            {{ tab.icon }}
          </span>

          <!-- Tab Label -->
          <span class="relative z-10">{{ tab.label }}</span>

          <!-- Tab Count Badge -->
          <span v-if="tab.count !== undefined" 
                class="ml-1.5 px-1.5 py-0.5 text-xs rounded-full transition-all duration-300"
                :class="modelValue === tab.id 
                  ? 'bg-primary-100 text-primary-700' 
                  : 'bg-gray-100 text-gray-500 group-hover:bg-gray-200'">
            {{ tab.count }}
          </span>

          <!-- Active Tab Indicator (Pill Style) -->
          <span v-if="variant === 'pills' && modelValue === tab.id" 
                class="absolute inset-0 bg-white shadow-sm rounded-lg"></span>

          <!-- Active Tab Indicator (Underline Style - Animated) -->
          <span v-if="variant === 'underline' && modelValue === tab.id" 
                class="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-600 rounded-full"></span>

          <!-- Notification Dot -->
          <span v-if="tab.notification" 
                class="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
        </button>
      </nav>
    </div>

    <!-- Tab Content with Transition -->
    <div class="mt-4 relative">
      <transition name="tab-fade" mode="out-in">
        <div :key="modelValue">
          <slot :activeTab="modelValue" />
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  tabs: { 
    type: Array, 
    required: true,
    validator: (tabs) => tabs.every(tab => tab.id && tab.label)
  },
  modelValue: { 
    type: String, 
    required: true 
  },
  variant: {
    type: String,
    default: 'underline',
    validator: (v) => ['underline', 'pills', 'boxed', 'minimal'].includes(v)
  },
  fullWidth: {
    type: Boolean,
    default: false
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v)
  },
  align: {
    type: String,
    default: 'left',
    validator: (v) => ['left', 'center'].includes(v)
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

function selectTab(tab) {
  if (!tab.disabled && tab.id !== props.modelValue) {
    emit('update:modelValue', tab.id)
    emit('change', tab)
  }
}

const variantClasses = {
  underline: {
    wrapper: 'border-b border-gray-200',
    nav: 'space-x-6 -mb-px'
  },
  pills: {
    wrapper: '',
    nav: 'space-x-1 bg-gray-100 p-1 rounded-xl'
  },
  boxed: {
    wrapper: 'border-b-2 border-gray-200',
    nav: 'space-x-1'
  },
  minimal: {
    wrapper: '',
    nav: 'space-x-4'
  }
}

const sizeClasses = {
  sm: 'pb-2 px-1 text-xs',
  md: 'pb-3 px-1.5 text-sm',
  lg: 'pb-4 px-2 text-base'
}

const alignClasses = {
  left: 'justify-start',
  center: 'justify-center'
}

function getTabClasses(tab) {
  const isActive = props.modelValue === tab.id
  const isDisabled = tab.disabled
  const variant = props.variant

  const baseClasses = [
    'font-medium transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded-md',
    sizeClasses[props.size],
    !props.fullWidth && alignClasses[props.align],
    isDisabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
  ]

  switch (variant) {
    case 'underline':
      return [
        ...baseClasses,
        'border-b-2 rounded-none',
        isActive 
          ? 'border-primary-600 text-primary-600' 
          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
      ]
    
    case 'pills':
      return [
        ...baseClasses,
        'relative px-4 py-2',
        isActive 
          ? 'text-primary-700' 
          : 'text-gray-500 hover:text-gray-700'
      ]
    
    case 'boxed':
      return [
        ...baseClasses,
        'border-2 border-b-0 rounded-t-lg px-4',
        isActive 
          ? 'border-gray-200 bg-white text-primary-600' 
          : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50'
      ]
    
    case 'minimal':
      return [
        ...baseClasses,
        'rounded-none border-b-0',
        isActive 
          ? 'text-primary-600 font-bold' 
          : 'text-gray-400 hover:text-gray-600'
      ]
    
    default:
      return baseClasses
  }
}
</script>

<style scoped>
/* Tab Content Transitions */
.tab-fade-enter-active,
.tab-fade-leave-active {
  transition: all 0.2s ease;
}

.tab-fade-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.tab-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Grid columns for full width tabs */
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
.grid-cols-5 { grid-template-columns: repeat(5, 1fr); }
.grid-cols-6 { grid-template-columns: repeat(6, 1fr); }
.grid-cols-7 { grid-template-columns: repeat(7, 1fr); }
.grid-cols-8 { grid-template-columns: repeat(8, 1fr); }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>