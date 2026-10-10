<template>
  <aside class="sidebar" :class="{ open: open }">
    <!-- Logo -->
    <div class="sidebar-logo">
      <div class="logo-mark">⚽</div>
      <span class="logo-text">LiveScore</span>
    </div>

    <nav class="sidebar-nav">
      <!-- Main Section -->
      <div class="nav-section">
        <span class="nav-label">MAIN</span>
        <router-link
          v-for="item in primaryNav"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: $route.path === item.path }"
          @click="$emit('close')"
        >
          <span class="nav-icon" v-html="item.icon" />
          <span class="nav-text">{{ item.label }}</span>
          <span v-if="item.badge && liveMatchCount > 0" class="live-badge">
            <span class="live-dot" />
            {{ liveMatchCount }}
          </span>
          <span v-if="$route.path === item.path" class="active-bar" />
        </router-link>
      </div>

      <!-- Explore Section -->
      <div class="nav-section">
        <span class="nav-label">EXPLORE</span>
        <router-link
          v-for="item in exploreNav"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: $route.path === item.path }"
          @click="$emit('close')"
        >
          <span class="nav-icon" v-html="item.icon" />
          <span class="nav-text">{{ item.label }}</span>
          <span v-if="$route.path === item.path" class="active-bar" />
        </router-link>
      </div>

      <!-- Personal Section -->
      <div v-if="authStore.isAuthenticated" class="nav-section">
        <span class="nav-label">PERSONAL</span>
        <router-link
          to="/favorites"
          class="nav-item"
          :class="{ active: $route.path === '/favorites' }"
          @click="$emit('close')"
        >
          <span class="nav-icon">★</span>
          <span class="nav-text">Favorites</span>
          <span v-if="$route.path === '/favorites'" class="active-bar" />
        </router-link>
        <router-link
          to="/profile"
          class="nav-item"
          :class="{ active: $route.path === '/profile' }"
          @click="$emit('close')"
        >
          <span class="nav-icon">◎</span>
          <span class="nav-text">My Profile</span>
          <span v-if="$route.path === '/profile'" class="active-bar" />
        </router-link>
      </div>
    </nav>

    <!-- User Profile Card -->
    <div class="sidebar-footer">
      <div v-if="authStore.isAuthenticated" class="user-card">
        <div class="user-avatar">
          {{ authStore.user?.first_name?.charAt(0) || authStore.user?.email?.charAt(0) || 'U' }}
        </div>
        <div class="user-info">
          <p class="user-name">{{ authStore.user?.first_name || 'User' }}</p>
          <p class="user-email">{{ authStore.user?.email }}</p>
        </div>
        <button class="logout-btn" @click="handleLogout" title="Sign out">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>

      <div v-else class="signin-prompt">
        <p class="signin-text">Sign in to personalize your experience</p>
        <router-link to="/login" class="btn-primary" @click="$emit('close')">
          Sign In
        </router-link>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useMatchStore } from '@/stores/matches'
import { storeToRefs } from 'pinia'

defineProps({ open: Boolean })
defineEmits(['close'])

const authStore = useAuthStore()
const matchStore = useMatchStore()
const { liveMatches } = storeToRefs(matchStore)
const liveMatchCount = computed(() => liveMatches.value?.length || 0)

const primaryNav = [
  { path: '/', label: 'Home', icon: '⌂' },
  { path: '/live', label: 'Live', icon: '▶', badge: true },
]

const exploreNav = [
  { path: '/competitions', label: 'Competitions', icon: '⬡' },
  { path: '/polls', label: 'Polls', icon: '◫' },
  { path: '/news', label: 'News', icon: '◈' },
]

function handleLogout() {
  authStore.logout()
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: var(--sidebar-w);
  height: 100vh;
  background: var(--c-surface);
  border-right: 1px solid var(--c-border);
  display: flex;
  flex-direction: column;
  z-index: 50;
  padding-top: var(--nav-h);
  transition: transform var(--transition);
}

@media (max-width: 1024px) {
  .sidebar {
    transform: translateX(-100%);
    padding-top: 0;
  }
  .sidebar.open {
    transform: translateX(0);
    box-shadow: 4px 0 40px rgba(0,0,0,0.5);
  }
}

/* ─── Logo ─────────────────────────────────────────────────── */
.sidebar-logo {
  display: none;
  align-items: center;
  gap: 10px;
  padding: 20px 20px 16px;
  border-bottom: 1px solid var(--c-border);
}

@media (max-width: 1024px) {
  .sidebar-logo { display: flex; }
}

.logo-mark {
  font-size: 22px;
}

.logo-text {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 0.04em;
  color: var(--c-text);
}

/* ─── Nav ──────────────────────────────────────────────────── */
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.nav-section {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--c-text-faint);
  padding: 0 12px 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: var(--radius-md);
  text-decoration: none;
  color: var(--c-text-muted);
  font-size: 14px;
  font-weight: 500;
  position: relative;
  transition: all var(--transition);
  cursor: pointer;
}

.nav-item:hover {
  background: var(--c-surface-2);
  color: var(--c-text);
  transform: translateX(3px);
}

.nav-item.active {
  background: var(--c-accent-dim);
  color: var(--c-accent);
  font-weight: 600;
}

.nav-icon {
  font-size: 17px;
  width: 22px;
  text-align: center;
  flex-shrink: 0;
  transition: transform var(--transition);
}

.nav-item:hover .nav-icon { transform: scale(1.15); }

.nav-text { flex: 1; }

.active-bar {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 60%;
  background: var(--c-accent);
  border-radius: 0 3px 3px 0;
  box-shadow: 0 0 8px var(--c-accent);
}

/* ─── Live Badge ───────────────────────────────────────────── */
.live-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  background: var(--c-live-dim);
  border: 1px solid rgba(255,61,87,0.25);
  border-radius: 99px;
  font-size: 10px;
  font-weight: 700;
  color: var(--c-live);
  letter-spacing: 0.04em;
}

.live-dot {
  width: 5px;
  height: 5px;
  background: var(--c-live);
  border-radius: 50%;
  animation: live-pulse 1.8s infinite;
}

/* ─── Footer ───────────────────────────────────────────────── */
.sidebar-footer {
  padding: 12px;
  border-top: 1px solid var(--c-border);
}

.user-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: var(--c-surface-2);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-md);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--c-accent), var(--c-accent-2));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 15px;
  color: #000;
  flex-shrink: 0;
}

.user-info { flex: 1; min-width: 0; }

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--c-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  font-size: 11px;
  color: var(--c-text-faint);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.logout-btn {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--c-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  color: var(--c-text-faint);
  transition: all var(--transition);
  flex-shrink: 0;
}

.logout-btn svg { width: 14px; height: 14px; }

.logout-btn:hover {
  background: rgba(255,61,87,0.1);
  border-color: rgba(255,61,87,0.3);
  color: var(--c-live);
}

.signin-prompt {
  text-align: center;
  padding: 8px 0;
}

.signin-text {
  font-size: 12px;
  color: var(--c-text-muted);
  margin-bottom: 10px;
  line-height: 1.5;
}
</style>