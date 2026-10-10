<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    
    <!-- Top Navbar -->
    <header class="fixed top-0 inset-x-0 z-40 backdrop-blur bg-white/80 border-b border-gray-200">
      <Navbar @toggle-sidebar="uiStore.toggleSidebar" />
    </header>

    <!-- Layout Body -->
    <div class="flex flex-1 pt-16">
      
      <!-- Sidebar (Desktop + Mobile Drawer) -->
      <transition name="slide">
        <aside
          v-if="uiStore.isSidebarOpen"
          class="fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 lg:static lg:translate-x-0"
        >
          <Sidebar @close="uiStore.closeSidebar" />
        </aside>
      </transition>

      <!-- Overlay (Mobile only) -->
      <div
        v-if="uiStore.isSidebarOpen"
        class="fixed inset-0 bg-black/30 z-40 lg:hidden"
        @click="uiStore.closeSidebar"
      ></div>

      <!-- Main Content -->
      <main class="flex-1 lg:pl-64">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>

        </div>

        <!-- Footer -->
        <footer class="border-t border-gray-200 mt-10 bg-white">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div class="flex flex-col md:flex-row items-center justify-between gap-3 text-sm text-gray-500">
              <p>
                © {{ year }} 
                <span class="font-medium text-gray-700">LiveScore</span>. 
                All rights reserved.
              </p>

              <div class="flex items-center gap-5">
                <a href="#" class="hover:text-primary-600 transition">About</a>
                <a href="#" class="hover:text-primary-600 transition">Privacy</a>
                <a href="#" class="hover:text-primary-600 transition">Terms</a>
                <a href="#" class="hover:text-primary-600 transition">Contact</a>
              </div>
            </div>
          </div>
        </footer>
      </main>
    </div>

    <!-- Toasts -->
    <div class="fixed bottom-4 right-4 z-50 space-y-3">
      <transition-group name="toast" tag="div">
        <Toast
          v-for="toast in uiStore.toasts"
          :key="toast.id"
          :toast="toast"
          @close="uiStore.removeToast(toast.id)"
        />
      </transition-group>
    </div>

    <!-- Global Search Modal -->
    <SearchModal
      v-if="uiStore.isSearchOpen"
      @close="uiStore.closeSearch"
    />
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import Navbar from '@/components/Navbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import Toast from '@/components/ui/Toast.vue'
import SearchModal from '@/components/SearchModal.vue'

import { useUIStore } from '@/stores/ui'
import { useAuthStore } from '@/stores/auth'
import { useMatchStore } from '@/stores/matches'

const uiStore = useUIStore()
const authStore = useAuthStore()
const matchStore = useMatchStore()

const year = computed(() => new Date().getFullYear())

onMounted(() => {
  authStore.checkAuth()
  matchStore.connectToLiveMatches()
})
</script>

<style scoped>
/* Fade (page transitions) */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(4px);
}

/* Sidebar slide */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.25s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}

/* Toast animation */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateY(10px) scale(0.95);
}
.toast-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.95);
}
</style>