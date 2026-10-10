<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Enhanced Header Section -->
      <div class="relative overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 rounded-2xl p-8 mb-8 text-white shadow-xl">
        <!-- Background Pattern -->
        <div class="absolute inset-0 opacity-10">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(120,119,198,0.3),rgba(255,255,255,0))]"></div>
          <div class="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-primary-500/20 to-transparent rounded-full blur-3xl"></div>
        </div>

        <div class="relative z-10">
          <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            <div>
              <h1 class="text-3xl sm:text-4xl font-bold mb-2 flex items-center gap-3">
                <span class="text-4xl">📰</span>
                Latest News
              </h1>
              <p class="text-white/70 text-lg">Stay updated with the latest football news and stories</p>
            </div>

            <!-- Quick Stats -->
            <div class="flex gap-4">
              <div class="bg-white/10 backdrop-blur rounded-2xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer">
                <div class="text-2xl font-bold">{{ totalArticles }}</div>
                <div class="text-xs text-white/70">Articles</div>
              </div>
              <div class="bg-white/10 backdrop-blur rounded-2xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer">
                <div class="text-2xl font-bold">{{ categories.length }}</div>
                <div class="text-xs text-white/70">Categories</div>
              </div>
              <div class="bg-white/10 backdrop-blur rounded-2xl px-5 py-3 text-center hover:bg-white/20 transition-all duration-300 cursor-pointer">
                <div class="text-2xl font-bold">{{ breakingNews.length }}</div>
                <div class="text-xs text-white/70">Breaking</div>
              </div>
            </div>
          </div>

          <!-- Enhanced Search and Filters -->
          <div class="mt-6 flex flex-col sm:flex-row gap-3">
            <div class="relative flex-1 group">
              <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-primary-500 transition-colors"
                   fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input v-model="searchQuery"
                     @input="debouncedSearch"
                     type="text"
                     placeholder="Search articles by title, content, or team..."
                     class="w-full pl-12 pr-4 py-3 bg-white/10 backdrop-blur border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300" />
              <button v-if="searchQuery" 
                      @click="searchQuery = ''; fetchArticles()"
                      class="absolute right-3 top-1/2 -translate-y-1/2 p-1 hover:bg-white/10 rounded-full transition-colors">
                <svg class="w-4 h-4 text-white/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <select v-model="categoryFilter" @change="handleFilterChange"
                    class="px-4 py-3 bg-white/10 backdrop-blur border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-primary-400 transition-all duration-300">
              <option value="" class="text-gray-900">All Categories</option>
              <option v-for="cat in categories" :key="cat.slug" :value="cat.slug" class="text-gray-900">
                {{ cat.name }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Breaking News Ticker - Enhanced -->
      <div v-if="breakingNews.length > 0 && !searchQuery && !categoryFilter" class="mb-8">
        <div class="relative overflow-hidden bg-gradient-to-r from-red-600 to-red-700 rounded-2xl shadow-lg shadow-red-500/20">
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-pattern-dots"></div>
          </div>
          
          <div class="relative p-4">
            <div class="flex items-center gap-4">
              <!-- Breaking Badge with Pulse -->
              <div class="flex items-center gap-2 bg-white/20 backdrop-blur rounded-xl px-4 py-2">
                <span class="relative flex h-3 w-3">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-3 w-3 bg-white"></span>
                </span>
                <span class="text-white font-bold text-sm uppercase tracking-wider">Breaking News</span>
              </div>
              
              <!-- Scrolling News -->
              <div class="flex-1 overflow-hidden">
                <div class="flex items-center gap-8 animate-marquee">
                  <router-link v-for="article in [...breakingNews, ...breakingNews]" :key="article.id + Math.random()"
                               :to="`/news/${article.id}`"
                               class="text-white hover:text-yellow-200 transition-colors whitespace-nowrap font-medium flex items-center gap-2 group">
                    <span class="w-1.5 h-1.5 bg-yellow-300 rounded-full group-hover:scale-150 transition-transform"></span>
                    {{ article.title }}
                    <span class="text-white/50 text-sm group-hover:text-white/80 transition-colors">{{ formatTimeAgo(article.published_at) }}</span>
                  </router-link>
                </div>
              </div>

              <!-- View All -->
              <router-link to="/news" 
                          class="hidden sm:flex items-center gap-1 text-white/80 hover:text-white transition-colors text-sm font-medium bg-white/10 hover:bg-white/20 rounded-lg px-3 py-1.5">
                View All
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Category Pills - Quick Filter -->
      <div v-if="!searchQuery && !categoryFilter" class="mb-8">
        <div class="flex items-center gap-3 mb-4">
          <h2 class="text-xl font-bold text-gray-900">Browse by Category</h2>
          <div class="h-px flex-1 bg-gray-200"></div>
        </div>
        <div class="flex gap-2 overflow-x-auto pb-2 custom-scrollbar">
          <button v-for="cat in categories.slice(0, 8)" :key="cat.slug"
                  @click="categoryFilter = cat.slug; handleFilterChange()"
                  class="group relative px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-300 whitespace-nowrap flex items-center gap-2 bg-white border border-gray-200 text-gray-600 hover:border-primary-300 hover:text-primary-600 hover:shadow-md hover:-translate-y-0.5">
            <span class="text-lg">{{ getCategoryIcon(cat.slug) }}</span>
            {{ cat.name }}
            <span class="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-0.5 bg-primary-500 rounded-full group-hover:w-1/2 transition-all duration-300"></span>
          </button>
        </div>
      </div>

      <!-- Active Filters Display -->
      <div v-if="categoryFilter || searchQuery" class="mb-6 flex items-center gap-3">
        <span class="text-sm text-gray-500">Active filters:</span>
        <div v-if="categoryFilter" 
             class="flex items-center gap-2 px-3 py-1.5 bg-primary-50 text-primary-700 rounded-lg text-sm">
          Category: {{ categories.find(c => c.slug === categoryFilter)?.name || categoryFilter }}
          <button @click="categoryFilter = ''; fetchArticles()" 
                  class="hover:bg-primary-100 rounded-full p-0.5 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div v-if="searchQuery" 
             class="flex items-center gap-2 px-3 py-1.5 bg-blue-50 text-blue-700 rounded-lg text-sm">
          Search: "{{ searchQuery }}"
          <button @click="searchQuery = ''; fetchArticles()" 
                  class="hover:bg-blue-100 rounded-full p-0.5 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <button @click="clearAllFilters" 
                class="text-sm text-gray-400 hover:text-gray-600 transition-colors ml-auto">
          Clear all
        </button>
      </div>

      <!-- Featured Articles Section -->
      <section v-if="featuredNews.length > 0 && !searchQuery && !categoryFilter" class="mb-10">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
              <span class="text-3xl">⭐</span>
              Featured Stories
            </h2>
            <p class="text-gray-500 text-sm mt-1">Top stories handpicked for you</p>
          </div>
        </div>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div v-for="article in featuredNews" :key="article.id"
               class="group relative bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer"
               @click="$router.push(`/news/${article.id}`)">
            <!-- Image -->
            <div class="relative h-64 overflow-hidden">
              <img v-if="article.image_url" :src="article.image_url" :alt="article.title"
                   class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
              <div v-else class="w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
                <span class="text-6xl">📰</span>
              </div>
              <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
              
              <!-- Category Badge -->
              <div class="absolute top-4 left-4">
                <span class="px-3 py-1 bg-white/90 backdrop-blur rounded-full text-xs font-semibold text-gray-700">
                  {{ article.category?.name || 'News' }}
                </span>
              </div>
            </div>
            
            <!-- Content -->
            <div class="absolute bottom-0 left-0 right-0 p-6 text-white">
              <h3 class="text-xl font-bold mb-2 line-clamp-2 group-hover:text-yellow-200 transition-colors">
                {{ article.title }}
              </h3>
              <p class="text-white/80 text-sm line-clamp-2 mb-3">{{ article.excerpt || article.content }}</p>
              <div class="flex items-center justify-between text-white/60 text-xs">
                <span>{{ formatDate(article.published_at) }}</span>
                <span class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ article.read_time || '5 min read' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Articles Grid Section -->
      <section>
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 v-if="searchQuery || categoryFilter" class="text-2xl font-bold text-gray-900">
              Search Results
              <span class="text-lg font-normal text-gray-500 ml-2">({{ articles.length }} articles)</span>
            </h2>
            <div v-else>
              <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
                <span class="text-3xl">📰</span>
                Latest Articles
              </h2>
              <p class="text-gray-500 text-sm mt-1">Stay informed with the most recent updates</p>
            </div>
          </div>
          
          <!-- Sort Options -->
          <div v-if="articles.length > 0" class="flex items-center gap-2">
            <button class="px-3 py-1.5 text-xs font-medium rounded-lg bg-primary-50 text-primary-700">
              Latest
            </button>
            <button class="px-3 py-1.5 text-xs font-medium rounded-lg bg-gray-50 text-gray-600 hover:bg-gray-100 transition-colors">
              Popular
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="i in 6" :key="i" class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden animate-pulse">
            <div class="h-48 bg-gray-200"></div>
            <div class="p-5 space-y-3">
              <div class="h-4 bg-gray-200 rounded-full w-1/4"></div>
              <div class="h-6 bg-gray-200 rounded-full w-3/4"></div>
              <div class="h-4 bg-gray-200 rounded-full w-full"></div>
              <div class="h-4 bg-gray-200 rounded-full w-2/3"></div>
              <div class="flex items-center justify-between pt-2">
                <div class="h-3 bg-gray-200 rounded-full w-1/3"></div>
                <div class="h-3 bg-gray-200 rounded-full w-1/4"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Articles Grid -->
        <div v-else-if="articles.length > 0"
             class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="article in articles" :key="article.id"
               class="group bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer"
               @click="$router.push(`/news/${article.id}`)">
            <!-- Article Image -->
            <div class="relative h-48 overflow-hidden bg-gray-100">
              <img v-if="article.image_url" :src="article.image_url" :alt="article.title"
                   class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
              <div v-else class="w-full h-full bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
                <span class="text-5xl">📰</span>
              </div>
              
              <!-- Category Tag -->
              <div class="absolute top-3 left-3">
                <span class="px-2.5 py-1 bg-white/90 backdrop-blur rounded-lg text-xs font-semibold text-gray-700 shadow-sm">
                  {{ getCategoryIcon(article.category?.slug) }} {{ article.category?.name || 'General' }}
                </span>
              </div>
              
              <!-- Breaking Badge -->
              <div v-if="article.is_breaking" class="absolute top-3 right-3">
                <span class="px-2.5 py-1 bg-red-500 rounded-lg text-xs font-bold text-white shadow-sm flex items-center gap-1">
                  <span class="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>
                  Breaking
                </span>
              </div>
            </div>

            <!-- Article Content -->
            <div class="p-5">
              <!-- Author & Date -->
              <div class="flex items-center gap-2 mb-3">
                <div v-if="article.author?.avatar_url" class="w-6 h-6 rounded-full overflow-hidden">
                  <img :src="article.author.avatar_url" class="w-full h-full object-cover" />
                </div>
                <div class="flex items-center gap-2 text-xs text-gray-500">
                  <span v-if="article.author?.name">{{ article.author.name }}</span>
                  <span v-if="article.author?.name && article.published_at">·</span>
                  <span>{{ formatTimeAgo(article.published_at) }}</span>
                </div>
              </div>

              <!-- Title -->
              <h3 class="font-bold text-gray-900 mb-2 line-clamp-2 group-hover:text-primary-600 transition-colors">
                {{ article.title }}
              </h3>
              
              <!-- Excerpt -->
              <p class="text-sm text-gray-600 line-clamp-2 mb-4">
                {{ article.excerpt || stripHtml(article.content) }}
              </p>

              <!-- Footer -->
              <div class="flex items-center justify-between pt-3 border-t border-gray-100">
                <div class="flex items-center gap-3 text-xs text-gray-500">
                  <span class="flex items-center gap-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {{ article.read_time || '5 min' }}
                  </span>
                  <span class="flex items-center gap-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    {{ article.views || 0 }}
                  </span>
                </div>
                <span class="text-primary-600 text-sm font-medium group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">
                  Read More
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-16">
          <div class="w-24 h-24 bg-gray-100 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-lg">
            <span class="text-5xl">📰</span>
          </div>
          <h3 class="text-xl font-bold text-gray-900 mb-2">No Articles Found</h3>
          <p class="text-gray-500 mb-6 max-w-md mx-auto">
            {{ searchQuery 
              ? `No articles match your search for "${searchQuery}". Try different keywords or clear your search.`
              : categoryFilter 
                ? `No articles found in this category. Try selecting a different category.`
                : 'No articles have been published yet. Check back soon for the latest news!'
            }}
          </p>
          <button v-if="searchQuery || categoryFilter"
                  @click="clearAllFilters"
                  class="inline-flex items-center gap-2 px-6 py-2.5 bg-primary-600 text-white font-medium rounded-xl hover:bg-primary-700 transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5">
            Clear Filters
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>

        <!-- Load More Button -->
        <div v-if="hasMore && articles.length > 0" class="text-center mt-10">
          <button @click="loadMore" 
                  class="group inline-flex items-center gap-2 px-8 py-3 bg-white border-2 border-gray-200 text-gray-700 font-medium rounded-xl hover:border-primary-300 hover:text-primary-600 hover:shadow-lg transition-all duration-300"
                  :disabled="loadingMore">
            <span v-if="loadingMore" class="flex items-center gap-2">
              <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Loading...
            </span>
            <span v-else class="flex items-center gap-2">
              Load More Articles
              <svg class="w-5 h-5 group-hover:translate-y-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
              </svg>
            </span>
          </button>
        </div>

        <!-- Back to Top -->
        <div v-if="articles.length > 12" class="text-center mt-6">
          <button @click="scrollToTop" 
                  class="text-sm text-gray-400 hover:text-gray-600 transition-colors flex items-center gap-1 mx-auto">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
            </svg>
            Back to top
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axios'

const router = useRouter()

const loading = ref(true)
const loadingMore = ref(false)
const articles = ref([])
const breakingNews = ref([])
const featuredNews = ref([])
const categories = ref([])
const searchQuery = ref('')
const categoryFilter = ref('')
const page = ref(1)
const hasMore = ref(false)
let searchTimeout = null

const totalArticles = computed(() => articles.value.length)

function getCategoryIcon(slug) {
  const icons = {
    'premier-league': '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
    'la-liga': '🇪🇸',
    'serie-a': '🇮🇹',
    'bundesliga': '🇩🇪',
    'ligue-1': '🇫🇷',
    'champions-league': '⭐',
    'transfer-news': '💸',
    'injury-news': '🏥',
    'match-preview': '🔮',
    'match-review': '📊',
    'team-news': '👥',
    'player-news': '⚽',
    'tactics': '📋',
    'opinion': '💭',
    'breaking': '🚨',
  }
  return icons[slug] || '📰'
}

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchArticles()
  }, 400)
}

function handleFilterChange() {
  page.value = 1
  fetchArticles()
}

function clearAllFilters() {
  searchQuery.value = ''
  categoryFilter.value = ''
  page.value = 1
  fetchArticles()
}

function stripHtml(html) {
  if (!html) return ''
  const tmp = document.createElement('div')
  tmp.innerHTML = html
  return tmp.textContent || tmp.innerText || ''
}

function formatDate(dateString) {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function formatTimeAgo(dateString) {
  if (!dateString) return ''
  
  const now = new Date()
  const date = new Date(dateString)
  const seconds = Math.floor((now - date) / 1000)
  
  if (seconds < 60) return 'Just now'
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
  if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`
  
  return formatDate(dateString)
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function fetchArticles(pageNum = 1) {
  if (pageNum === 1) loading.value = true
  else loadingMore.value = true

  try {
    const params = {
      status: 'published',
      page: pageNum,
      limit: 12,
    }
    if (categoryFilter.value) params.category = categoryFilter.value
    if (searchQuery.value) {
      params.search = searchQuery.value
      delete params.category
    }

    const res = await axios.get('/api/v1/news/articles/', { params })
    const data = res.data

    if (pageNum === 1) {
      articles.value = data.results || data
    } else {
      articles.value = [...articles.value, ...(data.results || [])]
    }

    hasMore.value = data.next !== null
    page.value = pageNum
  } catch (error) {
    console.error('Failed to fetch articles:', error)
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

async function loadMore() {
  await fetchArticles(page.value + 1)
}

onMounted(async () => {
  try {
    const [articlesRes, breakingRes, featuredRes, catRes] = await Promise.all([
      axios.get('/api/v1/news/articles/', { params: { status: 'published', limit: 12 } }),
      axios.get('/api/v1/news/articles/breaking/'),
      axios.get('/api/v1/news/articles/featured/'),
      axios.get('/api/v1/news/categories/'),
    ])

    articles.value = articlesRes.data.results || articlesRes.data || []
    breakingNews.value = breakingRes.data || []
    featuredNews.value = featuredRes.data || []
    categories.value = catRes.data.results || catRes.data || []

    hasMore.value = articlesRes.data.next !== null
  } catch (error) {
    console.error('Failed to load news:', error)
  } finally {
    loading.value = false
  }
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
  line-clamp: 2;
  overflow: hidden;
}

@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.animate-marquee {
  animation: marquee 40s linear infinite;
}

.animate-marquee:hover {
  animation-play-state: paused;
}

.bg-pattern-dots {
  background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='2' cy='2' r='1' fill='white' opacity='0.3'/%3E%3C/svg%3E");
  background-size: 20px 20px;
}
</style>