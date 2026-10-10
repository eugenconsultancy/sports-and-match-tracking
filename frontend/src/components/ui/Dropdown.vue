<template>
  <div class="relative" ref="dropdownRef">
    <button @click="isOpen = !isOpen" class="flex items-center gap-2">
      <slot name="trigger" />
    </button>
    
    <Transition name="dropdown">
      <div v-if="isOpen" class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50">
        <slot />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isOpen = ref(false)
const dropdownRef = ref(null)

function handleClickOutside(event) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.dropdown-enter-from {
  opacity: 0;
  transform: translateY(-8px);
}
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>