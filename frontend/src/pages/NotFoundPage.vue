<template>
  <div class="max-w-2xl mx-auto px-4 py-20 text-center">
    <div class="text-8xl mb-6">⚽</div>
    <h1 class="text-6xl font-bold text-gray-300 mb-4">404</h1>
    <h2 class="text-2xl font-semibold text-gray-700 mb-3">Page Not Found</h2>
    <p class="text-gray-500 mb-8">
      The page you're looking for doesn't exist or has been moved.
      Maybe the match was postponed or the season ended.
    </p>
    <div class="flex items-center justify-center gap-4">
      <router-link to="/" class="btn-primary">
        Go Home
      </router-link>
      <button @click="goBack" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 font-medium">
        Go Back
      </button>
    </div>

    <!-- Suggestions -->
    <div class="mt-12 grid grid-cols-1 sm:grid-cols-3 gap-4">
      <router-link to="/live"
                   class="card text-center hover:border-red-300 cursor-pointer">
        <div class="text-3xl mb-2">📺</div>
        <p class="text-sm font-medium">Live Matches</p>
      </router-link>
      <router-link to="/competitions"
                   class="card text-center hover:border-primary-300 cursor-pointer">
        <div class="text-3xl mb-2">🏆</div>
        <p class="text-sm font-medium">Competitions</p>
      </router-link>
      <router-link to="/news"
                   class="card text-center hover:border-yellow-300 cursor-pointer">
        <div class="text-3xl mb-2">📰</div>
        <p class="text-sm font-medium">Latest News</p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goBack() {
  router.back()
}
</script>