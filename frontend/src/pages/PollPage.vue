<template>
  <div class="space-y-8 max-w-4xl mx-auto">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-16">
      <div class="text-center">
        <div class="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-gray-500 animate-pulse">Loading poll...</p>
      </div>
    </div>

    <!-- Poll Content -->
    <div v-else-if="poll" class="space-y-8">
      <!-- Enhanced Back Button -->
      <button @click="$router.back()" 
              class="group flex items-center gap-2 text-gray-500 hover:text-primary-600 transition-all duration-300">
        <svg class="w-5 h-5 transform group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span class="font-medium">Back to Polls</span>
      </button>

      <!-- Match Info Card - Enhanced with Gradient -->
      <div class="relative overflow-hidden bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl p-8 text-white shadow-xl">
        <!-- Background Pattern -->
        <div class="absolute inset-0 opacity-5">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(120,119,198,0.3),rgba(255,255,255,0))]"></div>
        </div>
        
        <div class="relative z-10">
          <!-- Status Badge -->
          <div class="text-center mb-6">
            <span class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold"
                  :class="poll.status === 'active' ? 'bg-green-500/20 text-green-300' : 'bg-gray-500/20 text-gray-300'">
              <span v-if="poll.status === 'active'" class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
              {{ poll.status === 'active' ? 'LIVE POLL' : 'POLL CLOSED' }}
            </span>
          </div>

          <!-- Teams Display -->
          <div class="flex items-center justify-center gap-6 mb-6">
            <div class="text-center flex-1">
              <div class="w-24 h-24 mx-auto mb-3 bg-white/10 backdrop-blur rounded-2xl p-2 flex items-center justify-center hover:bg-white/20 transition-all duration-300">
                <img v-if="poll.match_info?.home_team_logo" :src="poll.match_info.home_team_logo" 
                     class="w-20 h-20 object-contain transform hover:scale-110 transition-transform" />
                <div v-else class="w-20 h-20 bg-white/10 rounded-xl flex items-center justify-center text-2xl font-bold">
                  {{ poll.match_info?.home_team?.charAt(0) || 'H' }}
                </div>
              </div>
              <p class="font-bold text-lg">{{ poll.match_info?.home_team }}</p>
            </div>
            
            <div class="flex flex-col items-center">
              <div class="text-3xl font-black text-white/30 mb-2">VS</div>
              <div class="w-12 h-12 bg-white/20 backdrop-blur rounded-full flex items-center justify-center">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                </svg>
              </div>
            </div>
            
            <div class="text-center flex-1">
              <div class="w-24 h-24 mx-auto mb-3 bg-white/10 backdrop-blur rounded-2xl p-2 flex items-center justify-center hover:bg-white/20 transition-all duration-300">
                <img v-if="poll.match_info?.away_team_logo" :src="poll.match_info.away_team_logo"
                     class="w-20 h-20 object-contain transform hover:scale-110 transition-transform" />
                <div v-else class="w-20 h-20 bg-white/10 rounded-xl flex items-center justify-center text-2xl font-bold">
                  {{ poll.match_info?.away_team?.charAt(0) || 'A' }}
                </div>
              </div>
              <p class="font-bold text-lg">{{ poll.match_info?.away_team }}</p>
            </div>
          </div>

          <!-- Match Details -->
          <div class="text-center space-y-1">
            <p class="text-white/70 font-medium">{{ poll.match_info?.competition_name }}</p>
            <p class="text-white/50 text-sm">{{ formatDate(poll.match_info?.kickoff_time) }} • {{ getMatchStatusLabel(poll.match_info?.status) }}</p>
          </div>
        </div>
      </div>

      <!-- Poll Voting Card - Enhanced -->
      <div class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
        <!-- Poll Header -->
        <div class="bg-gradient-to-r from-primary-50 to-blue-50 p-6 border-b border-gray-100">
          <div class="text-center">
            <h1 class="text-2xl font-bold text-gray-900 mb-3">{{ poll.question }}</h1>
            <div class="flex items-center justify-center gap-4 text-sm">
              <span class="flex items-center gap-1.5 text-gray-600">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span class="font-semibold">{{ totalVotes.toLocaleString() }}</span> total votes
              </span>
              <span v-if="poll.status === 'active'" class="flex items-center gap-1.5">
                <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                <span class="text-green-600 font-medium">Voting Open</span>
              </span>
            </div>
          </div>
        </div>

        <!-- Poll Options -->
        <div class="p-6 space-y-4">
          <div v-for="(option, index) in pollOptions" :key="option.id"
               @click="canVote && handleVote(option.id)"
               class="group relative overflow-hidden rounded-xl border-2 transition-all duration-300"
               :class="[
                 canVote ? 'hover:border-primary-300 hover:shadow-lg hover:-translate-y-0.5 cursor-pointer' : 'cursor-default',
                 userVote === option.id ? 'border-green-400 bg-green-50 shadow-md' : 'border-gray-200 bg-white',
                 isLeadingOption(option.id) && userVote !== option.id ? 'ring-2 ring-primary-200 ring-offset-2' : ''
               ]">
            
            <!-- Animated Background on Hover -->
            <div v-if="canVote" class="absolute inset-0 bg-gradient-to-r from-primary-50 to-blue-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            
            <!-- Selected Checkmark Animation -->
            <div v-if="userVote === option.id" class="absolute top-3 right-3 z-10">
              <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center animate-scale-in">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>

            <div class="relative z-10 p-5">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-4">
                  <!-- Rank Badge -->
                  <div class="w-10 h-10 rounded-lg flex items-center justify-center font-bold text-sm"
                       :class="getRankStyle(index)">
                    {{ getRankNumber(option.id) || index + 1 }}
                  </div>
                  
                  <!-- Option Content -->
                  <div>
                    <div class="flex items-center gap-2">
                      <span class="text-lg font-bold text-gray-900">{{ option.label }}</span>
                      <span v-if="isLeadingOption(option.id)" 
                            class="px-2 py-0.5 bg-yellow-100 text-yellow-700 rounded-full text-xs font-semibold flex items-center gap-1">
                        <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                        </svg>
                        Leading
                      </span>
                    </div>
                    <p class="text-sm text-gray-500 mt-0.5">{{ option.vote_count || 0 }} votes</p>
                  </div>
                </div>
                
                <!-- Percentage with Animation -->
                <div class="text-right">
                  <span class="text-3xl font-black text-primary-600">{{ option.percentage || 0 }}%</span>
                </div>
              </div>
              
              <!-- Enhanced Progress Bar -->
              <div class="relative h-4 bg-gray-100 rounded-full overflow-hidden">
                <!-- Background Pattern -->
                <div class="absolute inset-0 opacity-20" 
                     :style="{ backgroundImage: `repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(255,255,255,0.5) 5px, rgba(255,255,255,0.5) 10px)` }">
                </div>
                
                <!-- Fill Animation -->
                <div class="absolute inset-y-0 left-0 rounded-full transition-all duration-1000 ease-out"
                     :class="userVote === option.id ? 'bg-gradient-to-r from-green-400 to-green-500' : 'bg-gradient-to-r from-primary-500 to-primary-600'"
                     :style="{ width: `${option.percentage || 0}%` }">
                  
                  <!-- Shine Effect -->
                  <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shine"></div>
                </div>
              </div>
              
              <!-- Vote Count Bar -->
              <div class="flex justify-between items-center mt-2 text-sm">
                <span class="text-gray-500">{{ option.vote_count || 0 }} votes</span>
                <span class="font-semibold" :class="userVote === option.id ? 'text-green-600' : 'text-primary-600'">
                  {{ option.percentage || 0 }}%
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Messages -->
        <div class="p-6 border-t border-gray-100 bg-gray-50/50">
          <!-- User Not Authenticated -->
          <div v-if="!authStore.isAuthenticated && poll.status === 'active'" class="text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <p class="text-gray-700 font-medium mb-1">Want to have your say?</p>
            <p class="text-gray-500 text-sm mb-4">Sign in to cast your vote in this poll</p>
            <router-link to="/login" 
                        class="inline-flex items-center gap-2 px-6 py-2.5 bg-primary-600 text-white font-medium rounded-xl hover:bg-primary-700 transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5">
              Sign In to Vote
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </router-link>
          </div>
          
          <!-- User Has Voted -->
          <div v-else-if="userVote && poll.status === 'active'" class="text-center">
            <div class="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p class="text-green-700 font-medium">Thanks for voting! 🎉</p>
            <p class="text-green-600 text-sm mt-1">Your voice has been counted</p>
          </div>
          
          <!-- Poll Closed -->
          <div v-else-if="poll.status === 'closed'" class="text-center">
            <div class="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p class="text-gray-700 font-medium">This poll has ended</p>
            <p class="text-gray-500 text-sm mt-1">Check out other active polls</p>
            <router-link to="/polls" class="mt-3 inline-block text-primary-600 hover:text-primary-700 font-medium text-sm">
              Browse Polls →
            </router-link>
          </div>
        </div>
      </div>

      <!-- Share Section - Enhanced -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
        <div class="text-center mb-6">
          <h3 class="text-xl font-bold text-gray-900 mb-1">Share This Poll</h3>
          <p class="text-gray-500 text-sm">Let others join the conversation</p>
        </div>
        
        <div class="flex items-center justify-center gap-4">
          <!-- Twitter Share -->
          <button @click="sharePoll('twitter')" 
                  class="group flex items-center gap-2 px-5 py-3 bg-gray-900 text-white rounded-xl hover:bg-gray-800 transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
            </svg>
            <span class="font-medium">Twitter</span>
          </button>
          
          <!-- Facebook Share -->
          <button @click="sharePoll('facebook')" 
                  class="group flex items-center gap-2 px-5 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
            </svg>
            <span class="font-medium">Facebook</span>
          </button>
          
          <!-- Copy Link -->
          <button @click="copyLink" 
                  class="group flex items-center gap-2 px-5 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-all duration-300 hover:shadow-md hover:-translate-y-0.5">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
            <span class="font-medium">{{ copied ? 'Copied!' : 'Copy Link' }}</span>
          </button>
        </div>
        
        <!-- Copy Success Message -->
        <div v-if="copied" class="mt-4 text-center">
          <span class="inline-flex items-center gap-1.5 px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Link copied to clipboard!
          </span>
        </div>
      </div>

      <!-- Related Polls Section -->
      <div v-if="relatedPolls.length > 0" class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h3 class="text-xl font-bold text-gray-900">More Polls</h3>
            <p class="text-gray-500 text-sm">Other polls you might like</p>
          </div>
          <router-link to="/polls" class="text-primary-600 hover:text-primary-700 font-medium text-sm group flex items-center gap-1">
            View All
            <svg class="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </router-link>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="relatedPoll in relatedPolls" :key="relatedPoll.id"
               @click="$router.push(`/poll/${relatedPoll.id}`)"
               class="group p-4 rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all duration-300 cursor-pointer">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div class="flex-1">
                <p class="font-medium text-gray-900 group-hover:text-primary-600 transition-colors line-clamp-2">{{ relatedPoll.question }}</p>
              </div>
            </div>
            <div class="flex items-center gap-4 text-xs text-gray-500">
              <span>{{ relatedPoll.total_votes }} votes</span>
              <span class="flex items-center gap-1">
                <span :class="relatedPoll.status === 'active' ? 'text-green-600' : 'text-gray-400'">●</span>
                {{ relatedPoll.status === 'active' ? 'Active' : 'Closed' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Not Found State -->
    <div v-else class="text-center py-16">
      <div class="w-24 h-24 bg-gray-100 rounded-3xl flex items-center justify-center mx-auto mb-6">
        <span class="text-6xl">📊</span>
      </div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">Poll Not Found</h2>
      <p class="text-gray-500 mb-6">This poll might have been removed or doesn't exist</p>
      <router-link to="/polls" 
                   class="inline-flex items-center gap-2 px-6 py-2.5 bg-primary-600 text-white font-medium rounded-xl hover:bg-primary-700 transition-all duration-300">
        Browse All Polls
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
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { api } from '@/services/api'
import { useWebSocket } from '@/composables/useWebSocket'
import { formatDate, getMatchStatusLabel } from '@/utils/formatters'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()

const loading = ref(true)
const poll = ref(null)
const pollOptions = ref([])
const totalVotes = ref(0)
const userVote = ref(null)
const copied = ref(false)
const relatedPolls = ref([])

const canVote = computed(() => {
  return authStore.isAuthenticated && 
         poll.value?.status === 'active' && 
         !userVote.value &&
         !loading.value
})

function getOptionColor(optionType) {
  const colors = {
    home: '#3b82f6',
    draw: '#eab308',
    away: '#ef4444',
  }
  return colors[optionType] || '#8b5cf6'
}

function isLeadingOption(optionId) {
  if (!pollOptions.value.length) return false
  const maxVotes = Math.max(...pollOptions.value.map(o => o.vote_count || 0))
  const option = pollOptions.value.find(o => o.id === optionId)
  return option && (option.vote_count || 0) === maxVotes && maxVotes > 0
}

function getRankNumber(optionId) {
  const sorted = [...pollOptions.value].sort((a, b) => (b.vote_count || 0) - (a.vote_count || 0))
  const index = sorted.findIndex(o => o.id === optionId)
  return index !== -1 ? index + 1 : null
}

function getRankStyle(index) {
  if (index === 0) return 'bg-yellow-100 text-yellow-700 border-2 border-yellow-400'
  if (index === 1) return 'bg-gray-100 text-gray-600 border-2 border-gray-300'
  if (index === 2) return 'bg-orange-100 text-orange-700 border-2 border-orange-300'
  return 'bg-gray-50 text-gray-500 border-2 border-gray-200'
}

async function handleVote(optionId) {
  if (!authStore.isAuthenticated) {
    uiStore.showWarning('Please sign in to vote', 'Authentication Required')
    return
  }
  
  loading.value = true
  
  try {
    const result = await api.vote(route.params.id, optionId)
    if (result) {
      uiStore.showSuccess('Vote recorded! 🎉', 'Thanks for participating')
      await loadPoll()
    }
  } catch (error) {
    console.error('Vote failed:', error)
    uiStore.showError('Failed to record vote', 'Please try again')
  } finally {
    loading.value = false
  }
}

async function loadPoll() {
  loading.value = true
  try {
    const data = await api.getPoll(route.params.id)
    if (data) {
      poll.value = data
      pollOptions.value = data.options || []
      totalVotes.value = data.total_votes || 0
      
      if (authStore.isAuthenticated && data.user_vote) {
        userVote.value = data.user_vote.option_id
      }
      
      // Load related polls
      await loadRelatedPolls()
    }
  } catch (error) {
    console.error('Failed to load poll:', error)
  } finally {
    loading.value = false
  }
}

async function loadRelatedPolls() {
  try {
    const response = await api.getPolls({ 
      status: 'active', 
      limit: 4,
      exclude: route.params.id 
    })
    relatedPolls.value = (response.results || response || []).filter(p => p.id !== route.params.id).slice(0, 4)
  } catch (error) {
    console.error('Failed to load related polls:', error)
    relatedPolls.value = []
  }
}

function sharePoll(platform) {
  const url = window.location.href
  const title = poll.value?.question || 'Vote in this poll'
  const shareUrls = {
    twitter: `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`,
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
  }
  if (shareUrls[platform]) {
    window.open(shareUrls[platform], '_blank', 'width=600,height=400')
  }
}

async function copyLink() {
  try {
    await navigator.clipboard.writeText(window.location.href)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}

// WebSocket for real-time updates
const { addListener } = useWebSocket(`/ws/poll/${route.params.id}`, {
  autoConnect: true,
  onMessage: (data) => {
    if (data.type === 'poll_update' || data.type === 'initial_poll_results') {
      const updateData = data.data
      if (updateData.results) {
        pollOptions.value = updateData.results
        totalVotes.value = updateData.total_votes
        if (poll.value) poll.value.total_votes = updateData.total_votes
      }
    }
  },
})

onMounted(() => {
  loadPoll()
})
</script>

<style scoped>
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes scale-in {
  0% { transform: scale(0); opacity: 0; }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); opacity: 1; }
}

@keyframes shine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-scale-in {
  animation: scale-in 0.3s ease-out;
}

.animate-shine {
  animation: shine 2s infinite;
}

.progress-ring {
  transition: stroke-dashoffset 0.35s;
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  /* Add the standard property below */
  line-clamp: 2; 
}
</style>