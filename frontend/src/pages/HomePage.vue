<template>
  <div class="space-y-10">
    <!-- Hero Dashboard Section -->
    <section class="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 rounded-3xl p-8 text-white shadow-xl">
      <!-- Background Pattern -->
      <div class="absolute inset-0 opacity-10">
        <div class="absolute inset-0 bg-pattern-white"></div>
      </div>
      
      <div class="relative z-10">
        <!-- Welcome & Quick Stats -->
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 mb-8">
          <div>
            <h1 class="text-3xl sm:text-4xl font-bold mb-2">
              {{ greeting }}, {{ displayName }}
            </h1>
            <p class="text-white/80 text-lg">Your football world, live and personalized</p>
          </div>
          
          <!-- Quick Stats Dashboard -->
          <div class="flex gap-4">
            <div class="bg-white/10 backdrop-blur rounded-2xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer">
              <div class="text-2xl font-bold">{{ liveMatches.length }}</div>
              <div class="text-xs text-white/70">Live Matches</div>
            </div>
            <div class="bg-white/10 backdrop-blur rounded-2xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer">
              <div class="text-2xl font-bold">{{ todayMatches.length }}</div>
              <div class="text-xs text-white/70">Today's Games</div>
            </div>
            <div class="bg-white/10 backdrop-blur rounded-2xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer">
              <div class="text-2xl font-bold">{{ topCompetitions.length }}</div>
              <div class="text-xs text-white/70">Competitions</div>
            </div>
          </div>
        </div>
        
        <!-- Live Matches Ticker - Animated -->
        <div v-if="liveMatches.length > 0" class="mb-8">
          <div class="flex items-center gap-3 mb-4">
            <span class="live-indicator !bg-white"></span>
            <h2 class="text-xl font-bold flex items-center gap-2">
              Live Now
              <span class="text-sm font-normal text-white/70">({{ liveMatches.length }} matches)</span>
            </h2>
            <router-link to="/live" class="ml-auto text-sm text-white/80 hover:text-white transition-colors group flex items-center gap-1">
              View all 
              <svg class="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </router-link>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="match in liveMatches.slice(0, 3)" :key="match.id" 
                 class="group bg-white/10 backdrop-blur rounded-2xl p-4 cursor-pointer hover:bg-white/20 transition-all duration-300 hover:scale-[1.02] hover:shadow-lg"
                 @click="goToMatch(match.id)">
              <!-- Match Minute with Pulse -->
              <div class="flex items-center gap-2 mb-3">
                <span class="live-indicator"></span>
                <span class="text-xs font-semibold text-white/80">{{ match.minute || 0 }}'</span>
                <span class="text-xs text-white/60 ml-auto">{{ match.competition_name }}</span>
              </div>
              
              <!-- Teams -->
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-3 flex-1">
                  <img v-if="match.home_team_logo" :src="match.home_team_logo" class="w-9 h-9 object-contain group-hover:scale-110 transition-transform" />
                  <span class="font-semibold text-sm">{{ match.home_team_name }}</span>
                </div>
                <span class="text-2xl font-bold mx-3">{{ match.home_score }}</span>
              </div>
              
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3 flex-1">
                  <img v-if="match.away_team_logo" :src="match.away_team_logo" class="w-9 h-9 object-contain group-hover:scale-110 transition-transform" />
                  <span class="font-semibold text-sm">{{ match.away_team_name }}</span>
                </div>
                <span class="text-2xl font-bold mx-3">{{ match.away_score }}</span>
              </div>
              
              <!-- Match Events Indicator -->
              <div v-if="match.events && match.events.length" class="mt-3 flex gap-1">
                <span v-for="event in match.events.slice(0, 3)" :key="event.id"
                      class="w-2 h-2 rounded-full bg-yellow-400" 
                      :title="event.type">
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Empty State for Live Matches -->
        <div v-else class="text-center py-8 bg-white/5 rounded-2xl">
          <svg class="w-16 h-16 mx-auto mb-3 text-white/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          <p class="text-white/60 text-sm">No live matches right now</p>
          <p class="text-white/40 text-xs mt-1">Check back soon for live action</p>
        </div>
      </div>
    </section>

    <!-- Featured Polls Section - Enhanced -->
    <section v-if="featuredPolls.length > 0">
      <div class="flex items-center justify-between mb-5">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/20">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div>
            <h2 class="text-xl font-bold">Fan Polls</h2>
            <p class="text-xs text-gray-500">Have your say on the big football debates</p>
          </div>
        </div>
        <router-link to="/polls" class="text-sm font-medium text-primary-600 hover:text-primary-700 transition-colors group flex items-center gap-1">
          View all polls 
          <svg class="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </router-link>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <PollWidget v-for="poll in featuredPolls.slice(0, 2)" :key="poll.id" 
                    :poll-id="poll.id" :match-id="poll.match" :initial-data="poll"
                    class="hover:shadow-lg transition-shadow duration-300" />
      </div>
    </section>

    <!-- Today's Matches Section - Enhanced -->
    <section>
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-5">
        <div>
          <h2 class="text-xl font-bold flex items-center gap-2">
            Today's Matches
            <span class="text-sm font-normal text-gray-500">({{ todayMatches.length }})</span>
          </h2>
          <p class="text-xs text-gray-500 mt-1">{{ formattedDate }}</p>
        </div>
        
        <!-- Enhanced Filters -->
        <div class="flex gap-1.5 bg-gray-100 rounded-xl p-1 overflow-x-auto">
          <button v-for="filter in matchFilters" :key="filter.value"
                  @click="todayFilter = filter.value"
                  class="px-4 py-2 rounded-lg text-xs font-semibold whitespace-nowrap transition-all duration-200 flex items-center gap-1.5"
                  :class="todayFilter === filter.value 
                    ? 'bg-white text-primary-700 shadow-sm' 
                    : 'text-gray-600 hover:text-gray-900 hover:bg-white/50'">
            <span class="inline-block">{{ filter.icon }}</span>
            {{ filter.label }}
          </button>
        </div>
      </div>
      
      <!-- Loading State -->
      <div v-if="loadingToday" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <div v-for="i in 4" :key="i" class="card p-5">
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <Skeleton width="60px" height="xs" />
              <Skeleton width="80px" height="xs" />
            </div>
            <div class="flex justify-between items-center">
              <div class="flex items-center gap-3">
                <Skeleton width="32px" height="32px" variant="circle" />
                <Skeleton width="100px" height="sm" />
              </div>
              <Skeleton width="40px" height="lg" />
            </div>
            <div class="flex justify-between items-center">
              <div class="flex items-center gap-3">
                <Skeleton width="32px" height="32px" variant="circle" />
                <Skeleton width="100px" height="sm" />
              </div>
              <Skeleton width="40px" height="lg" />
            </div>
          </div>
        </div>
      </div>
      
      <!-- Matches Grid -->
      <div v-else-if="filteredTodayMatches.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <MatchWidget v-for="match in filteredTodayMatches" :key="match.id" :match="match" 
                     class="hover:shadow-md transition-all duration-300 hover:-translate-y-1" />
      </div>
      
      <!-- Empty State -->
      <div v-else class="card text-center py-12">
        <div class="max-w-sm mx-auto">
          <svg class="w-20 h-20 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <h3 class="text-lg font-semibold text-gray-700 mb-2">No Matches Scheduled</h3>
          <p class="text-gray-500 text-sm mb-6">There are no matches scheduled for today. Check out upcoming fixtures or browse competitions.</p>
          <div class="flex gap-3 justify-center">
            <router-link to="/competitions" class="btn-primary text-sm px-4 py-2">
              Browse Competitions
            </router-link>
            <router-link to="/live" class="btn-outline text-sm px-4 py-2">
              View Live
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Top Competitions with Standings Preview -->
    <section>
      <div class="flex items-center justify-between mb-5">
        <div>
          <h2 class="text-xl font-bold">Top Competitions</h2>
          <p class="text-xs text-gray-500 mt-1">Standings from major leagues</p>
        </div>
        <router-link to="/competitions" class="text-sm font-medium text-primary-600 hover:text-primary-700 transition-colors group flex items-center gap-1">
          View all 
          <svg class="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </router-link>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div v-for="comp in topCompetitions" :key="comp.id" 
             class="card overflow-hidden group hover:shadow-lg transition-all duration-300">
          <!-- Competition Header -->
          <div class="p-5 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white">
            <div class="flex items-center gap-3">
              <img v-if="comp.logo_url" :src="comp.logo_url" class="w-11 h-11 object-contain group-hover:scale-110 transition-transform" />
              <div class="flex-1">
                <h3 class="font-bold">{{ comp.name }}</h3>
                <p class="text-xs text-gray-500">{{ comp.country }} • {{ comp.competition_type }}</p>
              </div>
              <router-link :to="`/competition/${comp.id}`" 
                          class="px-3 py-1.5 text-xs font-medium text-primary-600 hover:bg-primary-50 rounded-lg transition-colors">
                View Details →
              </router-link>
            </div>
          </div>
          
          <!-- Standings Preview -->
          <div v-if="getCompetitionStandings(comp.id) && getCompetitionStandings(comp.id).length > 0">
            <StandingsTable :standings="getCompetitionStandings(comp.id)" :title="''" :compact="true" />
          </div>
          <div v-else class="p-8 text-center">
            <svg class="w-12 h-12 mx-auto mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p class="text-gray-400 text-sm">Standings not available yet</p>
            <router-link :to="`/competition/${comp.id}`" class="text-xs text-primary-600 hover:underline mt-1 inline-block">
              View competition details
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Latest News Section -->
    <section>
      <div class="flex items-center justify-between mb-5">
        <div>
          <h2 class="text-xl font-bold">Latest News</h2>
          <p class="text-xs text-gray-500 mt-1">Stay updated with football news</p>
        </div>
        <router-link to="/news" class="text-sm font-medium text-primary-600 hover:text-primary-700 transition-colors group flex items-center gap-1">
          View all 
          <svg class="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </router-link>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <NewsCard v-for="article in featuredNews" :key="article.id" :article="article" 
                  class="hover:shadow-lg transition-all duration-300 hover:-translate-y-1" />
      </div>
    </section>

    <!-- Top Scorers Section -->
    <section v-if="topScorers.length > 0">
      <div class="flex items-center justify-between mb-5">
        <div>
          <h2 class="text-xl font-bold flex items-center gap-2">
            <span class="text-2xl">⚽</span>
            Top Scorers
          </h2>
          <p class="text-xs text-gray-500 mt-1">Leading goalscorers this season</p>
        </div>
      </div>
      
      <div class="card overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="bg-gray-50 border-b border-gray-200">
                <th class="px-4 py-3 text-left w-12">#</th>
                <th class="px-4 py-3 text-left">Player</th>
                <th class="px-4 py-3 text-left">Team</th>
                <th class="px-4 py-3 text-center">Goals</th>
                <th class="px-4 py-3 text-center">Assists</th>
                <th class="px-4 py-3 text-center">Apps</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(scorer, idx) in topScorers.slice(0, 10)" :key="scorer.player_id"
                  class="cursor-pointer hover:bg-gray-50 transition-colors border-b border-gray-100 group"
                  @click="goToPlayer(scorer.player_id)">
                <td class="px-4 py-3">
                  <span class="font-bold text-primary-600 group-hover:scale-110 inline-block transition-transform">
                    {{ idx + 1 }}
                  </span>
                </td>
                <td class="px-4 py-3">
                  <div class="flex items-center gap-3">
                    <img v-if="scorer.player_image" :src="scorer.player_image" 
                         class="w-8 h-8 rounded-full object-cover border-2 border-gray-200" />
                    <div v-else class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center text-xs font-bold text-primary-600">
                      {{ scorer.player_name.charAt(0) }}
                    </div>
                    <span class="font-medium group-hover:text-primary-600 transition-colors">{{ scorer.player_name }}</span>
                  </div>
                </td>
                <td class="px-4 py-3 text-gray-600">{{ scorer.team_name }}</td>
                <td class="px-4 py-3 text-center">
                  <span class="font-bold text-green-600 bg-green-50 px-2 py-0.5 rounded-full">{{ scorer.goals }}</span>
                </td>
                <td class="px-4 py-3 text-center text-blue-600">{{ scorer.assists }}</td>
                <td class="px-4 py-3 text-center text-gray-500">{{ scorer.appearances }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMatchStore } from '@/stores/matches'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import { api } from '@/services/api'
import Skeleton from '@/components/ui/Skeleton.vue'
import MatchWidget from '@/components/MatchWidget.vue'
import NewsCard from '@/components/NewsCard.vue'
import PollWidget from '@/components/PollWidget.vue'
import StandingsTable from '@/components/StandingsTable.vue'

const router = useRouter()
const matchStore = useMatchStore()
const authStore = useAuthStore()
const { liveMatches } = storeToRefs(matchStore)

const loadingToday = ref(true)
const todayMatches = ref([])
const featuredNews = ref([])
const topCompetitions = ref([])
const competitionStandings = ref({})
const featuredPolls = ref([])
const topScorers = ref([])
const todayFilter = ref('all')

const displayName = computed(() => {
  const user = authStore.user
  return user?.first_name || 'Football Fan'
})

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good Morning'
  if (hour < 18) return 'Good Afternoon'
  return 'Good Evening'
})

const formattedDate = computed(() => {
  return new Date().toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
})

const matchFilters = [
  { label: 'All Matches', value: 'all', icon: '📋' },
  { label: 'Live', value: 'live', icon: '🔴' },
  { label: 'Upcoming', value: 'scheduled', icon: '⏰' },
]

const filteredTodayMatches = computed(() => {
  if (todayFilter.value === 'all') return todayMatches.value
  if (todayFilter.value === 'live') return todayMatches.value.filter(m => m.status === 'live' || m.status === 'half_time')
  return todayMatches.value.filter(m => m.status === 'scheduled')
})

function getCompetitionStandings(compId) {
  return competitionStandings.value[compId] || []
}

function goToMatch(matchId) {
  router.push(`/match/${matchId}`)
}

function goToPlayer(playerId) {
  router.push(`/player/${playerId}`)
}

async function loadTodayMatches() {
  loadingToday.value = true
  try {
    todayMatches.value = await matchStore.fetchTodayMatches()
  } catch (error) {
    console.error('Failed to load today matches:', error)
    todayMatches.value = []
  } finally {
    loadingToday.value = false
  }
}

async function loadFeaturedNews() {
  try {
    const response = await api.getFeaturedNews()
    featuredNews.value = response.results || response || []
  } catch (error) {
    console.error('Failed to load news:', error)
    featuredNews.value = []
  }
}

async function loadTopCompetitions() {
  try {
    const response = await api.getCompetitions({ is_active: true, limit: 4 })
    topCompetitions.value = response.results || response || []
    
    for (const comp of topCompetitions.value) {
      try {
        const standings = await api.getCompetitionStandings(comp.id)
        if (standings && standings.length > 0) {
          competitionStandings.value[comp.id] = standings
        }
      } catch (e) {
        competitionStandings.value[comp.id] = []
      }
    }
  } catch (error) {
    console.error('Failed to load competitions:', error)
    topCompetitions.value = []
  }
}

async function loadFeaturedPolls() {
  try {
    const response = await api.getPolls({ is_featured: true, status: 'active', limit: 4 })
    featuredPolls.value = response.results || response || []
  } catch (error) {
    console.error('Failed to load polls:', error)
    featuredPolls.value = []
  }
}

async function loadTopScorers() {
  try {
    const response = await api.getPlayers({ ordering: '-goals', limit: 20 })
    const players = response.results || response || []
    topScorers.value = players.map(p => ({
      player_id: p.id,
      player_name: p.full_name,
      player_image: p.image_url,
      team_name: p.current_team_name,
      goals: p.season_stats?.[0]?.goals || 0,
      assists: p.season_stats?.[0]?.assists || 0,
      appearances: p.season_stats?.[0]?.appearances || 0,
    })).sort((a, b) => b.goals - a.goals).filter(p => p.goals > 0)
  } catch (error) {
    console.error('Failed to load top scorers:', error)
    topScorers.value = []
  }
}

onMounted(() => {
  loadTodayMatches()
  loadFeaturedNews()
  loadTopCompetitions()
  loadFeaturedPolls()
  loadTopScorers()
})
</script>

<style scoped>
.live-indicator {
  width: 8px;
  height: 8px;
  background-color: #ef4444;
  border-radius: 50%;
  display: inline-block;
  animation: pulse 2s infinite;
}

.btn-primary {
  @apply bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors duration-200 font-medium;
}

.btn-outline {
  @apply border-2 border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-gray-500 bg-white px-4 py-2 rounded-lg font-medium transition-colors duration-200;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
  100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

.bg-pattern-white {
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  background-repeat: repeat;
}
</style>