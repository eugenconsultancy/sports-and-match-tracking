<template>
  <div class="relative" ref="dropdownRef">
    <button @click="isOpen = !isOpen" class="relative p-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
      </svg>
      <span v-if="unreadCount > 0"
            class="absolute -top-1 -right-1 bg-red-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </span>
    </button>
    
    <!-- Dropdown -->
    <Transition name="dropdown">
      <div v-if="isOpen" class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
        <div class="p-3 border-b border-gray-100 flex items-center justify-between">
          <h3 class="font-semibold text-gray-900">Notifications</h3>
          <button v-if="unreadCount > 0" @click="markAllRead"
                  class="text-xs text-primary-600 hover:text-primary-700">
            Mark all as read
          </button>
        </div>
        
        <div class="max-h-96 overflow-y-auto">
          <div v-if="notifications.length === 0" class="p-4 text-center text-gray-500">
            No notifications
          </div>
          <div v-for="notif in notifications" :key="notif.id"
               class="p-3 border-b border-gray-100 hover:bg-gray-50 cursor-pointer transition-colors"
               :class="{ 'bg-primary-50': notif.delivery_status !== 'read' }"
               @click="markRead(notif.id)">
            <p class="text-sm font-medium text-gray-900">{{ notif.notification?.title }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ notif.notification?.body }}</p>
            <p class="text-xs text-gray-400 mt-1">{{ formatRelativeTime(notif.created_at) }}</p>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useNotificationStore } from '@/stores/notifications'
import { formatRelativeTime } from '@/utils/formatters'

const notificationStore = useNotificationStore()
const isOpen = ref(false)
const dropdownRef = ref(null)

const notifications = computed(() => notificationStore.notifications)
const unreadCount = computed(() => notificationStore.unreadCount)

function handleClickOutside(event) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

async function markAllRead() {
  await notificationStore.markAllRead()
}

async function markRead(id) {
  await notificationStore.markRead(id)
}

onMounted(() => {
  if (notificationStore.isAuthenticated) {
    notificationStore.fetchNotifications()
    notificationStore.fetchUnreadCount()
    document.addEventListener('click', handleClickOutside)
  }
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