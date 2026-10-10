<template>
  <div class="space-y-8 max-w-6xl mx-auto">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-16">
      <div class="text-center">
        <div class="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-gray-500 animate-pulse">Loading competition data...</p>
      </div>
    </div>

    <!-- Competition Content -->
    <div v-else-if="competition" class="space-y-8">
      <!-- Enhanced Competition Header -->
      <div class="relative overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 rounded-2xl p-8 text-white shadow-xl">
        <!-- Background Pattern -->
        <div class="absolute inset-0 opacity-10">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(120,119,198,0.3),rgba(255,255,255,0))]"></div>
          <div class="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-primary-500/20 to-transparent rounded-full blur-3xl"></div>
        </div>

        <div class="relative z-10">
          <div class="flex flex-col lg:flex-row items-center gap-8">
            <!-- Competition Logo -->
            <div class="relative">
              <div class="w-32 h-32 bg-white/10 backdrop-blur rounded-2xl p-3 flex items-center justify-center hover:bg-white/20 transition-all duration-300 transform hover:scale-105">
                <img v-if="competition.logo_url" :src="competition.logo_url" :alt="competition.name" 
                     class="w-24 h-24 object-contain" />
                <div v-else class="w-24 h-24 bg-white/10 rounded-xl flex items-center justify-center text-4xl font-bold text-white/30">
                  {{ competition.name.charAt(0) }}
                </div>
              </div>
              <!-- Status Indicator -->
              <div v-if="competition.is_active" class="absolute -top-2 -right-2 w-6 h-6 bg-green-500 rounded-full border-4 border-gray-900 animate-pulse"></div>
            </div>

            <!-- Competition Info -->
            <div class="flex-1 text-center lg:text-left">
              <h1 class="text-3xl lg:text-4xl font-bold mb-4 tracking-tight">{{ competition.name }}</h1>
              
              <div class="flex flex-wrap items-center justify-center lg:justify-start gap-3 mb-4">
                <span class="px-4 py-1.5 bg-white/10 backdrop-blur rounded-full text-sm font-medium flex items-center gap-2">
                  <span class="text-lg">{{ competition.competition_type === 'league' ? '🏆' : '🏅' }}</span>
                  {{ competition.competition_type }}
                </span>
                <span class="px-4 py-1.5 bg-white/10 backdrop-blur rounded-full text-sm font-medium flex items-center gap-2">
                  <span>🌍</span>
                  {{ competition.country }}
                </span>
                <span v-if="competition.is_active" class="px-4 py-1.5 bg-green-500/20 backdrop-blur rounded-full text-sm font-medium flex items-center gap-2">
                  <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                  Active
                </span>
                <span class="px-4 py-1.5 bg-white/10 backdrop-blur rounded-full text-sm font-medium">
                  Tier {{ competition.tier }}
                </span>
              </div>

              <!-- Quick Stats -->
              <div class="flex gap-4 justify-center lg:justify-start">
                <div class="bg-white/10 backdrop-blur rounded-xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300">
                  <div class="text-2xl font-bold">{{ teams.length }}</div>
                  <div class="text-xs text-white/70">Teams</div>
                </div>
                <div class="bg-white/10 backdrop-blur rounded-xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300">
                  <div class="text-2xl font-bold">{{ seasons.length }}</div>
                  <div class="text-xs text-white/70">Seasons</div>
                </div>
                <div class="bg-white/10 backdrop-blur rounded-xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300">
                  <div class="text-2xl font-bold">{{ activeSeason?.match_count || 0 }}</div>
                  <div class="text-xs text-white/70">Matches</div>
                </div>
              </div>
            </div>

            <!-- Favorite Button -->
            <button @click="toggleFavorite" 
                    class="p-4 rounded-2xl transition-all duration-300 transform hover:scale-110"
                    :class="isFavorited ? 'bg-red-500 text-white shadow-lg shadow-red-500/30' : 'bg-white/10 text-white/70 hover:bg-white/20'">
              <svg class="w-8 h-8" :fill="isFavorited ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Enhanced Season Selector -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-4">
        <div class="flex items-center gap-2 mb-3">
          <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span class="text-sm font-medium text-gray-700">Select Season</span>
        </div>
        <div class="flex gap-2 overflow-x-auto pb-2 custom-scrollbar">
          <button v-for="season in seasons" :key="season.id"
                  @click="selectedSeasonId = season.id; loadSeasonData()"
                  class="group relative px-6 py-3 rounded-xl text-sm font-semibold transition-all duration-300 whitespace-nowrap flex items-center gap-2"
                  :class="selectedSeasonId === season.id 
                    ? 'bg-primary-600 text-white shadow-lg shadow-primary-500/30 transform scale-105' 
                    : 'bg-gray-50 text-gray-600 hover:bg-gray-100 hover:shadow-md'">
            {{ season.name }}
            <span v-if="season.is_current" 
                  class="px-2 py-0.5 bg-green-500/20 text-green-700 rounded-full text-xs font-bold"
                  :class="selectedSeasonId === season.id ? 'bg-green-400/30 text-green-200' : ''">
              CURRENT
            </span>
            <span v-if="selectedSeasonId === season.id" 
                  class="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-1.5 h-1.5 bg-primary-600 rounded-full">
            </span>
          </button>
        </div>
      </div>

      <!-- Enhanced Tabs -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        <!-- Tab Navigation -->
        <div class="border-b border-gray-100 bg-gray-50/50 p-2">
          <div class="flex gap-1">
            <button v-for="tab in tabs" :key="tab.id"
                    @click="activeTab = tab.id"
                    class="relative px-6 py-3 rounded-xl text-sm font-semibold transition-all duration-300 flex items-center gap-2"
                    :class="activeTab === tab.id 
                      ? 'bg-white text-primary-700 shadow-sm' 
                      : 'text-gray-500 hover:text-gray-700 hover:bg-white/50'">
              <span class="text-lg">{{ tab.icon }}</span>
              {{ tab.label }}
              <span v-if="getTabCount(tab.id)" 
                    class="ml-1 px-1.5 py-0.5 text-xs rounded-full"
                    :class="activeTab === tab.id ? 'bg-primary-100 text-primary-700' : 'bg-gray-200 text-gray-600'">
                {{ getTabCount(tab.id) }}
              </span>
            </button>
          </div>
        </div>

        <!-- Tab Content -->
        <div class="p-6">
          <!-- Standings Tab -->
          <div v-if="activeTab === 'standings'" class="space-y-6">
            <div v-if="standings.length > 0" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div v-for="standing in standings" :key="standing.id" 
                   class="group bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                <div class="bg-gradient-to-r from-primary-50 to-blue-50 p-5 border-b border-gray-100">
                  <div class="flex items-center justify-between">
                    <div>
                      <h3 class="font-bold text-gray-900 flex items-center gap-2">
                        {{ standing.stage_name }}
                        <span v-if="standing.group_name" class="text-sm font-normal text-gray-500 px-2 py-0.5 bg-white rounded-md">
                          {{ standing.group_name }}
                        </span>
                      </h3>
                      <p class="text-xs text-gray-500 mt-1">{{ standing.standing_type }}</p>
                    </div>
                    <div class="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                      <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                    </div>
                  </div>
                </div>
                <StandingsTable :standings="standing.team_standings" :title="''" :compact="true" />
              </div>
            </div>
            <div v-else class="text-center py-16">
              <div class="w-20 h-20 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-700 mb-1">No Standings Available</h3>
              <p class="text-gray-500 text-sm">Standings data for this season hasn't been published yet</p>
            </div>
          </div>

          <!-- Matches Tab -->
          <div v-if="activeTab === 'matches'" class="space-y-6">
            <!-- Match Rounds Filter -->
            <div class="flex items-center gap-2 mb-4">
              <div class="flex gap-1.5 overflow-x-auto pb-2 flex-1 custom-scrollbar">
                <button v-for="round in matchRounds" :key="round"
                        @click="selectedRound = round"
                        class="px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-300 whitespace-nowrap"
                        :class="selectedRound === round 
                          ? 'bg-primary-600 text-white shadow-md shadow-primary-500/20' 
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'">
                  Matchday {{ round }}
                </button>
              </div>
              <button v-if="filteredMatches.length > 0"
                      class="flex items-center gap-2 px-4 py-2 bg-green-50 text-green-700 rounded-xl text-sm font-semibold hover:bg-green-100 transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
                </svg>
                {{ filteredMatches.length }} matches
              </button>
            </div>
            
            <!-- Matches Grid -->
            <div v-if="filteredMatches.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="match in filteredMatches" :key="match.id"
                   class="group">
                <MatchWidget :match="match" 
                             class="hover:shadow-lg transition-all duration-300 hover:-translate-y-1" />
              </div>
            </div>
            <div v-else class="text-center py-16">
              <div class="w-20 h-20 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-700 mb-1">No Matches Found</h3>
              <p class="text-gray-500 text-sm">No matches scheduled for this round</p>
            </div>
          </div>

          <!-- Stats Tab -->
          <div v-if="activeTab === 'stats'" class="space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <!-- Top Scorers -->
              <div class="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-lg transition-all duration-300">
                <div class="bg-gradient-to-r from-orange-50 to-yellow-50 p-5 border-b border-gray-100">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-orange-100 rounded-xl flex items-center justify-center">
                      <span class="text-2xl">⚽</span>
                    </div>
                    <div>
                      <h3 class="font-bold text-gray-900">Top Scorers</h3>
                      <p class="text-xs text-gray-500">Leading goalscorers this season</p>
                    </div>
                  </div>
                </div>
                <div class="p-3">
                  <div v-if="topScorers.length > 0" class="space-y-2">
                    <div v-for="(player, idx) in topScorers.slice(0, 10)" :key="player.player_id"
                         class="group flex items-center justify-between p-3 rounded-xl hover:bg-gradient-to-r hover:from-orange-50 hover:to-yellow-50 cursor-pointer transition-all duration-300"
                         @click="$router.push(`/player/${player.player_id}`)">
                      <div class="flex items-center gap-3">
                        <span class="w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm"
                              :class="getRankColorClass(idx)">
                          {{ idx + 1 }}
                        </span>
                        <img v-if="player.player_image" :src="player.player_image" 
                             class="w-9 h-9 rounded-full object-cover border-2 border-gray-200 group-hover:border-primary-300 transition-colors" />
                        <div v-else class="w-9 h-9 rounded-full bg-primary-100 flex items-center justify-center text-xs font-bold text-primary-600">
                          {{ player.player_name.charAt(0) }}
                        </div>
                        <div>
                          <p class="font-medium group-hover:text-primary-600 transition-colors">{{ player.player_name }}</p>
                          <p class="text-xs text-gray-500">{{ player.team_name }}</p>
                        </div>
                      </div>
                      <div class="text-right">
                        <span class="text-xl font-bold text-orange-600">{{ player.goals }}</span>
                        <span class="text-xs text-gray-400 ml-1">goals</span>
                      </div>
                    </div>
                  </div>
                  <div v-else class="text-center py-8 text-gray-500">
                    No scorer data available
                  </div>
                </div>
              </div>

              <!-- Top Assisters -->
              <div class="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-lg transition-all duration-300">
                <div class="bg-gradient-to-r from-blue-50 to-purple-50 p-5 border-b border-gray-100">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
                      <span class="text-2xl">🎯</span>
                    </div>
                    <div>
                      <h3 class="font-bold text-gray-900">Top Assisters</h3>
                      <p class="text-xs text-gray-500">Leading assist providers</p>
                    </div>
                  </div>
                </div>
                <div class="p-3">
                  <div v-if="topAssisters.length > 0" class="space-y-2">
                    <div v-for="(player, idx) in topAssisters.slice(0, 10)" :key="player.player_id"
                         class="group flex items-center justify-between p-3 rounded-xl hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 cursor-pointer transition-all duration-300"
                         @click="$router.push(`/player/${player.player_id}`)">
                      <div class="flex items-center gap-3">
                        <span class="w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm"
                              :class="getRankColorClass(idx)">
                          {{ idx + 1 }}
                        </span>
                        <img v-if="player.player_image" :src="player.player_image" 
                             class="w-9 h-9 rounded-full object-cover border-2 border-gray-200 group-hover:border-blue-300 transition-colors" />
                        <div v-else class="w-9 h-9 rounded-full bg-blue-100 flex items-center justify-center text-xs font-bold text-blue-600">
                          {{ player.player_name.charAt(0) }}
                        </div>
                        <div>
                          <p class="font-medium group-hover:text-blue-600 transition-colors">{{ player.player_name }}</p>
                          <p class="text-xs text-gray-500">{{ player.team_name }}</p>
                        </div>
                      </div>
                      <div class="text-right">
                        <span class="text-xl font-bold text-blue-600">{{ player.assists }}</span>
                        <span class="text-xs text-gray-400 ml-1">assists</span>
                      </div>
                    </div>
                  </div>
                  <div v-else class="text-center py-8 text-gray-500">
                    No assist data available
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Teams Tab -->
          <div v-if="activeTab === 'teams'">
            <div v-if="teams.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
              <div v-for="team in teams" :key="team.id"
                   class="group bg-white rounded-xl border border-gray-200 p-4 text-center hover:shadow-lg transition-all duration-300 hover:-translate-y-1 cursor-pointer"
                   @click="$router.push(`/team/${team.id}`)">
                <div class="w-20 h-20 mx-auto mb-3 bg-gray-50 rounded-2xl p-2 flex items-center justify-center group-hover:bg-primary-50 transition-colors">
                  <img v-if="team.logo_url" :src="team.logo_url" :alt="team.name" 
                       class="w-16 h-16 object-contain group-hover:scale-110 transition-transform" />
                  <div v-else class="w-16 h-16 bg-gray-200 rounded-xl flex items-center justify-center text-xl font-bold text-gray-400">
                    {{ team.name.charAt(0) }}
                  </div>
                </div>
                <p class="font-semibold text-sm group-hover:text-primary-600 transition-colors line-clamp-2">{{ team.name }}</p>
              </div>
            </div>
            <div v-else class="text-center py-16">
              <div class="w-20 h-20 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-700 mb-1">No Teams Available</h3>
              <p class="text-gray-500 text-sm">Teams data not available for this season</p>
            </div>
          </div>

          <!-- News Tab -->
          <div v-if="activeTab === 'news'">
            <div v-if="news.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <NewsCard v-for="article in news" :key="article.id" :article="article" 
                        class="hover:shadow-lg transition-all duration-300 hover:-translate-y-1" />
            </div>
            <div v-else class="text-center py-16">
              <div class="w-20 h-20 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-700 mb-1">No News Available</h3>
              <p class="text-gray-500 text-sm">Latest news hasn't been published for this competition yet</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Not Found State -->
    <div v-else class="text-center py-16">
      <div class="w-32 h-32 bg-gradient-to-br from-gray-100 to-gray-200 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-lg">
        <span class="text-6xl">🏆</span>
      </div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">Competition Not Found</h2>
      <p class="text-gray-500 mb-6">This competition might have been removed or doesn't exist</p>
      <router-link to="/competitions" 
                   class="inline-flex items-center gap-2 px-6 py-2.5 bg-primary-600 text-white font-medium rounded-xl hover:bg-primary-700 transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5">
        Browse All Competitions
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
        </svg>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUIStore } from '@/stores/ui'
import { api } from '@/services/api'
import Badge from '@/components/ui/Badge.vue'
import MatchWidget from '@/components/MatchWidget.vue'
import StandingsTable from '@/components/StandingsTable.vue'
import NewsCard from '@/components/NewsCard.vue'

const route = useRoute()
const router = useRouter()
const uiStore = useUIStore()
const competitionId = route.params.id

const loading = ref(true)
const competition = ref(null)
const seasons = ref([])
const selectedSeasonId = ref(null)
const standings = ref([])
const matches = ref([])
const teams = ref([])
const news = ref([])
const topScorers = ref([])
const topAssisters = ref([])
const isFavorited = ref(false)
const activeTab = ref('standings')
const selectedRound = ref(1)

const tabs = [
  { id: 'standings', label: 'Standings', icon: '📊' },
  { id: 'matches', label: 'Matches', icon: '⚽' },
  { id: 'stats', label: 'Stats', icon: '📈' },
  { id: 'teams', label: 'Teams', icon: '👥' },
  { id: 'news', label: 'News', icon: '📰' },
]

const activeSeason = computed(() => {
  return seasons.value.find(s => s.id === selectedSeasonId.value)
})

const matchRounds = computed(() => {
  const rounds = new Set()
  matches.value.forEach(m => {
    if (m.round_number) rounds.add(m.round_number)
  })
  return Array.from(rounds).sort((a, b) => a - b)
})

const filteredMatches = computed(() => {
  if (selectedRound.value === -1) return matches.value
  return matches.value.filter(m => m.round_number === selectedRound.value)
})

function getTabCount(tabId) {
  switch(tabId) {
    case 'standings': return standings.value.length || null
    case 'matches': return matches.value.length || null
    case 'teams': return teams.value.length || null
    case 'news': return news.value.length || null
    default: return null
  }
}

function getRankColorClass(index) {
  if (index === 0) return 'bg-yellow-100 text-yellow-700 border-2 border-yellow-400'
  if (index === 1) return 'bg-gray-100 text-gray-600 border-2 border-gray-300'
  if (index === 2) return 'bg-orange-100 text-orange-700 border-2 border-orange-300'
  return 'bg-gray-50 text-gray-500 border border-gray-200'
}

async function loadCompetition() {
  try {
    competition.value = await api.getCompetition(competitionId)
  } catch (error) {
    console.error('Failed to load competition:', error)
    competition.value = null
  }
}

async function loadSeasons() {
  try {
    const response = await api.getCompetitionSeasons(competitionId)
    seasons.value = response.results || response || []
    const currentSeason = seasons.value.find(s => s.is_current)
    selectedSeasonId.value = currentSeason?.id || seasons.value[0]?.id
    if (selectedSeasonId.value) {
      await loadSeasonData()
    } else {
      loading.value = false
    }
  } catch (error) {
    console.error('Failed to load seasons:', error)
    seasons.value = []
    loading.value = false
  }
}

async function loadSeasonData() {
  if (!selectedSeasonId.value) return
  
  loading.value = true
  try {
    const [standingsRes, matchesRes, teamsRes, newsRes] = await Promise.all([
      api.getStandings({ competition_season: selectedSeasonId.value }),
      api.getMatches({ competition_season: selectedSeasonId.value, limit: 100 }),
      api.getTeams({ competition_season: selectedSeasonId.value }),
      api.getArticles({ by_entity: 'competition', id: competitionId, limit: 20 }),
    ])
    
    standings.value = standingsRes.results || standingsRes || []
    matches.value = matchesRes.results || matchesRes || []
    teams.value = teamsRes.results || teamsRes || []
    news.value = newsRes.results || newsRes || []
    
    // Auto-select first available round
    if (matchRounds.value.length > 0) {
      selectedRound.value = matchRounds.value[0]
    }
    
    // Load stats
    await Promise.all([
      loadTopScorers(),
      loadTopAssisters()
    ])
  } catch (error) {
    console.error('Failed to load season data:', error)
    standings.value = []
    matches.value = []
    teams.value = []
    news.value = []
  } finally {
    loading.value = false
  }
}

async function loadTopScorers() {
  try {
    const response = await api.getPlayers({ 
      competition_season: selectedSeasonId.value,
      ordering: '-goals',
      limit: 20 
    })
    const players = response.results || response || []
    topScorers.value = players.map(p => ({
      player_id: p.id,
      player_name: p.full_name,
      player_image: p.image_url,
      team_name: p.current_team_name,
      goals: p.season_stats?.[0]?.goals || 0,
    })).sort((a, b) => b.goals - a.goals).filter(p => p.goals > 0)
  } catch (error) {
    console.error('Failed to load top scorers:', error)
    topScorers.value = []
  }
}

async function loadTopAssisters() {
  try {
    const response = await api.getPlayers({ 
      competition_season: selectedSeasonId.value,
      ordering: '-assists',
      limit: 20 
    })
    const players = response.results || response || []
    topAssisters.value = players.map(p => ({
      player_id: p.id,
      player_name: p.full_name,
      player_image: p.image_url,
      team_name: p.current_team_name,
      assists: p.season_stats?.[0]?.assists || 0,
    })).sort((a, b) => b.assists - a.assists).filter(p => p.assists > 0)
  } catch (error) {
    console.error('Failed to load top assisters:', error)
    topAssisters.value = []
  }
}

function toggleFavorite() {
  isFavorited.value = !isFavorited.value
  uiStore.showSuccess(
    isFavorited.value ? 'Added to favorites!' : 'Removed from favorites',
    isFavorited.value ? '⭐' : ''
  )
  // API call to toggle favorite would go here
}

onMounted(() => {
  loadCompetition()
  loadSeasons()
})
</script>

<style scoped>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.custom-scrollbar::-webkit-scrollbar {
  height: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 20px;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  /* Add the standard property below */
  line-clamp: 2;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>