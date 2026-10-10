import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
    const isSidebarOpen = ref(false)
    const isSearchOpen = ref(false)
    const theme = ref(localStorage.getItem('theme') || 'light')
    const toasts = ref([])
    let nextToastId = 0

    function toggleSidebar() {
        isSidebarOpen.value = !isSidebarOpen.value
    }

    function openSearch() {
        isSearchOpen.value = true
        document.body.style.overflow = 'hidden'
    }

    function closeSearch() {
        isSearchOpen.value = false
        document.body.style.overflow = ''
    }

    function setTheme(newTheme) {
        theme.value = newTheme
        localStorage.setItem('theme', newTheme)
        if (newTheme === 'dark') {
            document.documentElement.classList.add('dark')
        } else {
            document.documentElement.classList.remove('dark')
        }
    }

    function addToast(message, type = 'info', title = '', duration = 3000) {
        const id = nextToastId++
        const toast = { id, title, message, type }
        toasts.value.push(toast)

        if (duration > 0) {
            setTimeout(() => removeToast(id), duration)
        }

        return id
    }

    function removeToast(id) {
        const index = toasts.value.findIndex(t => t.id === id)
        if (index !== -1) {
            toasts.value.splice(index, 1)
        }
    }

    function showSuccess(message, title = 'Success') {
        return addToast(message, 'success', title)
    }

    function showError(message, title = 'Error') {
        return addToast(message, 'error', title)
    }

    function showWarning(message, title = 'Warning') {
        return addToast(message, 'warning', title)
    }

    function showInfo(message, title = 'Info') {
        return addToast(message, 'info', title)
    }

    return {
        isSidebarOpen,
        isSearchOpen,
        theme,
        toasts,
        toggleSidebar,
        openSearch,
        closeSearch,
        setTheme,
        addToast,
        removeToast,
        showSuccess,
        showError,
        showWarning,
        showInfo,
    }
})