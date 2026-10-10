<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto px-4 py-8 space-y-8">
      <!-- Enhanced Hero Header -->
      <div class="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-purple-800 rounded-2xl p-8 text-white shadow-xl">
        <!-- Background Pattern -->
        <div class="absolute inset-0 opacity-10">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(255,255,255,0.3),rgba(255,255,255,0))]"></div>
          <div class="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-yellow-500/20 to-transparent rounded-full blur-3xl"></div>
          <div class="absolute bottom-0 left-0 w-64 h-64 bg-gradient-to-tr from-pink-500/20 to-transparent rounded-full blur-3xl"></div>
        </div>

        <div class="relative z-10">
          <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            <div>
              <div class="flex items-center gap-3 mb-2">
                <div class="w-12 h-12 bg-white/10 backdrop-blur rounded-2xl flex items-center justify-center">
                  <svg class="w-7 h-7 text-yellow-300" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                  </svg>
                </div>
                <div>
                  <h1 class="text-3xl sm:text-4xl font-bold tracking-tight">My Favorites</h1>
                  <p class="text-white/70 text-sm">Your personalized football experience</p>
                </div>
              </div>
            </div>

            <!-- Quick Stats -->
            <div class="flex gap-3">
              <div class="bg-white/10 backdrop-blur rounded-2xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer">
                <div class="text-2xl font-bold">{{ favoriteTeams.length }}</div>
                <div class="text-xs text-white/70">Teams</div>
              </div>
              <div class="bg-white/10 backdrop-blur rounded-2xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer">
                <div class="text-2xl font-bold">{{ favoriteMatches.length }}</div>
                <div class="text-xs text-white/70">Matches</div>
              </div>
              <button v-if="authStore.isAuthenticated && (favoriteTeams.length > 0 || favoriteMatches.length > 0)"
                @click="refreshAll" 
                class="bg-white/10 backdrop-blur rounded-2xl px-4 py-3 hover:bg-white/20 transition-all duration-300 group"
                :disabled="refreshing">
                <svg class="w-5 h-5" :class="{ 'animate-spin': refreshing }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Not Authenticated - Enhanced -->
      <div v-if="!authStore.isAuthenticated" class="relative overflow-hidden bg-white rounded-2xl shadow-xl border border-gray-100">
        <div class="absolute inset-0 bg-gradient-to-br from-primary-50 to-purple-50 opacity-50"></div>
        <div class="relative z-10 text-center py-16 px-6">
          <div class="w-24 h-24 bg-gradient-to-br from-primary-100 to-purple-100 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-lg">
            <svg class="w-12 h-12 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 mb-3">Sign in to Your Favorites</h3>
          <p class="text-gray-600 mb-8 max-w-md mx-auto">
            Create your personalized football hub by saving your favorite teams, matches, and competitions for quick access.
          </p>
          
          <!-- Features List -->
          <div class="flex flex-wrap justify-center gap-6 mb-8">
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <span class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </span>
              Quick access to teams
            </div>
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <span class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </span>
              Live match tracking
            </div>
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <span class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </span>
              Personalized experience
            </div>
          </div>

          <router-link to="/login" 
                       class="inline-flex items-center gap-2 px-8 py-3 bg-primary-600 text-white font-bold rounded-xl hover:bg-primary-700 transition-all duration-300 hover:shadow-xl hover:-translate-y-0.5">
            Sign In Now
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
          <p class="mt-4 text-sm text-gray-500">
            Don't have an account? 
            <router-link to="/register" class="text-primary-600 hover:text-primary-700 font-medium">Create one here</router-link>
          </p>
        </div>
      </div>

      <!-- Authenticated Content -->
      <div v-else>
        <!-- Loading State -->
        <div v-if="loading" class="space-y-8">
          <!-- Teams Skeleton -->
          <div>
            <div class="h-8 bg-gray-200 rounded-full w-48 mb-4 animate-pulse"></div>
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
              <div v-for="i in 6" :key="i" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4 animate-pulse">
                <div class="w-16 h-16 bg-gray-200 rounded-full mx-auto mb-3"></div>
                <div class="h-4 bg-gray-200 rounded-full w-20 mx-auto mb-2"></div>
                <div class="h-3 bg-gray-200 rounded-full w-16 mx-auto"></div>
              </div>
            </div>
          </div>
          
          <!-- Matches Skeleton -->
          <div>
            <div class="h-8 bg-gray-200 rounded-full w-48 mb-4 animate-pulse"></div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="i in 3" :key="i" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 animate-pulse">
                <div class="h-3 bg-gray-200 rounded-full w-24 mb-6"></div>
                <div class="space-y-4">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 bg-gray-200 rounded-xl"></div>
                      <div class="h-4 bg-gray-200 rounded-full w-24"></div>
                    </div>
                    <div class="h-8 w-8 bg-gray-200 rounded-lg"></div>
                  </div>
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 bg-gray-200 rounded-xl"></div>
                      <div class="h-4 bg-gray-200 rounded-full w-24"></div>
                    </div>
                    <div class="h-8 w-8 bg-gray-200 rounded-lg"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="favoriteTeams.length === 0 && favoriteMatches.length === 0" class="text-center py-16">
          <div class="w-32 h-32 bg-gradient-to-br from-gray-100 to-gray-200 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-lg">
            <svg class="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 mb-3">No Favorites Yet</h3>
          <p class="text-gray-500 mb-8 max-w-md mx-auto">
            Start building your personalized football hub by following your favorite teams and matches. Click the star icon anywhere to add to your favorites!
          </p>
          
          <!-- Quick Start Guide -->
          <div class="flex flex-wrap justify-center gap-4 mb-8">
            <router-link to="/live" 
                         class="group flex items-center gap-3 px-6 py-4 bg-white rounded-xl shadow-sm border border-gray-200 hover:border-red-300 hover:shadow-md transition-all duration-300">
              <div class="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                <span class="text-2xl">🔴</span>
              </div>
              <div class="text-left">
                <p class="font-semibold text-gray-900">Live Matches</p>
                <p class="text-xs text-gray-500">Watch games in real-time</p>
              </div>
            </router-link>
            
            <router-link to="/competitions" 
                         class="group flex items-center gap-3 px-6 py-4 bg-white rounded-xl shadow-sm border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all duration-300">
              <div class="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                <span class="text-2xl">🏆</span>
              </div>
              <div class="text-left">
                <p class="font-semibold text-gray-900">Competitions</p>
                <p class="text-xs text-gray-500">Browse leagues & tournaments</p>
              </div>
            </router-link>
            
            <router-link to="/" 
                         class="group flex items-center gap-3 px-6 py-4 bg-white rounded-xl shadow-sm border border-gray-200 hover:border-green-300 hover:shadow-md transition-all duration-300">
              <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                <span class="text-2xl">⚽</span>
              </div>
              <div class="text-left">
                <p class="font-semibold text-gray-900">Today's Matches</p>
                <p class="text-xs text-gray-500">See scheduled games</p>
              </div>
            </router-link>
          </div>
        </div>

        <!-- Favorite Teams Section -->
        <section v-if="favoriteTeams.length > 0" class="space-y-6">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-3">
                <div class="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                Favorite Teams
                <span class="text-lg font-normal text-gray-400">({{ favoriteTeams.length }})</span>
              </h2>
            </div>
            <button v-if="favoriteTeams.length > 6" 
                    @click="showAllTeams = !showAllTeams" 
                    class="text-sm font-medium text-primary-600 hover:text-primary-700 transition-colors flex items-center gap-1 group">
              {{ showAllTeams ? 'Show less' : 'Show all' }}
              <svg class="w-4 h-4 transition-transform" :class="showAllTeams ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>
          
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
            <div v-for="fav in displayedTeams" :key="fav.id"
                 class="group bg-white rounded-2xl shadow-sm border border-gray-100 p-5 text-center hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer relative overflow-hidden"
                 @click="goToTeam(fav.team_id)">
              
              <!-- Hover Gradient -->
              <div class="absolute inset-0 bg-gradient-to-br from-primary-50 to-purple-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              
              <!-- Content -->
              <div class="relative z-10">
                <!-- Team Logo -->
                <div class="w-20 h-20 mx-auto mb-4 relative">
                  <div class="absolute inset-0 bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl group-hover:scale-110 transition-transform duration-300"></div>
                  <div class="relative w-full h-full rounded-2xl p-2 flex items-center justify-center">
                    <img v-if="fav.team_logo" :src="fav.team_logo" :alt="fav.team_name"
                         class="w-16 h-16 object-contain relative z-10 group-hover:scale-110 transition-transform duration-300" />
                    <div v-else class="w-16 h-16 bg-primary-100 rounded-xl flex items-center justify-center relative z-10">
                      <span class="text-2xl font-bold text-primary-600">{{ fav.team_name?.charAt(0) }}</span>
                    </div>
                  </div>
                  
                  <!-- Favorite Badge -->
                  <div class="absolute -top-1 -right-1 w-6 h-6 bg-yellow-400 rounded-full flex items-center justify-center shadow-lg">
                    <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                    </svg>
                  </div>
                </div>
                
                <!-- Team Info -->
                <h3 class="font-bold text-gray-900 group-hover:text-primary-600 transition-colors line-clamp-1">{{ fav.team_name }}</h3>
                
                <!-- Next Match Info -->
                <div v-if="fav.next_match" class="mt-2">
                  <div class="inline-flex items-center gap-1 px-2.5 py-1 bg-green-50 rounded-full text-xs font-medium text-green-700">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    Next: {{ formatDate(fav.next_match.kickoff_time) }}
                  </div>
                </div>
                <p v-else class="text-xs text-gray-400 mt-2">No upcoming matches</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Favorite Matches Section -->
        <section v-if="favoriteMatches.length > 0" class="space-y-6">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-3">
                <div class="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                Favorite Matches
                <span class="text-lg font-normal text-gray-400">({{ favoriteMatches.length }})</span>
              </h2>
            </div>
            <button v-if="favoriteMatches.length > 6" 
                    @click="showAllMatches = !showAllMatches" 
                    class="text-sm font-medium text-primary-600 hover:text-primary-700 transition-colors flex items-center gap-1 group">
              {{ showAllMatches ? 'Show less' : 'Show all' }}
              <svg class="w-4 h-4 transition-transform" :class="showAllMatches ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="fav in displayedMatches" :key="fav.id"
                 class="group">
              <MatchWidget :match="fav" 
                          class="hover:shadow-xl transition-all duration-300 hover:-translate-y-1" />
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { api } from '@/services/api'
import MatchWidget from '@/components/MatchWidget.vue'
import { formatDate } from '@/utils/formatters'

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()

const loading = ref(true)
const refreshing = ref(false)
const favoriteTeams = ref([])
const favoriteMatches = ref([])
const showAllTeams = ref(false)
const showAllMatches = ref(false)

const displayedTeams = computed(() => {
  if (showAllTeams.value) return favoriteTeams.value
  return favoriteTeams.value.slice(0, 6)
})

const displayedMatches = computed(() => {
  if (showAllMatches.value) return favoriteMatches.value
  return favoriteMatches.value.slice(0, 6)
})

async function loadFavorites() {
  if (!authStore.isAuthenticated) {
    loading.value = false
    return
  }
  
  loading.value = true
  try {
    const [teamsRes, matchesRes] = await Promise.all([
      api.getFavoriteTeams(),
      api.getFavoriteMatches(),
    ])
    
    favoriteTeams.value = teamsRes.results || teamsRes || []
    favoriteMatches.value = matchesRes.results || matchesRes || []
  } catch (error) {
    console.error('Failed to load favorites:', error)
    uiStore.showError('Failed to load favorites', 'Please try again')
  } finally {
    loading.value = false
  }
}

async function refreshAll() {
  refreshing.value = true
  try {
    await loadFavorites()
    uiStore.showSuccess('Favorites updated!', '')
  } catch (error) {
    console.error('Failed to refresh favorites:', error)
  } finally {
    refreshing.value = false
  }
}

function goToTeam(teamId) {
  router.push(`/team/${teamId}`)
}

onMounted(() => {
  loadFavorites()
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  line-clamp: 1;
  overflow: hidden;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>