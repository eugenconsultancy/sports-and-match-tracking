<template>
  <!-- Live-pulse line at very top -->
  <div class="live-top-bar" aria-hidden="true"></div>

  <nav
    ref="navRef"
    class="nav-shell"
    :class="{
      'nav-scrolled': scrolled,
      'nav-hidden': navHidden,
      'dark-theme': isDark,
    }"
  >
    <div class="nav-container">
      <!-- ── Logo ────────────────────────────────────────── -->
      <router-link to="/" class="nav-logo group" aria-label="LiveScore Home">
        <div class="logo-icon logo-glow">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/><path d="M12 2a9.96 9.96 0 0 1 6.29 2.23L12 10.36 5.71 4.23A9.96 9.96 0 0 1 12 2z"/>
          </svg>
        </div>
        <span class="logo-label">LiveScore</span>
      </router-link>

      <!-- ── Desktop Nav ─────────────────────────────────── -->
      <div class="desktop-nav" role="navigation" aria-label="Main navigation">
        <div class="nav-track">
          <!-- Sliding active pill -->
          <div
            class="active-pill"
            :style="pillStyle"
            aria-hidden="true"
          ></div>

          <router-link
            v-for="(item, idx) in navItems"
            :key="item.path"
            :ref="el => { if (el) navLinkRefs[idx] = el }"
            :to="item.path"
            class="nav-link"
            :class="{ 'nav-link--active': isActive(item.path) }"
            :aria-current="isActive(item.path) ? 'page' : undefined"
            @click="updatePill(idx)"
          >
            <component :is="item.icon" class="nav-icon" aria-hidden="true" />
            <span class="nav-label">{{ item.label }}</span>

            <!-- Live badge with count -->
            <span v-if="item.badge && liveMatchCount > 0" class="live-badge">
              <span class="live-dot"></span>
              {{ liveMatchCount }}
            </span>
          </router-link>
        </div>
      </div>

      <!-- ── Right Actions ───────────────────────────────── -->
      <div class="nav-actions">
        <!-- Desktop search with ⌘K hint -->
        <button
          class="search-btn hidden sm:flex"
          aria-label="Open search (⌘K)"
          @click="uiStore.openSearch"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
          </svg>
          <span class="search-placeholder">Search...</span>
          <kbd class="kbd-hint">⌘K</kbd>
        </button>

        <!-- Mobile search -->
        <button
          class="icon-btn sm:hidden"
          aria-label="Search"
          @click="uiStore.openSearch"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
          </svg>
        </button>

        <!-- Notifications -->
        <NotificationBell />

        <!-- Authenticated user menu -->
        <div v-if="authStore.isAuthenticated" class="user-menu-wrap" ref="userMenuRef">
          <button
            class="avatar-btn"
            :aria-expanded="showUserMenu"
            aria-haspopup="true"
            @click="showUserMenu = !showUserMenu"
          >
            <!-- Avatar with gradient ring -->
            <div class="avatar-ring">
              <span class="avatar-initial">{{ userInitial }}</span>
            </div>
            <!-- Online status dot -->
            <span class="status-dot" aria-hidden="true"></span>
            <!-- Name on large screens -->
            <span class="avatar-name hidden xl:block">{{ displayName }}</span>
            <svg
              class="w-3.5 h-3.5 text-gray-400 transition-transform duration-200"
              :class="{ 'rotate-180': showUserMenu }"
              fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"
            >
              <path d="M19 9l-7 7-7-7"/>
            </svg>
          </button>

          <!-- Dropdown -->
          <Transition name="dropdown-spring">
            <div v-if="showUserMenu" class="user-dropdown" role="menu" aria-label="User menu">
              <!-- User info card -->
              <div class="dropdown-user-card">
                <div class="avatar-ring avatar-ring--lg">
                  <span class="avatar-initial avatar-initial--lg">{{ userInitial }}</span>
                </div>
                <div class="min-w-0">
                  <p class="dropdown-user-name">{{ displayName }}</p>
                  <p class="dropdown-user-email">{{ authStore.user?.email }}</p>
                  <p v-if="memberSince" class="dropdown-user-since">Member since {{ memberSince }}</p>
                </div>
              </div>

              <div class="dropdown-divider" aria-hidden="true"></div>

              <!-- Sign Out -->
              <button class="dropdown-item dropdown-item--danger" role="menuitem" @click="handleLogout">
                <svg class="dropdown-item-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                </svg>
                Sign Out
              </button>
            </div>
          </Transition>
        </div>

        <!-- Sign In -->
        <router-link v-else to="/login" class="signin-btn">
          <span class="hidden sm:inline">Sign In</span>
          <svg class="w-5 h-5 sm:hidden" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/>
          </svg>
        </router-link>

        <!-- Mobile hamburger -->
        <button
          class="icon-btn md:hidden"
          :aria-expanded="showMobileMenu"
          aria-label="Toggle menu"
          @click="showMobileMenu = !showMobileMenu"
        >
          <svg class="w-5 h-5 transition-all duration-200" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/>
            <path v-else stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>
  </nav>

  <!-- ── Mobile Drawer ──────────────────────────────────── -->
  <Transition name="drawer-slide">
    <div
      v-if="showMobileMenu"
      class="mobile-drawer md:hidden"
      :class="{ 'dark-theme': isDark }"
      role="dialog"
      aria-modal="true"
      aria-label="Mobile menu"
    >
      <div class="mobile-drawer-inner">
        <!-- User Info (if authenticated) -->
        <div v-if="authStore.isAuthenticated" class="mobile-user-card">
          <div class="avatar-ring avatar-ring--lg">
            <span class="avatar-initial avatar-initial--lg">{{ userInitial }}</span>
          </div>
          <div class="min-w-0">
            <p class="dropdown-user-name">{{ displayName }}</p>
            <p class="dropdown-user-email">{{ authStore.user?.email }}</p>
          </div>
        </div>

        <div v-if="authStore.isAuthenticated" class="dropdown-divider" aria-hidden="true"></div>

        <!-- Navigation Links -->
        <nav class="mobile-nav" aria-label="Mobile navigation">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="mobile-nav-link"
            :class="{ 'mobile-nav-link--active': isActive(item.path) }"
            @click="showMobileMenu = false"
          >
            <component :is="item.icon" class="w-5 h-5" />
            {{ item.label }}
            <span v-if="item.badge && liveMatchCount > 0" class="live-badge live-badge--sm ml-auto">
              <span class="live-dot"></span>
              {{ liveMatchCount }} LIVE
            </span>
          </router-link>
        </nav>

        <!-- Account Actions -->
        <div v-if="authStore.isAuthenticated" class="mobile-account-section">
          <p class="dropdown-section-label">Account</p>
          <button class="mobile-nav-link mobile-nav-link--danger" @click="handleLogout">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
            Sign Out
          </button>
        </div>

        <!-- Sign In (if not authenticated) -->
        <div v-else class="mobile-account-section">
          <router-link to="/login" class="signin-btn w-full text-center block" @click="showMobileMenu = false">
            Sign In
          </router-link>
        </div>
      </div>
    </div>
  </Transition>

  <!-- Drawer backdrop -->
  <Transition name="backdrop-fade">
    <div
      v-if="showMobileMenu"
      class="mobile-drawer-backdrop md:hidden"
      @click="showMobileMenu = false"
      aria-hidden="true"
    ></div>
  </Transition>

  <!-- Global Search -->
  <SearchModal v-if="uiStore.isSearchOpen" @close="uiStore.closeSearch" />
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useMatchStore } from '@/stores/matches'
import { useUIStore } from '@/stores/ui'
import { storeToRefs } from 'pinia'
import NotificationBell from '@/components/NotificationBell.vue'
import SearchModal from '@/components/SearchModal.vue'

// ── Icons as render functions (inline SVG components) ─────
const HomeIcon = { template: `<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>` }
const LiveIcon = { template: `<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8" fill="currentColor"/></svg>` }
const TrophyIcon = { template: `<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M6 9H4.5a2.5 2.5 0 010-5H6"/><path d="M18 9h1.5a2.5 2.5 0 000-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0012 0V2z"/></svg>` }
const PollIcon = { template: `<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>` }
const NewsIcon = { template: `<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/></svg>` }

const route = useRoute()
const authStore = useAuthStore()
const matchStore = useMatchStore()
const uiStore = useUIStore()
const { liveMatches } = storeToRefs(matchStore)

const showUserMenu  = ref(false)
const showMobileMenu = ref(false)
const userMenuRef   = ref(null)
const navRef        = ref(null)
const navLinkRefs   = ref([])
const scrolled      = ref(false)
const navHidden     = ref(false)

// Active pill position
const pillStyle = ref({ left: '0px', width: '0px' })

const isDark = computed(() =>
  typeof window !== 'undefined' && window.matchMedia('(prefers-color-scheme: dark)').matches
)

const liveMatchCount = computed(() => liveMatches.value?.length || 0)

const userInitial = computed(() => {
  const u = authStore.user
  if (u?.first_name) return u.first_name.charAt(0).toUpperCase()
  if (u?.email)      return u.email.charAt(0).toUpperCase()
  return 'U'
})

const displayName = computed(() => {
  const u = authStore.user
  if (u?.first_name) return u.first_name
  if (u?.email)      return u.email.split('@')[0]
  return 'User'
})

const memberSince = computed(() => {
  const d = authStore.user?.date_joined
  return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', year: 'numeric' }) : ''
})

const navItems = [
  { path: '/',             label: 'Home',         icon: HomeIcon  },
  { path: '/live',         label: 'Live',         icon: LiveIcon, badge: true },
  { path: '/competitions', label: 'Competitions', icon: TrophyIcon },
  { path: '/polls',        label: 'Polls',        icon: PollIcon  },
  { path: '/news',         label: 'News',         icon: NewsIcon  },
]

function isActive(path) {
  return route.path === path
}

// ── Active pill logic ────────────────────────────────────
async function updatePill(idx) {
  await nextTick()
  const el = navLinkRefs.value[idx]?.$el || navLinkRefs.value[idx]
  if (!el) return
  const track = el.parentElement
  const trackRect = track.getBoundingClientRect()
  const elRect = el.getBoundingClientRect()
  pillStyle.value = {
    left:  (elRect.left - trackRect.left) + 'px',
    width: elRect.width + 'px',
  }
}

onMounted(async () => {
  await nextTick()
  const activeIdx = navItems.findIndex(i => isActive(i.path))
  if (activeIdx >= 0) updatePill(activeIdx)
})

// ── Smart scroll hide/show ───────────────────────────────
let lastScroll = 0
function handleScroll() {
  const current = window.scrollY
  scrolled.value = current > 10

  if (current > lastScroll && current > 80) {
    navHidden.value = true   // scrolling down
  } else {
    navHidden.value = false  // scrolling up
  }
  lastScroll = current
}

// ── Keyboard ─────────────────────────────────────────────
function handleKeyboard(e) {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault()
    uiStore.openSearch()
  }
  if (e.key === 'Escape') {
    showUserMenu.value = false
    showMobileMenu.value = false
  }
}

// ── Click outside ─────────────────────────────────────────
function handleClickOutside(e) {
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
    showUserMenu.value = false
  }
}

function handleLogout() {
  showUserMenu.value   = false
  showMobileMenu.value = false
  authStore.logout()
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeyboard)
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeyboard)
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
/* ─────────────────────────────────────────────────────────
   LIVE TOP BAR
───────────────────────────────────────────────────────── */
.live-top-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, #ef4444, #f97316, #ef4444);
  z-index: 9999;
  animation: top-pulse 2.5s ease-in-out infinite;
}

@keyframes top-pulse {
  0%, 100% { opacity: 0.7; }
  50%       { opacity: 1; }
}

/* ─────────────────────────────────────────────────────────
   SHELL (floating frame)
───────────────────────────────────────────────────────── */
.nav-shell {
  position: fixed;
  top: 0.5rem;
  left: 0.75rem;
  right: 0.75rem;
  z-index: 5000;
  transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.2s ease;
}

@media (min-width: 768px) {
  .nav-shell {
    left: 1rem;
    right: 1rem;
  }
}

@media (min-width: 1024px) {
  .nav-shell {
    left: 2rem;
    right: 2rem;
  }
}

.nav-hidden {
  transform: translateY(calc(-100% - 0.75rem));
}

/* ─────────────────────────────────────────────────────────
   INNER CONTAINER
───────────────────────────────────────────────────────── */
.nav-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 3.5rem;
  padding: 0 1rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-radius: 1rem;
  border: 1px solid rgba(255,255,255,0.8);
  box-shadow: 0 4px 16px rgba(0,0,0,0.06), 0 1px 4px rgba(0,0,0,0.04);
  transition: box-shadow 0.2s ease;
}

@media (min-width: 768px) {
  .nav-container {
    padding: 0 1.5rem;
    border-radius: 1.25rem;
  }
}

.nav-scrolled .nav-container {
  box-shadow: 0 8px 32px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.06);
}

/* ─────────────────────────────────────────────────────────
   LOGO
───────────────────────────────────────────────────────── */
.nav-logo {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  text-decoration: none;
  flex-shrink: 0;
}

.logo-icon {
  width: 2.25rem;
  height: 2.25rem;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(99,102,241,0.35);
  transition: box-shadow 0.25s ease, transform 0.25s ease;
}

.logo-glow:hover {
  box-shadow: 0 0 20px rgba(99,102,241,0.6), 0 2px 8px rgba(99,102,241,0.35);
  transform: scale(1.07);
}

.logo-label {
  font-size: 1.125rem;
  font-weight: 800;
  color: #111827;
  letter-spacing: -0.02em;
  display: none;
}

@media (min-width: 640px) { 
  .logo-label { display: block; } 
}

/* ─────────────────────────────────────────────────────────
   DESKTOP NAV TRACK + PILL
───────────────────────────────────────────────────────── */
.desktop-nav {
  display: none;
}

@media (min-width: 768px) {
  .desktop-nav { 
    display: flex; 
    align-items: center; 
  }
}

.nav-track {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.125rem;
  background: #f3f4f6;
  border-radius: 0.75rem;
  padding: 0.25rem;
}

/* Sliding active pill */
.active-pill {
  position: absolute;
  top: 0.25rem;
  bottom: 0.25rem;
  background: #fff;
  border-radius: 0.5rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
  transition: left 0.28s cubic-bezier(0.22, 1, 0.36, 1), width 0.28s cubic-bezier(0.22, 1, 0.36, 1);
  pointer-events: none;
}

.nav-link {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #6b7280;
  text-decoration: none;
  white-space: nowrap;
  transition: color 0.2s ease;
  z-index: 1;
}

.nav-link:hover { color: #111827; }
.nav-link--active { color: #4f46e5; }

.nav-icon {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
}

.nav-label {
  display: none;
}

@media (min-width: 1024px) {
  .nav-label { display: inline; }
}

/* ─────────────────────────────────────────────────────────
   LIVE BADGE
───────────────────────────────────────────────────────── */
.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.125rem 0.5rem;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: #fff;
  font-size: 0.625rem;
  font-weight: 700;
  border-radius: 999px;
  letter-spacing: 0.02em;
  animation: badge-glow 2s ease-in-out infinite;
}

.live-badge--sm { 
  font-size: 0.65rem;
  padding: 0.125rem 0.625rem;
}

@keyframes badge-glow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
  50% { box-shadow: 0 0 0 4px rgba(239, 68, 68, 0); }
}

.live-dot {
  width: 5px;
  height: 5px;
  background: #fff;
  border-radius: 50%;
  animation: live-pulse 1.5s ease-in-out infinite;
}

@keyframes live-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.6; transform: scale(0.7); }
}

/* ─────────────────────────────────────────────────────────
   RIGHT ACTIONS
───────────────────────────────────────────────────────── */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 0.75rem;
  border: none;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}

.icon-btn:hover { background: #f3f4f6; color: #111827; }

.search-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4375rem 0.875rem;
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
  background: #f9fafb;
  color: #6b7280;
  font-size: 0.8125rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.search-btn:hover {
  background: #fff;
  border-color: #d1d5db;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
}

.search-placeholder {
  color: #9ca3af;
  font-size: 0.8125rem;
}

.kbd-hint {
  padding: 0.125rem 0.375rem;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 0.7rem;
  color: #9ca3af;
  background: #fff;
  font-weight: 500;
}

/* ─────────────────────────────────────────────────────────
   AVATAR + USER MENU
───────────────────────────────────────────────────────── */
.user-menu-wrap {
  position: relative;
}

.avatar-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.5rem;
  border-radius: 0.875rem;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: background 0.15s ease;
  position: relative;
}

.avatar-btn:hover { background: #f3f4f6; }

.avatar-ring {
  position: relative;
  width: 2.125rem;
  height: 2.125rem;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 0 2px #fff, 0 2px 6px rgba(99,102,241,0.3);
}

.avatar-ring--lg {
  width: 2.75rem;
  height: 2.75rem;
  flex-shrink: 0;
}

.avatar-initial {
  font-size: 0.8125rem;
  font-weight: 700;
  color: #fff;
}

.avatar-initial--lg { font-size: 1rem; }

.status-dot {
  position: absolute;
  bottom: 2px;
  left: 1.5rem;
  width: 8px;
  height: 8px;
  background: #22c55e;
  border: 2px solid #fff;
  border-radius: 50%;
}

.avatar-name {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #374151;
}

/* ─────────────────────────────────────────────────────────
   DROPDOWN
───────────────────────────────────────────────────────── */
.user-dropdown {
  position: absolute;
  right: 0;
  top: calc(100% + 0.5rem);
  width: 14rem;
  background: #fff;
  border-radius: 1rem;
  border: 1px solid rgba(229,231,235,0.8);
  box-shadow: 0 20px 40px rgba(0,0,0,0.12), 0 4px 12px rgba(0,0,0,0.06);
  overflow: hidden;
  z-index: 100;
}

.dropdown-user-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: linear-gradient(to right, #f9fafb, #fff);
}

.dropdown-user-name {
  font-size: 0.875rem;
  font-weight: 700;
  color: #111827;
  line-height: 1.2;
}

.dropdown-user-email {
  font-size: 0.75rem;
  color: #6b7280;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-user-since {
  font-size: 0.65rem;
  color: #9ca3af;
  margin-top: 2px;
}

.dropdown-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, #e5e7eb, transparent);
  margin: 0.125rem 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  width: 100%;
  padding: 0.625rem 1rem;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #374151;
  background: transparent;
  border: none;
  cursor: pointer;
  text-decoration: none;
  transition: background 0.12s ease, color 0.12s ease;
}

.dropdown-item:hover { background: #f9fafb; color: #111827; }

.dropdown-item--danger { color: #ef4444; }
.dropdown-item--danger:hover { background: #fef2f2; color: #dc2626; }

.dropdown-item-icon { width: 1rem; height: 1rem; color: #9ca3af; flex-shrink: 0; }

/* ─────────────────────────────────────────────────────────
   SIGN IN BUTTON
───────────────────────────────────────────────────────── */
.signin-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1.125rem;
  border-radius: 0.75rem;
  background: linear-gradient(135deg, #4f46e5, #6366f1);
  color: #fff;
  font-size: 0.8125rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(79,70,229,0.35);
}

.signin-btn:hover {
  background: linear-gradient(135deg, #4338ca, #4f46e5);
  box-shadow: 0 4px 14px rgba(79,70,229,0.45);
  transform: translateY(-1px);
}

/* ─────────────────────────────────────────────────────────
   MOBILE DRAWER
───────────────────────────────────────────────────────── */
.mobile-drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: min(85vw, 320px);
  background: #fff;
  z-index: 4999;
  box-shadow: -8px 0 32px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.mobile-drawer-inner {
  padding: 5rem 1.25rem 2rem;
}

.mobile-drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.35);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 4998;
}

.mobile-user-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0 1rem;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 0.875rem;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #374151;
  text-decoration: none;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
  width: 100%;
  text-align: left;
}

.mobile-nav-link:hover { background: #f9fafb; }
.mobile-nav-link--active { background: #eef2ff; color: #4f46e5; }
.mobile-nav-link--danger { color: #ef4444; }
.mobile-nav-link--danger:hover { background: #fef2f2; }

.mobile-account-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f3f4f6;
}

.dropdown-section-label {
  padding: 0.25rem 0 0.5rem;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #9ca3af;
}

/* ─────────────────────────────────────────────────────────
   TRANSITIONS
───────────────────────────────────────────────────────── */
.dropdown-spring-enter-active {
  transition: opacity 0.2s ease, transform 0.22s cubic-bezier(0.22,1,0.36,1);
}
.dropdown-spring-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.dropdown-spring-enter-from { opacity: 0; transform: translateY(-8px) scale(0.96); }
.dropdown-spring-leave-to   { opacity: 0; transform: translateY(-6px) scale(0.98); }

.drawer-slide-enter-active { transition: transform 0.32s cubic-bezier(0.22,1,0.36,1); }
.drawer-slide-leave-active { transition: transform 0.22s ease; }
.drawer-slide-enter-from   { transform: translateX(100%); }
.drawer-slide-leave-to     { transform: translateX(100%); }

.backdrop-fade-enter-active { transition: opacity 0.22s ease; }
.backdrop-fade-leave-active { transition: opacity 0.18s ease; }
.backdrop-fade-enter-from,
.backdrop-fade-leave-to     { opacity: 0; }

/* ─────────────────────────────────────────────────────────
   DARK THEME
───────────────────────────────────────────────────────── */
.dark-theme .nav-container {
  background: rgba(17,24,39,0.9);
  border-color: rgba(255,255,255,0.08);
  box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}

.dark-theme .logo-label { color: #f9fafb; }

.dark-theme .nav-track { background: rgba(255,255,255,0.06); }
.dark-theme .active-pill { background: rgba(255,255,255,0.15); }
.dark-theme .nav-link { color: #9ca3af; }
.dark-theme .nav-link:hover { color: #f3f4f6; }
.dark-theme .nav-link--active { color: #a5b4fc; }

.dark-theme .search-btn {
  background: rgba(255,255,255,0.06);
  border-color: rgba(255,255,255,0.1);
  color: #9ca3af;
}

.dark-theme .search-placeholder { color: #6b7280; }
.dark-theme .kbd-hint { 
  background: rgba(255,255,255,0.1);
  border-color: rgba(255,255,255,0.1);
  color: #6b7280;
}

.dark-theme .icon-btn { color: #9ca3af; }
.dark-theme .icon-btn:hover { background: rgba(255,255,255,0.08); color: #f3f4f6; }

.dark-theme .avatar-btn:hover { background: rgba(255,255,255,0.08); }
.dark-theme .avatar-name { color: #d1d5db; }
.dark-theme .status-dot { border-color: #1f2937; }

.dark-theme .user-dropdown {
  background: #1f2937;
  border-color: rgba(255,255,255,0.08);
  box-shadow: 0 20px 48px rgba(0,0,0,0.5);
}

.dark-theme .dropdown-user-card { background: linear-gradient(to right, #111827, #1f2937); }
.dark-theme .dropdown-user-name { color: #f9fafb; }
.dark-theme .dropdown-item { color: #d1d5db; }
.dark-theme .dropdown-item:hover { background: rgba(255,255,255,0.06); color: #f9fafb; }

.dark-theme .mobile-drawer { background: #111827; }
.dark-theme .mobile-nav-link { color: #d1d5db; }
.dark-theme .mobile-nav-link:hover { background: rgba(255,255,255,0.06); }
.dark-theme .mobile-nav-link--active { background: rgba(99,102,241,0.15); color: #a5b4fc; }
.dark-theme .mobile-account-section { border-color: rgba(255,255,255,0.06); }
.dark-theme .dropdown-divider { background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent); }
</style>