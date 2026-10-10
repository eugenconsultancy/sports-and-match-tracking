<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <!-- Enhanced Hero Header -->
      <div class="relative overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 rounded-2xl p-8 text-white shadow-xl">
        <!-- Background Pattern -->
        <div class="absolute inset-0 opacity-10">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(120,119,198,0.3),rgba(255,255,255,0))]"></div>
          <div class="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-primary-500/20 to-transparent rounded-full blur-3xl"></div>
        </div>

        <div class="relative z-10">
          <div class="flex items-center gap-4">
            <div class="w-16 h-16 bg-white/10 backdrop-blur rounded-2xl flex items-center justify-center">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <div>
              <h1 class="text-3xl sm:text-4xl font-bold tracking-tight">Settings</h1>
              <p class="text-white/70 mt-1">Manage your account and preferences</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Profile Section -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        <!-- Section Header -->
        <div class="bg-gradient-to-r from-primary-50 to-blue-50 px-6 py-4 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <div>
              <h2 class="text-lg font-bold text-gray-900">Profile Information</h2>
              <p class="text-xs text-gray-500">Update your personal details</p>
            </div>
          </div>
        </div>

        <div class="p-6 space-y-6">
          <!-- Avatar Section -->
          <div class="flex items-center gap-6 pb-6 border-b border-gray-100">
            <div class="relative">
              <div class="w-20 h-20 bg-gradient-to-br from-primary-400 to-primary-600 rounded-2xl flex items-center justify-center text-2xl font-bold text-white shadow-lg">
                {{ profile.first_name?.charAt(0) || 'U' }}{{ profile.last_name?.charAt(0) || '' }}
              </div>
              <button class="absolute -bottom-2 -right-2 w-8 h-8 bg-white rounded-lg shadow-md border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition-colors group">
                <svg class="w-4 h-4 text-gray-600 group-hover:text-primary-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </button>
            </div>
            <div>
              <p class="font-semibold text-gray-900">{{ profile.first_name }} {{ profile.last_name }}</p>
              <p class="text-sm text-gray-500">{{ profile.email }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">First Name</label>
              <input 
                v-model="profile.first_name" 
                :disabled="!isEditing"
                type="text"
                class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 disabled:bg-gray-50 disabled:text-gray-500"
                :class="{ 'bg-gray-50': !isEditing }" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Last Name</label>
              <input 
                v-model="profile.last_name" 
                :disabled="!isEditing"
                type="text"
                class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 disabled:bg-gray-50 disabled:text-gray-500"
                :class="{ 'bg-gray-50': !isEditing }" />
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Email Address</label>
            <div class="relative">
              <input 
                v-model="profile.email" 
                disabled
                type="email"
                class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-500 cursor-not-allowed" />
              <div class="absolute right-3 top-1/2 -translate-y-1/2">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
            </div>
            <p class="text-xs text-gray-400 mt-1">Email cannot be changed</p>
          </div>
          
          <div class="flex justify-end gap-3 pt-4 border-t border-gray-100">
            <template v-if="isEditing">
              <button @click="cancelEdit" 
                      class="px-5 py-2.5 text-sm font-semibold text-gray-700 hover:bg-gray-100 rounded-xl transition-all duration-300">
                Cancel
              </button>
              <button @click="saveProfile" 
                      :disabled="savingProfile"
                      class="px-5 py-2.5 bg-primary-600 text-white text-sm font-semibold rounded-xl hover:bg-primary-700 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all duration-300 disabled:opacity-50 shadow-sm hover:shadow-md flex items-center gap-2">
                <svg v-if="savingProfile" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                {{ savingProfile ? 'Saving...' : 'Save Changes' }}
              </button>
            </template>
            <button v-else @click="isEditing = true" 
                    class="px-5 py-2.5 border-2 border-gray-300 text-gray-700 text-sm font-semibold rounded-xl hover:border-primary-300 hover:text-primary-600 hover:bg-primary-50 transition-all duration-300 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
              Edit Profile
            </button>
          </div>
        </div>
      </div>

      <!-- Password Section -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        <div class="bg-gradient-to-r from-blue-50 to-purple-50 px-6 py-4 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <div>
              <h2 class="text-lg font-bold text-gray-900">Change Password</h2>
              <p class="text-xs text-gray-500">Ensure your account is secure</p>
            </div>
          </div>
        </div>

        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Current Password</label>
            <div class="relative">
              <input 
                v-model="passwordForm.current"
                :type="showCurrentPassword ? 'text' : 'password'"
                class="w-full px-4 py-2.5 border rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                :class="passwordErrors.current ? 'border-red-300 bg-red-50' : 'border-gray-300'" />
              <button @click="showCurrentPassword = !showCurrentPassword" 
                      class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                <svg v-if="showCurrentPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M15 12a3 3 0 01-4.243 4.243" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
            <p v-if="passwordErrors.current" class="text-xs text-red-600 mt-1">{{ passwordErrors.current }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">New Password</label>
            <div class="relative">
              <input 
                v-model="passwordForm.new"
                :type="showNewPassword ? 'text' : 'password'"
                class="w-full px-4 py-2.5 border rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                :class="passwordErrors.new ? 'border-red-300 bg-red-50' : 'border-gray-300'" />
              <button @click="showNewPassword = !showNewPassword" 
                      class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                <svg v-if="showNewPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M15 12a3 3 0 01-4.243 4.243" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
            <p v-if="passwordErrors.new" class="text-xs text-red-600 mt-1">{{ passwordErrors.new }}</p>
            <!-- Password Strength Indicator -->
            <div v-if="passwordForm.new" class="mt-2">
              <div class="flex gap-1">
                <div v-for="i in 4" :key="i" 
                     class="h-1 flex-1 rounded-full transition-all duration-300"
                     :class="getStrengthBarClass(i)"></div>
              </div>
              <p class="text-xs mt-1" :class="getStrengthTextClass">{{ getStrengthText }}</p>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Confirm New Password</label>
            <div class="relative">
              <input 
                v-model="passwordForm.confirm"
                :type="showConfirmPassword ? 'text' : 'password'"
                class="w-full px-4 py-2.5 border rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                :class="passwordErrors.confirm ? 'border-red-300 bg-red-50' : 'border-gray-300'" />
              <button @click="showConfirmPassword = !showConfirmPassword" 
                      class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                <svg v-if="showConfirmPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M15 12a3 3 0 01-4.243 4.243" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
            <p v-if="passwordErrors.confirm" class="text-xs text-red-600 mt-1">{{ passwordErrors.confirm }}</p>
          </div>
          
          <div class="flex justify-end pt-4 border-t border-gray-100">
            <button @click="changePassword" 
                    :disabled="changingPassword"
                    class="px-5 py-2.5 bg-blue-600 text-white text-sm font-semibold rounded-xl hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-300 disabled:opacity-50 shadow-sm hover:shadow-md flex items-center gap-2">
              <svg v-if="changingPassword" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              {{ changingPassword ? 'Changing...' : 'Change Password' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Notification Preferences -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        <div class="bg-gradient-to-r from-green-50 to-emerald-50 px-6 py-4 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-green-100 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </div>
            <div>
              <h2 class="text-lg font-bold text-gray-900">Notification Preferences</h2>
              <p class="text-xs text-gray-500">Choose what to receive notifications about</p>
            </div>
          </div>
        </div>

        <div class="p-6">
          <!-- Match Notifications -->
          <div class="mb-6">
            <h3 class="text-sm font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <span class="text-lg">⚽</span>
              Match Notifications
            </h3>
            <div class="space-y-3">
              <label v-for="option in matchNotifications" :key="option.key"
                     class="flex items-center justify-between p-3 rounded-xl hover:bg-gray-50 transition-colors cursor-pointer group">
                <div>
                  <span class="text-sm font-medium text-gray-700 group-hover:text-gray-900 transition-colors">{{ option.label }}</span>
                  <p class="text-xs text-gray-400 mt-0.5">{{ option.description }}</p>
                </div>
                <div class="relative">
                  <input type="checkbox" 
                         v-model="preferences[option.key]" 
                         class="sr-only peer" />
                  <div class="w-11 h-6 bg-gray-200 peer-checked:bg-green-500 rounded-full transition-all duration-300 peer-checked:shadow-lg peer-checked:shadow-green-500/30"></div>
                  <div class="absolute left-0.5 top-0.5 w-5 h-5 bg-white rounded-full shadow peer-checked:translate-x-5 transition-transform duration-300"></div>
                </div>
              </label>
            </div>
          </div>

          <!-- Other Notifications -->
          <div>
            <h3 class="text-sm font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <span class="text-lg">📧</span>
              Other Notifications
            </h3>
            <div class="space-y-3">
              <label v-for="option in otherNotifications" :key="option.key"
                     class="flex items-center justify-between p-3 rounded-xl hover:bg-gray-50 transition-colors cursor-pointer group">
                <div>
                  <span class="text-sm font-medium text-gray-700 group-hover:text-gray-900 transition-colors">{{ option.label }}</span>
                  <p class="text-xs text-gray-400 mt-0.5">{{ option.description }}</p>
                </div>
                <div class="relative">
                  <input type="checkbox" 
                         v-model="preferences[option.key]" 
                         class="sr-only peer" />
                  <div class="w-11 h-6 bg-gray-200 peer-checked:bg-primary-500 rounded-full transition-all duration-300 peer-checked:shadow-lg peer-checked:shadow-primary-500/30"></div>
                  <div class="absolute left-0.5 top-0.5 w-5 h-5 bg-white rounded-full shadow peer-checked:translate-x-5 transition-transform duration-300"></div>
                </div>
              </label>
            </div>
          </div>
          
          <div class="flex justify-end pt-6 border-t border-gray-100 mt-6">
            <button @click="savePreferences" 
                    :disabled="savingPreferences"
                    class="px-5 py-2.5 bg-green-600 text-white text-sm font-semibold rounded-xl hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-300 disabled:opacity-50 shadow-sm hover:shadow-md flex items-center gap-2">
              <svg v-if="savingPreferences" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              {{ savingPreferences ? 'Saving...' : 'Save Preferences' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Danger Zone -->
      <div class="bg-gradient-to-br from-red-50 to-orange-50 rounded-2xl shadow-lg border-2 border-red-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-red-200 bg-gradient-to-r from-red-100/50 to-orange-100/50">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <div>
              <h2 class="text-lg font-bold text-red-700">Danger Zone</h2>
              <p class="text-xs text-red-600">Irreversible actions</p>
            </div>
          </div>
        </div>

        <div class="p-6">
          <div class="flex items-start justify-between gap-4">
            <div>
              <h3 class="font-semibold text-gray-900 mb-1">Deactivate Account</h3>
              <p class="text-sm text-gray-600">Once you deactivate your account, you will lose all your data, favorites, and preferences. This action cannot be undone.</p>
            </div>
          </div>
          
          <div class="flex justify-end mt-6">
            <button @click="showDeactivateModal = true" 
                    class="px-5 py-2.5 bg-red-600 text-white text-sm font-semibold rounded-xl hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-all duration-300 shadow-sm hover:shadow-md flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Deactivate Account
            </button>
          </div>
        </div>
      </div>

      <!-- Deactivate Confirmation Modal -->
      <Teleport to="body">
        <div v-if="showDeactivateModal" 
             class="fixed inset-0 z-50 flex items-center justify-center p-4"
             @click.self="showDeactivateModal = false">
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/50 backdrop-blur-sm"></div>
          
          <!-- Modal -->
          <div class="relative bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 animate-scale-in">
            <div class="text-center mb-6">
              <div class="w-16 h-16 bg-red-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <h3 class="text-xl font-bold text-gray-900 mb-2">Deactivate Account</h3>
              <p class="text-gray-500 text-sm">Are you sure you want to deactivate your account? This action cannot be undone.</p>
            </div>
            
            <div class="flex gap-3">
              <button @click="showDeactivateModal = false" 
                      class="flex-1 px-4 py-2.5 border-2 border-gray-300 text-gray-700 font-semibold rounded-xl hover:bg-gray-50 transition-all duration-300">
                Cancel
              </button>
              <button @click="deactivateAccount" 
                      :disabled="deactivating"
                      class="flex-1 px-4 py-2.5 bg-red-600 text-white font-semibold rounded-xl hover:bg-red-700 transition-all duration-300 disabled:opacity-50 flex items-center justify-center gap-2">
                <svg v-if="deactivating" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                {{ deactivating ? 'Deactivating...' : 'Yes, Deactivate' }}
              </button>
            </div>
          </div>
        </div>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { api } from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()

const isEditing = ref(false)
const savingProfile = ref(false)
const changingPassword = ref(false)
const savingPreferences = ref(false)
const deactivating = ref(false)
const showDeactivateModal = ref(false)

const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const profile = ref({
  first_name: '',
  last_name: '',
  email: '',
})

const passwordForm = ref({
  current: '',
  new: '',
  confirm: '',
})
const passwordErrors = ref({})

const preferences = ref({
  notification_match_start: true,
  notification_goal: true,
  notification_red_card: true,
  notification_half_time: false,
  notification_full_time: true,
  notification_news: false,
  email_notifications: true,
  push_notifications: true,
})

const matchNotifications = [
  { key: 'notification_match_start', label: 'Match Start', description: 'Get notified when matches begin' },
  { key: 'notification_goal', label: 'Goals', description: 'Get notified when goals are scored' },
  { key: 'notification_red_card', label: 'Red Cards', description: 'Get notified for red card incidents' },
  { key: 'notification_half_time', label: 'Half Time', description: 'Get notified at half time' },
  { key: 'notification_full_time', label: 'Full Time', description: 'Get notified at full time' },
]

const otherNotifications = [
  { key: 'notification_news', label: 'News Updates', description: 'Get notified about breaking news' },
  { key: 'email_notifications', label: 'Email Notifications', description: 'Receive notifications via email' },
  { key: 'push_notifications', label: 'Push Notifications', description: 'Receive push notifications in browser' },
]

// Password strength calculation
const passwordStrength = computed(() => {
  const password = passwordForm.value.new
  if (!password) return 0
  
  let strength = 0
  if (password.length >= 8) strength++
  if (password.match(/[A-Z]/)) strength++
  if (password.match(/[0-9]/)) strength++
  if (password.match(/[^A-Za-z0-9]/)) strength++
  return strength
})

const strengthTexts = ['Weak', 'Fair', 'Good', 'Strong']
const strengthColors = ['text-red-600', 'text-orange-600', 'text-yellow-600', 'text-green-600']

const getStrengthText = computed(() => {
  if (passwordStrength.value === 0) return ''
  return strengthTexts[passwordStrength.value - 1]
})

const getStrengthTextClass = computed(() => {
  if (passwordStrength.value === 0) return ''
  return strengthColors[passwordStrength.value - 1]
})

function getStrengthBarClass(index) {
  if (passwordStrength.value === 0) return 'bg-gray-200'
  if (index <= passwordStrength.value) {
    const colors = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-green-500']
    return colors[passwordStrength.value - 1]
  }
  return 'bg-gray-200'
}

onMounted(() => {
  if (authStore.user) {
    profile.value = {
      first_name: authStore.user.first_name || '',
      last_name: authStore.user.last_name || '',
      email: authStore.user.email || '',
    }
  }
})

function cancelEdit() {
  isEditing.value = false
  profile.value = {
    first_name: authStore.user?.first_name || '',
    last_name: authStore.user?.last_name || '',
    email: authStore.user?.email || '',
  }
}

async function saveProfile() {
  savingProfile.value = true
  try {
    await authStore.updateProfile({
      first_name: profile.value.first_name,
      last_name: profile.value.last_name,
    })
    isEditing.value = false
    uiStore.showSuccess('Profile updated successfully', '')
  } catch (error) {
    uiStore.showError('Failed to update profile', 'Please try again')
  } finally {
    savingProfile.value = false
  }
}

async function changePassword() {
  passwordErrors.value = {}
  
  if (!passwordForm.value.current) {
    passwordErrors.value.current = 'Current password is required'
    return
  }
  if (passwordForm.value.new.length < 8) {
    passwordErrors.value.new = 'Password must be at least 8 characters'
    return
  }
  if (passwordForm.value.new !== passwordForm.value.confirm) {
    passwordErrors.value.confirm = 'Passwords do not match'
    return
  }
  
  changingPassword.value = true
  try {
    await authStore.changePassword(passwordForm.value.current, passwordForm.value.new)
    passwordForm.value = { current: '', new: '', confirm: '' }
    uiStore.showSuccess('Password changed successfully', '')
  } catch (error) {
    uiStore.showError(error.response?.data?.detail || 'Failed to change password', 'Please try again')
  } finally {
    changingPassword.value = false
  }
}

async function savePreferences() {
  savingPreferences.value = true
  try {
    // API call to save preferences
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API call
    uiStore.showSuccess('Preferences saved successfully', '')
  } catch (error) {
    uiStore.showError('Failed to save preferences', 'Please try again')
  } finally {
    savingPreferences.value = false
  }
}

async function deactivateAccount() {
  deactivating.value = true
  try {
    // await authStore.deactivate()
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API call
    showDeactivateModal.value = false
    authStore.logout()
    uiStore.showSuccess('Account deactivated', '')
    router.push('/')
  } catch (error) {
    uiStore.showError('Failed to deactivate account', 'Please try again')
  } finally {
    deactivating.value = false
  }
}
</script>

<style scoped>
@keyframes scale-in {
  0% { transform: scale(0.95); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

.animate-scale-in {
  animation: scale-in 0.2s ease-out;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>