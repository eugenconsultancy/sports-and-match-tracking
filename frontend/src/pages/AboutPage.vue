<template>
  <div class="space-y-12">
    <!-- Hero Section -->
    <div class="text-center space-y-4">
      <h1 class="text-4xl md:text-5xl font-bold text-gray-900">About LiveScore</h1>
      <p class="text-xl text-gray-600 max-w-3xl mx-auto">
        Your ultimate destination for live sports scores, news, and real-time updates
      </p>
    </div>

    <!-- Mission Section -->
    <div class="card p-8 text-center">
      <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
        </svg>
      </div>
      <h2 class="text-2xl font-bold mb-3">Our Mission</h2>
      <p class="text-gray-600 max-w-2xl mx-auto">
        To deliver the fastest, most accurate live sports scores and news to fans around the world, 
        creating an immersive experience that brings you closer to the action.
      </p>
    </div>

    <!-- Stats Section -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold text-primary-600">50+</div>
        <div class="text-sm text-gray-500 mt-1">Competitions</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold text-primary-600">1000+</div>
        <div class="text-sm text-gray-500 mt-1">Teams</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold text-primary-600">10K+</div>
        <div class="text-sm text-gray-500 mt-1">Players</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-3xl font-bold text-primary-600">1M+</div>
        <div class="text-sm text-gray-500 mt-1">Active Users</div>
      </div>
    </div>

    <!-- Features Section -->
    <div>
      <h2 class="text-2xl font-bold text-center mb-8">What We Offer</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="card p-6">
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 class="font-bold mb-2">Live Scores</h3>
          <p class="text-sm text-gray-500">Real-time updates from matches around the world, delivered instantly.</p>
        </div>
        <div class="card p-6">
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 class="font-bold mb-2">Detailed Stats</h3>
          <p class="text-sm text-gray-500">Comprehensive match statistics, player profiles, and team analytics.</p>
        </div>
        <div class="card p-6">
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
            </svg>
          </div>
          <h3 class="font-bold mb-2">Breaking News</h3>
          <p class="text-sm text-gray-500">Latest news, transfers, and updates from the world of sports.</p>
        </div>
      </div>
    </div>

    <!-- Team Section -->
    <div>
      <h2 class="text-2xl font-bold text-center mb-8">Our Team</h2>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div v-for="member in team" :key="member.name" class="card p-6 text-center">
          <div class="w-24 h-24 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full mx-auto mb-4 flex items-center justify-center">
            <span class="text-2xl font-bold text-white">{{ member.name.charAt(0) }}</span>
          </div>
          <h3 class="font-bold">{{ member.name }}</h3>
          <p class="text-sm text-primary-600">{{ member.role }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const team = [
  { name: 'John Smith', role: 'CEO & Founder' },
  { name: 'Sarah Johnson', role: 'CTO' },
  { name: 'Mike Williams', role: 'Head of Product' },
  { name: 'Emily Brown', role: 'Head of Data' },
]
</script>