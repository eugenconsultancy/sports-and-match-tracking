<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto px-4 py-8 space-y-8">
      <!-- Enhanced Hero Header -->
      <div class="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-indigo-800 rounded-2xl p-8 text-white shadow-xl">
        <!-- Background Pattern -->
        <div class="absolute inset-0 opacity-10">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(255,255,255,0.3),rgba(255,255,255,0))]"></div>
          <div class="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-yellow-500/20 to-transparent rounded-full blur-3xl"></div>
          <div class="absolute bottom-0 left-0 w-64 h-64 bg-gradient-to-tr from-purple-500/20 to-transparent rounded-full blur-3xl"></div>
        </div>

        <div class="relative z-10">
          <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            <div>
              <div class="flex items-center gap-3 mb-2">
                <div class="w-12 h-12 bg-white/10 backdrop-blur rounded-2xl flex items-center justify-center">
                  <span class="text-3xl">🏆</span>
                </div>
                <div>
                  <h1 class="text-3xl sm:text-4xl font-bold tracking-tight">Competitions</h1>
                  <p class="text-white/70 text-sm">Explore leagues and tournaments from around the world</p>
                </div>
              </div>
            </div>

            <!-- Quick Stats -->
            <div class="flex gap-3">
              <div class="bg-white/10 backdrop-blur rounded-2xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer">
                <div class="text-2xl font-bold">{{ competitions.length }}</div>
                <div class="text-xs text-white/70">Total</div>
              </div>
              <div class="bg-white/10 backdrop-blur rounded-2xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer">
                <div class="text-2xl font-bold">{{ liveCount }}</div>
                <div class="text-xs text-white/70">Live Now</div>
              </div>
              <div class="bg-white/10 backdrop-blur rounded-2xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer">
                <div class="text-2xl font-bold">{{ countries.length }}</div>
                <div class="text-xs text-white/70">Countries</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Enhanced Search & Filters -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
        <div class="flex flex-col lg:flex-row gap-4">
          <!-- Search Input -->
          <div class="flex-1 relative group">
            <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-primary-500 transition-colors"
                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input v-model="searchQuery"
                   type="text"
                   placeholder="Search by name, country, or league..."
                   class="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 text-sm" />
            <button v-if="searchQuery" 
                    @click="searchQuery = ''"
                    class="absolute right-3 top-1/2 -translate-y-1/2 p-1 hover:bg-gray-100 rounded-full transition-colors">
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Type Filter -->
          <select v-model="typeFilter"
                  class="px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 text-sm bg-white">
            <option value="">All Types</option>
            <option value="league">🏆 League</option>
            <option value="cup">🏅 Cup</option>
            <option value="international">🌍 International</option>
          </select>

          <!-- Country Filter -->
          <select v-model="countryFilter"
                  class="px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 text-sm bg-white min-w-[150px]">
            <option value="">All Countries</option>
            <option v-for="country in countries" :key="country" :value="country">{{ country }}</option>
          </select>

          <!-- Clear Filters Button -->
          <button v-if="searchQuery || typeFilter || countryFilter"
                  @click="clearFilters"
                  class="px-4 py-3 text-sm font-medium text-red-600 hover:bg-red-50 rounded-xl transition-all duration-300 flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            Clear Filters
          </button>
        </div>

        <!-- Active Filters Display -->
        <div v-if="searchQuery || typeFilter || countryFilter" class="mt-4 flex items-center gap-2 text-sm">
          <span class="text-gray-500">Active filters:</span>
          <span v-if="searchQuery" class="px-3 py-1 bg-primary-50 text-primary-700 rounded-lg text-xs font-medium">
            Search: "{{ searchQuery }}"
          </span>
          <span v-if="typeFilter" class="px-3 py-1 bg-blue-50 text-blue-700 rounded-lg text-xs font-medium capitalize">
            {{ typeFilter }}
          </span>
          <span v-if="countryFilter" class="px-3 py-1 bg-green-50 text-green-700 rounded-lg text-xs font-medium">
            {{ countryFilter }}
          </span>
          <span class="text-gray-400 text-xs ml-auto">
            {{ filteredCompetitions.length }} result{{ filteredCompetitions.length !== 1 ? 's' : '' }}
          </span>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        <div v-for="i in 10" :key="i" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 animate-pulse">
          <div class="w-20 h-20 bg-gray-200 rounded-2xl mx-auto mb-4"></div>
          <div class="h-4 bg-gray-200 rounded-full w-3/4 mx-auto mb-2"></div>
          <div class="h-3 bg-gray-200 rounded-full w-1/2 mx-auto mb-3"></div>
          <div class="flex justify-center gap-2">
            <div class="h-5 bg-gray-200 rounded-full w-16"></div>
            <div class="h-5 bg-gray-200 rounded-full w-12"></div>
          </div>
        </div>
      </div>

      <!-- Competition Grid -->
      <div v-else-if="filteredCompetitions.length > 0"
           class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        <div v-for="comp in filteredCompetitions" :key="comp.id"
             class="group relative bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
             @click="$router.push(`/competition/${comp.id}`)">
          
          <!-- Top Gradient Bar -->
          <div class="h-1.5 w-full bg-gradient-to-r opacity-80 group-hover:opacity-100 transition-opacity"
               :style="{ backgroundImage: `linear-gradient(to right, ${comp.primary_color || '#3b82f6'}, ${comp.secondary_color || '#8b5cf6'})` }">
          </div>

          <!-- Card Content -->
          <div class="p-5">
            <!-- Logo Section -->
            <div class="relative mb-4">
              <div class="w-20 h-20 mx-auto relative">
                <!-- Background Glow -->
                <div class="absolute inset-0 bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl group-hover:scale-110 transition-transform duration-300"
                     :style="{ boxShadow: `0 0 20px ${comp.primary_color || '#3b82f6'}10` }">
                </div>
                
                <!-- Logo Image -->
                <div class="relative w-full h-full rounded-2xl p-2 flex items-center justify-center">
                  <img v-if="comp.logo_url"
                       :src="comp.logo_url"
                       :alt="comp.name"
                       class="w-16 h-16 object-contain relative z-10 group-hover:scale-110 transition-transform duration-300" />
                  <div v-else
                       class="w-16 h-16 rounded-xl flex items-center justify-center text-2xl font-bold text-white relative z-10 shadow-lg"
                       :style="{ backgroundColor: comp.primary_color || '#3b82f6' }">
                    {{ comp.name?.charAt(0) }}
                  </div>
                </div>

                <!-- Live Season Indicator -->
                <div v-if="comp.current_season?.status === 'live' || comp.is_active" 
                     class="absolute -top-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-white flex items-center justify-center shadow-sm">
                  <span class="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>
                </div>
              </div>
            </div>

            <!-- Competition Info -->
            <div class="text-center">
              <!-- Name -->
              <h3 class="font-bold text-gray-900 group-hover:text-primary-600 transition-colors line-clamp-2 mb-2 text-sm leading-tight">
                {{ comp.name }}
              </h3>
              
              <!-- Country -->
              <p class="text-xs text-gray-500 flex items-center justify-center gap-1 mb-3">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064" />
                </svg>
                {{ comp.country || 'International' }}
              </p>

              <!-- Badges -->
              <div class="flex items-center justify-center gap-2 flex-wrap">
                <span class="px-2.5 py-1 rounded-full text-xs font-semibold"
                      :class="getTypeClasses(comp.competition_type)">
                  {{ formatType(comp.competition_type) }}
                </span>
                <span class="px-2.5 py-1 bg-gray-100 text-gray-600 rounded-full text-xs font-semibold">
                  T{{ comp.tier }}
                </span>
              </div>
            </div>

            <!-- Quick Stats -->
            <div v-if="comp.teams_count || comp.matches_count" 
                 class="mt-4 pt-4 border-t border-gray-100">
              <div class="grid grid-cols-2 gap-3">
                <div v-if="comp.teams_count" class="text-center">
                  <p class="text-lg font-bold text-gray-900">{{ comp.teams_count }}</p>
                  <p class="text-xs text-gray-500">Teams</p>
                </div>
                <div v-if="comp.matches_count" class="text-center">
                  <p class="text-lg font-bold text-gray-900">{{ comp.matches_count }}</p>
                  <p class="text-xs text-gray-500">Matches</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Hover Overlay -->
          <div class="absolute inset-0 bg-gradient-to-t from-primary-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none rounded-2xl"></div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-16">
        <div class="w-32 h-32 bg-gradient-to-br from-gray-100 to-gray-200 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-lg">
          <span class="text-6xl">🔍</span>
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-3">No Competitions Found</h3>
        <p class="text-gray-500 mb-6 max-w-md mx-auto">
          We couldn't find any competitions matching your criteria. Try adjusting your search terms or filters.
        </p>
        <button @click="clearFilters" 
                class="inline-flex items-center gap-2 px-6 py-2.5 bg-primary-600 text-white font-medium rounded-xl hover:bg-primary-700 transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Clear All Filters
        </button>
      </div>

      <!-- Load More Button -->
      <div v-if="hasMore && filteredCompetitions.length > 0" class="text-center">
        <button @click="loadMore" 
                class="group inline-flex items-center gap-2 px-8 py-3 bg-white border-2 border-gray-200 text-gray-700 font-medium rounded-xl hover:border-primary-300 hover:text-primary-600 hover:shadow-lg transition-all duration-300"
                :disabled="loadingMore">
          <span v-if="loadingMore" class="flex items-center gap-2">
            <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Loading...
          </span>
          <span v-else class="flex items-center gap-2">
            Load More Competitions
            <svg class="w-5 h-5 group-hover:translate-y-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from '@/axios'

const loading = ref(true)
const loadingMore = ref(false)
const competitions = ref([])
const searchQuery = ref('')
const typeFilter = ref('')
const countryFilter = ref('')
const page = ref(1)
const hasMore = ref(false)

const countries = computed(() => {
  const all = competitions.value.map(c => c.country).filter(Boolean)
  return [...new Set(all)].sort()
})

const liveCount = computed(() => {
  return competitions.value.filter(c => 
    c.current_season?.status === 'live' || c.is_active
  ).length
})

const filteredCompetitions = computed(() => {
  let result = competitions.value

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(c =>
      c.name?.toLowerCase().includes(q) ||
      c.short_name?.toLowerCase().includes(q) ||
      c.country?.toLowerCase().includes(q)
    )
  }

  if (typeFilter.value) {
    result = result.filter(c => c.competition_type === typeFilter.value)
  }

  if (countryFilter.value) {
    result = result.filter(c => c.country === countryFilter.value)
  }

  return result
})

function getTypeClasses(type) {
  const classes = {
    league: 'bg-blue-50 text-blue-700',
    cup: 'bg-orange-50 text-orange-700',
    international: 'bg-purple-50 text-purple-700',
  }
  return classes[type] || 'bg-gray-50 text-gray-700'
}

function formatType(type) {
  const formats = {
    league: 'League',
    cup: 'Cup',
    international: 'Intl',
  }
  return formats[type] || type
}

function clearFilters() {
  searchQuery.value = ''
  typeFilter.value = ''
  countryFilter.value = ''
}

async function fetchCompetitions(pageNum = 1) {
  try {
    const res = await axios.get('/api/v1/competitions/competitions/', {
      params: { is_active: true, page: pageNum, page_size: 20 }
    })
    const data = res.data

    if (pageNum === 1) {
      competitions.value = data.results || data
    } else {
      competitions.value = [...competitions.value, ...(data.results || data)]
    }

    hasMore.value = data.next !== null
    page.value = pageNum
  } catch (error) {
    console.error('Failed to fetch competitions:', error)
  }
}

async function loadMore() {
  loadingMore.value = true
  await fetchCompetitions(page.value + 1)
  loadingMore.value = false
}

onMounted(async () => {
  await fetchCompetitions()
  loading.value = false
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  overflow: hidden;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>