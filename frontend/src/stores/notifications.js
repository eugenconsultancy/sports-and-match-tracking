import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from '@/axios'
import { useAuthStore } from './auth'

export const useNotificationStore = defineStore('notifications', () => {
    const authStore = useAuthStore()
    const notifications = ref([])
    const unreadCount = ref(0)
    const loading = ref(false)
    let wsConnection = null

    const isAuthenticated = computed(() => authStore.isAuthenticated)

    async function fetchNotifications(params = {}) {
        if (!authStore.isAuthenticated) return []

        loading.value = true
        try {
            const response = await axios.get('/api/v1/notifications/notifications/', { params })
            const data = response.data
            notifications.value = data.results || data || []
            return notifications.value
        } catch (error) {
            console.error('Failed to fetch notifications:', error)
            return []
        } finally {
            loading.value = false
        }
    }

    async function fetchUnreadCount() {
        if (!authStore.isAuthenticated) return 0

        try {
            const response = await axios.get('/api/v1/notifications/notifications/unread_count/')
            unreadCount.value = response.data.unread_count || 0
            return unreadCount.value
        } catch (error) {
            console.error('Failed to fetch unread count:', error)
            return 0
        }
    }

    async function markRead(notificationId) {
        try {
            await axios.post(`/api/v1/notifications/notifications/${notificationId}/mark_read/`)
            const notif = notifications.value.find(n => n.id === notificationId)
            if (notif) {
                notif.delivery_status = 'read'
                notif.read_at = new Date().toISOString()
            }
            await fetchUnreadCount()
            return true
        } catch (error) {
            console.error('Failed to mark notification as read:', error)
            return false
        }
    }

    async function markAllRead() {
        try {
            await axios.post('/api/v1/notifications/notifications/mark_all_read/')
            notifications.value.forEach(n => {
                if (n.delivery_status !== 'read') {
                    n.delivery_status = 'read'
                    n.read_at = new Date().toISOString()
                }
            })
            unreadCount.value = 0
            return true
        } catch (error) {
            console.error('Failed to mark all as read:', error)
            return false
        }
    }

    function connectWebSocket() {
        if (!authStore.isAuthenticated) return

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        const wsUrl = `${protocol}//localhost:8001/ws/notifications/${authStore.user?.id}`

        wsConnection = new WebSocket(wsUrl)

        wsConnection.onopen = () => {
            console.log('Connected to notifications WebSocket')
        }

        wsConnection.onmessage = (event) => {
            const data = JSON.parse(event.data)
            if (data.type === 'notification') {
                notifications.value.unshift(data.data)
                unreadCount.value++
            }
        }

        wsConnection.onclose = () => {
            setTimeout(() => connectWebSocket(), 5000)
        }
    }

    function disconnectWebSocket() {
        if (wsConnection) {
            wsConnection.close()
            wsConnection = null
        }
    }

    return {
        notifications,
        unreadCount,
        loading,
        isAuthenticated,
        fetchNotifications,
        fetchUnreadCount,
        markRead,
        markAllRead,
        connectWebSocket,
        disconnectWebSocket,
    }
})