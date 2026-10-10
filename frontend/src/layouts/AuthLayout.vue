<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-50">
    <div class="container mx-auto px-4 py-12">
      <!-- Logo -->
      <div class="text-center mb-8">
        <router-link to="/" class="inline-flex items-center space-x-2">
          <div class="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center">
            <span class="text-white font-bold text-lg">LS</span>
          </div>
          <span class="text-2xl font-bold text-gray-900">LiveScore</span>
        </router-link>
      </div>
      
      <!-- Auth Card -->
      <div class="max-w-md mx-auto">
        <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>