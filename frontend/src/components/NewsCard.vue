<template>
  <div class="group relative bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
       :class="[featured ? 'md:col-span-2 md:grid md:grid-cols-2' : '']"
       @click="$router.push(`/news/${article.id}`)">
    
    <!-- Image Section -->
    <div class="relative overflow-hidden" :class="featured ? 'md:h-full' : 'h-48'">
      <!-- Image -->
      <img v-if="article.cover_image || article.thumbnail || article.image_url"
           :src="article.cover_image || article.thumbnail || article.image_url"
           :alt="article.title"
           class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
           :class="featured ? 'md:h-full' : 'h-48'" />
      
      <!-- Placeholder -->
      <div v-else
           class="w-full h-full bg-gradient-to-br from-primary-400 via-primary-500 to-purple-600 flex items-center justify-center relative overflow-hidden"
           :class="featured ? 'md:h-full' : 'h-48'">
        <!-- Decorative Circles -->
        <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2"></div>
        <div class="absolute bottom-0 left-0 w-24 h-24 bg-white/10 rounded-full translate-y-1/2 -translate-x-1/2"></div>
        <span class="text-5xl font-black text-white/30 relative z-10">LS</span>
      </div>

      <!-- Gradient Overlay -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>

      <!-- Top Badges -->
      <div class="absolute top-3 left-3 flex gap-2">
        <!-- Category Badge -->
        <span v-if="article.category_name || article.category?.name"
              class="px-2.5 py-1 bg-white/95 backdrop-blur rounded-lg text-xs font-semibold text-gray-700 shadow-sm">
          {{ article.category_name || article.category?.name }}
        </span>
      </div>

      <!-- Breaking News Badge -->
      <div v-if="article.is_breaking" class="absolute top-3 right-3">
        <span class="px-2.5 py-1 bg-red-600 rounded-lg text-xs font-bold text-white shadow-lg flex items-center gap-1.5">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-white"></span>
          </span>
          Breaking
        </span>
      </div>

      <!-- Featured Badge -->
      <div v-if="article.is_featured && !article.is_breaking" class="absolute top-3 right-3">
        <span class="px-2.5 py-1 bg-yellow-500 rounded-lg text-xs font-bold text-white shadow-lg flex items-center gap-1">
          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
            <path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
          </svg>
          Featured
        </span>
      </div>

      <!-- Read Time (Bottom Right) -->
      <div class="absolute bottom-3 right-3">
        <span class="px-2.5 py-1 bg-black/50 backdrop-blur rounded-lg text-xs font-medium text-white">
          {{ article.reading_time_minutes || article.read_time || '5' }} min read
        </span>
      </div>
    </div>

    <!-- Content Section -->
    <div class="p-5" :class="featured ? 'md:flex md:flex-col md:justify-center' : ''">
      <!-- Tags -->
      <div v-if="article.tags?.length" class="flex items-center gap-2 mb-3">
        <span v-for="tag in article.tags.slice(0, 2)" :key="tag.id || tag.name"
              class="px-2 py-0.5 bg-primary-50 text-primary-700 rounded-md text-xs font-medium">
          {{ tag.name }}
        </span>
      </div>

      <!-- Title -->
      <h3 class="font-bold text-gray-900 group-hover:text-primary-600 transition-colors line-clamp-2 mb-2"
          :class="featured ? 'text-xl lg:text-2xl' : 'text-base'">
        {{ article.title }}
      </h3>

      <!-- Summary/Excerpt -->
      <p v-if="article.summary || article.excerpt" 
         class="text-sm text-gray-500 line-clamp-3 mb-4"
         :class="featured ? 'md:line-clamp-4' : ''">
        {{ article.summary || article.excerpt }}
      </p>

      <!-- Author & Meta Footer -->
      <div class="flex items-center justify-between mt-auto">
        <!-- Author Info -->
        <div class="flex items-center gap-2">
          <!-- Author Avatar -->
          <div v-if="article.author?.avatar_url" class="w-7 h-7 rounded-full overflow-hidden">
            <img :src="article.author.avatar_url" :alt="article.author?.name" class="w-full h-full object-cover" />
          </div>
          <div v-else class="w-7 h-7 bg-primary-100 rounded-full flex items-center justify-center">
            <svg class="w-3.5 h-3.5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <span class="text-xs font-medium text-gray-600">
            {{ article.author_name || article.author?.name || 'LiveScore' }}
          </span>
        </div>

        <!-- Date & Read More -->
        <div class="flex items-center gap-3 text-xs text-gray-400">
          <span class="flex items-center gap-1">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ formatTimeAgo(article.published_at) }}
          </span>
          <span class="hidden sm:flex items-center gap-1 text-primary-600 opacity-0 group-hover:opacity-100 transition-opacity">
            Read More
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </span>
        </div>
      </div>

      <!-- Article Stats (Optional) -->
      <div v-if="article.views || article.comments_count" class="mt-3 pt-3 border-t border-gray-100 flex items-center gap-4 text-xs text-gray-400">
        <span v-if="article.views" class="flex items-center gap-1">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          {{ article.views.toLocaleString() }}
        </span>
        <span v-if="article.comments_count" class="flex items-center gap-1">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          {{ article.comments_count }}
        </span>
      </div>
    </div>

    <!-- Hover Overlay -->
    <div class="absolute inset-0 bg-gradient-to-t from-primary-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none rounded-2xl"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  article: { 
    type: Object, 
    required: true,
    validator: (obj) => {
      return obj.title
    }
  },
  featured: { 
    type: Boolean, 
    default: false 
  },
})

function formatDate(dateString) {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
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
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  line-clamp: 3;
  overflow: hidden;
}

.line-clamp-4 {
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  line-clamp: 4;
  overflow: hidden;
}

@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

.animate-ping {
  animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>