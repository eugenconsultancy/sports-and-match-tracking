<template>
  <div class="app-root" :class="{ 'sidebar-open': sidebarOpen }">
    <!-- Navbar -->
    <Navbar @toggle-sidebar="sidebarOpen = !sidebarOpen" />

    <!-- Layout wrapper -->
    <div class="layout-wrapper">
      <!-- Sidebar -->
      <Sidebar :open="sidebarOpen" @close="sidebarOpen = false" />

      <!-- Overlay for mobile -->
      <Transition name="overlay">
        <div v-if="sidebarOpen" class="sidebar-overlay" @click="sidebarOpen = false" />
      </Transition>

      <!-- Main -->
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <Transition name="page" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </main>
    </div>

    <!-- Footer -->
    <footer class="app-footer">
      <div class="footer-inner">
        <div class="footer-grid">
          <!-- Brand -->
          <div class="footer-brand">
            <div class="brand-logo">
              <span class="brand-icon">⚽</span>
              <span class="brand-name">LiveScore</span>
            </div>
            <p class="brand-desc">Your ultimate destination for live football scores, real-time stats, and breaking news from around the world.</p>
            <div class="social-links">
              <a href="#" class="social-btn" aria-label="Twitter/X">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
              </a>
              <a href="#" class="social-btn" aria-label="Facebook">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
              </a>
              <a href="#" class="social-btn" aria-label="Instagram">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
              </a>
            </div>
          </div>

          <!-- Quick Links -->
          <div class="footer-col">
            <h4 class="footer-heading">Platform</h4>
            <ul class="footer-links">
              <li><router-link to="/">Home</router-link></li>
              <li><router-link to="/live">Live Scores</router-link></li>
              <li><router-link to="/competitions">Competitions</router-link></li>
              <li><router-link to="/news">News</router-link></li>
              <li><router-link to="/polls">Polls</router-link></li>
            </ul>
          </div>

          <!-- Company -->
          <div class="footer-col">
            <h4 class="footer-heading">Company</h4>
            <ul class="footer-links">
              <li><router-link to="/about">About Us</router-link></li>
              <li><router-link to="/contact">Contact</router-link></li>
              <li><router-link to="/terms">Terms of Service</router-link></li>
              <li><a href="#">Privacy Policy</a></li>
              <li><a href="#">Advertise With Us</a></li>
            </ul>
          </div>

          <!-- Newsletter -->
          <div class="footer-col">
            <h4 class="footer-heading">Stay Updated</h4>
            <p class="footer-note">Get match alerts and football news straight to your inbox.</p>
            <div class="newsletter-form">
              <input type="email" placeholder="your@email.com" class="newsletter-input" />
              <button class="newsletter-btn">→</button>
            </div>
          </div>
        </div>

        <div class="footer-bottom">
          <p class="copyright">© {{ new Date().getFullYear() }} LiveScore. All rights reserved.</p>
          <div class="footer-legal">
            <a href="#">Cookie Policy</a>
            <span>·</span>
            <a href="#">GDPR</a>
            <span>·</span>
            <a href="#">Accessibility</a>
          </div>
        </div>
      </div>
    </footer>

    <!-- Toast Stack -->
    <div class="toast-stack">
      <Toast v-for="toast in uiStore.toasts" :key="toast.id" :toast="toast" @close="uiStore.removeToast(toast.id)" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '@/components/Navbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import Toast from '@/components/ui/Toast.vue'
import { useAuthStore } from '@/stores/auth'
import { useMatchStore } from '@/stores/matches'
import { useUIStore } from '@/stores/ui'

const authStore = useAuthStore()
const matchStore = useMatchStore()
const uiStore = useUIStore()
const sidebarOpen = ref(false)

onMounted(() => {
  authStore.checkAuth()
  matchStore.connectToLiveMatches()
})
</script>

<style>
/* ─── Google Fonts ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800;900&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ─── Design Tokens ────────────────────────────────────────── */
:root {
  --c-bg:           #070b12;
  --c-surface:      #0e1420;
  --c-surface-2:    #141c2b;
  --c-surface-3:    #1c2638;
  --c-border:       rgba(255,255,255,0.07);
  --c-border-hover: rgba(255,255,255,0.14);
  --c-accent:       #00e676;
  --c-accent-dim:   rgba(0,230,118,0.12);
  --c-accent-2:     #00b8d4;
  --c-live:         #ff3d57;
  --c-live-dim:     rgba(255,61,87,0.15);
  --c-text:         #f0f4ff;
  --c-text-muted:   rgba(240,244,255,0.55);
  --c-text-faint:   rgba(240,244,255,0.28);
  --font-display:   'Barlow Condensed', sans-serif;
  --font-body:      'DM Sans', sans-serif;
  --radius-sm:      6px;
  --radius-md:      12px;
  --radius-lg:      18px;
  --radius-xl:      24px;
  --shadow-glow:    0 0 30px rgba(0,230,118,0.15);
  --shadow-card:    0 4px 24px rgba(0,0,0,0.4);
  --shadow-card-hover: 0 8px 40px rgba(0,0,0,0.6);
  --nav-h:          64px;
  --sidebar-w:      248px;
  --transition:     0.22s cubic-bezier(0.4,0,0.2,1);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  font-family: var(--font-body);
  background: var(--c-bg);
  color: var(--c-text);
  -webkit-font-smoothing: antialiased;
  min-height: 100vh;
}

/* ─── App Root ─────────────────────────────────────────────── */
.app-root {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* ─── Layout ───────────────────────────────────────────────── */
.layout-wrapper {
  display: flex;
  flex: 1;
  padding-top: var(--nav-h);
  position: relative;
}

.main-content {
  flex: 1;
  margin-left: var(--sidebar-w);
  min-width: 0;
  padding: 28px 32px 48px;
  max-width: 1440px;
}

@media (max-width: 1024px) {
  .main-content { margin-left: 0; padding: 20px 16px 40px; }
}

/* ─── Sidebar Overlay ──────────────────────────────────────── */
.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(4px);
  z-index: 40;
}

.overlay-enter-active, .overlay-leave-active { transition: opacity var(--transition); }
.overlay-enter-from, .overlay-leave-to { opacity: 0; }

/* ─── Page Transition ──────────────────────────────────────── */
.page-enter-active {
  transition: opacity 0.28s ease, transform 0.28s ease;
}
.page-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}
.page-enter-from { opacity: 0; transform: translateY(12px); }
.page-leave-to   { opacity: 0; transform: translateY(-6px); }

/* ─── Footer ───────────────────────────────────────────────── */
.app-footer {
  background: var(--c-surface);
  border-top: 1px solid var(--c-border);
  margin-left: var(--sidebar-w);
}

@media (max-width: 1024px) {
  .app-footer { margin-left: 0; }
}

.footer-inner { max-width: 1440px; margin: 0 auto; padding: 48px 32px 24px; }

.footer-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr 1.2fr;
  gap: 40px;
  margin-bottom: 40px;
}

@media (max-width: 900px) {
  .footer-grid { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 580px) {
  .footer-grid { grid-template-columns: 1fr; }
  .footer-inner { padding: 32px 16px 20px; }
}

.footer-brand .brand-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.brand-icon { font-size: 24px; }

.brand-name {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 800;
  letter-spacing: 0.02em;
  color: var(--c-text);
}

.brand-desc {
  font-size: 13px;
  color: var(--c-text-muted);
  line-height: 1.7;
  margin-bottom: 20px;
}

.social-links { display: flex; gap: 10px; }

.social-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--c-surface-2);
  border: 1px solid var(--c-border);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--c-text-muted);
  transition: all var(--transition);
  text-decoration: none;
}

.social-btn svg { width: 16px; height: 16px; }

.social-btn:hover {
  background: var(--c-accent-dim);
  border-color: var(--c-accent);
  color: var(--c-accent);
  transform: translateY(-2px);
}

.footer-heading {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--c-accent);
  margin-bottom: 16px;
}

.footer-links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-links a {
  font-size: 13px;
  color: var(--c-text-muted);
  text-decoration: none;
  transition: color var(--transition);
}

.footer-links a:hover { color: var(--c-text); }

.footer-note {
  font-size: 13px;
  color: var(--c-text-muted);
  line-height: 1.6;
  margin-bottom: 14px;
}

.newsletter-form {
  display: flex;
  gap: 8px;
}

.newsletter-input {
  flex: 1;
  background: var(--c-surface-2);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-sm);
  padding: 9px 12px;
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--c-text);
  outline: none;
  transition: border-color var(--transition);
}

.newsletter-input::placeholder { color: var(--c-text-faint); }
.newsletter-input:focus { border-color: var(--c-accent); }

.newsletter-btn {
  width: 38px;
  height: 38px;
  background: var(--c-accent);
  color: #000;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.newsletter-btn:hover {
  background: #4cff9e;
  transform: scale(1.05);
}

.footer-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 20px;
  border-top: 1px solid var(--c-border);
  gap: 12px;
  flex-wrap: wrap;
}

.copyright {
  font-size: 12px;
  color: var(--c-text-faint);
}

.footer-legal {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: var(--c-text-faint);
}

.footer-legal a {
  color: var(--c-text-faint);
  text-decoration: none;
  transition: color var(--transition);
}
.footer-legal a:hover { color: var(--c-text-muted); }

/* ─── Toast Stack ──────────────────────────────────────────── */
.toast-stack {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* ─── Scrollbar ────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--c-surface-3); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--c-border-hover); }

/* ─── Global Utilities ─────────────────────────────────────── */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 20px;
  background: var(--c-accent);
  color: #000;
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 700;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  text-decoration: none;
  transition: all var(--transition);
  letter-spacing: 0.02em;
}

.btn-primary:hover {
  background: #4cff9e;
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(0,230,118,0.35);
}

.btn-ghost {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 20px;
  background: transparent;
  color: var(--c-text-muted);
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  border: 1px solid var(--c-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  text-decoration: none;
  transition: all var(--transition);
}

.btn-ghost:hover {
  border-color: var(--c-border-hover);
  color: var(--c-text);
  background: var(--c-surface-2);
}

.card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: all var(--transition);
}

.card:hover {
  border-color: var(--c-border-hover);
  box-shadow: var(--shadow-card);
}

.section-title {
  font-family: var(--font-display);
  font-size: 26px;
  font-weight: 800;
  letter-spacing: 0.02em;
  color: var(--c-text);
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.badge-live {
  background: var(--c-live-dim);
  color: var(--c-live);
  border: 1px solid rgba(255,61,87,0.3);
}

.badge-success {
  background: var(--c-accent-dim);
  color: var(--c-accent);
  border: 1px solid rgba(0,230,118,0.3);
}

.badge-default {
  background: var(--c-surface-3);
  color: var(--c-text-muted);
  border: 1px solid var(--c-border);
}

/* Live pulse dot */
@keyframes live-pulse {
  0%   { box-shadow: 0 0 0 0 rgba(255,61,87,0.7); }
  70%  { box-shadow: 0 0 0 8px rgba(255,61,87,0); }
  100% { box-shadow: 0 0 0 0 rgba(255,61,87,0); }
}

.live-dot {
  width: 8px;
  height: 8px;
  background: var(--c-live);
  border-radius: 50%;
  display: inline-block;
  animation: live-pulse 1.8s infinite;
}

/* Shimmer skeleton */
@keyframes shimmer {
  0%   { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}

.skeleton {
  background: linear-gradient(90deg, var(--c-surface-2) 25%, var(--c-surface-3) 50%, var(--c-surface-2) 75%);
  background-size: 800px 100%;
  animation: shimmer 1.6s infinite;
  border-radius: var(--radius-sm);
}
</style>