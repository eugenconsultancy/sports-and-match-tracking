<template>
  <div class="article-page" :class="{ 'dark-theme': isDark }">

    <!-- ── Reading Progress Bar ─────────────────────────── -->
    <div class="progress-track" aria-hidden="true">
      <div class="progress-fill" :style="{ width: readingProgress + '%' }"></div>
    </div>

    <!-- ── Loading ─────────────────────────────────────── -->
    <div v-if="loading" class="loading-center">
      <div class="loader-ring"></div>
    </div>

    <article v-else-if="article" class="article-shell fade-up">

      <!-- ══════════════════════════════════════════════════
           CINEMATIC HERO
      ═══════════════════════════════════════════════════ -->
      <header class="hero-wrapper">
        <div v-if="article.cover_image" class="hero-image-container">
          <!-- Parallax image -->
          <img
            ref="heroImgRef"
            :src="article.cover_image"
            :alt="article.title"
            class="hero-img"
          />
          <!-- Deep gradient overlay -->
          <div class="hero-overlay"></div>

          <!-- Badges + Title on image -->
          <div class="hero-text">
            <div class="hero-badges">
              <router-link v-if="article.category"
                           :to="`/news?category=${article.category.slug}`"
                           class="badge badge--glass">
                {{ article.category.name }}
              </router-link>
              <span v-if="article.is_breaking" class="badge badge--breaking">
                <span class="badge-dot"></span>
                Breaking
              </span>
              <span v-if="article.is_featured" class="badge badge--featured">Featured</span>
            </div>

            <h1 class="hero-title">{{ article.title }}</h1>
            <p v-if="article.subtitle" class="hero-subtitle">{{ article.subtitle }}</p>
          </div>
        </div>

        <!-- No-image fallback header -->
        <div v-else class="hero-no-image">
          <div class="hero-badges">
            <router-link v-if="article.category"
                         :to="`/news?category=${article.category.slug}`"
                         class="badge badge--glass">
              {{ article.category.name }}
            </router-link>
            <span v-if="article.is_breaking" class="badge badge--breaking">
              <span class="badge-dot"></span>
              Breaking
            </span>
          </div>
          <h1 class="hero-title hero-title--dark">{{ article.title }}</h1>
          <p v-if="article.subtitle" class="hero-subtitle hero-subtitle--dark">{{ article.subtitle }}</p>
        </div>
      </header>

      <!-- ── Body container ──────────────────────────────── -->
      <div class="article-body-wrap">

        <!-- ── Floating Side Actions (desktop) ───────────── -->
        <aside class="floating-actions hidden lg:flex" aria-label="Article actions">
          <button class="action-btn" title="Copy link" @click="copyLink">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
          </button>
          <button class="action-btn" title="Share on X" @click="shareArticle('twitter')">
            <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
          </button>
          <button class="action-btn" title="Share on Facebook" @click="shareArticle('facebook')">
            <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
          </button>
          <Transition name="fade">
            <span v-if="copied" class="copy-flash">✓</span>
          </Transition>
        </aside>

        <!-- ── Main content column ─────────────────────── -->
        <div class="article-main">

          <!-- ── Metadata bar ───────────────────────────── -->
          <div class="meta-bar fade-up-delay-1">
            <!-- Author -->
            <div class="meta-author">
              <div v-if="article.author_avatar" class="meta-avatar">
                <img :src="article.author_avatar" class="w-full h-full object-cover" />
              </div>
              <div v-else class="meta-avatar meta-avatar--initial">
                {{ article.author_name?.charAt(0) || 'A' }}
              </div>
              <span class="meta-author-name">{{ article.author_name || 'LiveScore Staff' }}</span>
            </div>

            <span class="meta-dot" aria-hidden="true">·</span>
            <time class="meta-text" :datetime="article.published_at">{{ formatDate(article.published_at) }}</time>
            <span class="meta-dot" aria-hidden="true">·</span>

            <!-- Reading time visual bar -->
            <div class="read-time-wrap" :title="`${article.reading_time_minutes} min read`">
              <div class="read-time-track">
                <div class="read-time-fill" :style="{ width: Math.min(readingProgress, 100) + '%' }"></div>
              </div>
              <span class="meta-text">{{ article.reading_time_minutes }} min</span>
            </div>

            <span class="meta-dot" aria-hidden="true">·</span>
            <span class="meta-text meta-views">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
              {{ article.view_count?.toLocaleString() }}
            </span>
          </div>

          <!-- ── Tags ────────────────────────────────────── -->
          <div v-if="article.tags?.length" class="tags-row fade-up-delay-2">
            <router-link
              v-for="tag in article.tags"
              :key="tag.id"
              :to="`/news?tag=${tag.slug}`"
              class="tag-chip"
            >
              #{{ tag.name }}
            </router-link>
          </div>

          <!-- ── Article Body (prose) ───────────────────── -->
          <div
            class="article-prose fade-up-delay-3"
            v-html="article.body"
          ></div>

          <!-- ── Inline callout example (you can use this in body via CMS) -->

          <!-- ── Related Entities ───────────────────────── -->
          <div v-if="hasRelatedEntities" class="related-section fade-up-delay-3">
            <h3 class="related-title">
              <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
              Related to this Article
            </h3>
            <div class="related-scroll">
              <router-link
                v-for="team in article.related_entities?.teams"
                :key="team.id"
                :to="`/team/${team.id}`"
                class="related-chip"
              >
                <img v-if="team.logo" :src="team.logo" class="w-6 h-6 object-contain" />
                {{ team.name }}
              </router-link>
              <router-link
                v-for="player in article.related_entities?.players"
                :key="player.id"
                :to="`/player/${player.id}`"
                class="related-chip"
              >
                <span class="related-chip-avatar">{{ player.name.charAt(0) }}</span>
                {{ player.name }}
              </router-link>
              <router-link
                v-for="match in article.related_entities?.matches"
                :key="match.id"
                :to="`/match/${match.id}`"
                class="related-chip"
              >
                ⚽ {{ match.home_team }} vs {{ match.away_team }}
              </router-link>
            </div>
          </div>

          <!-- ── Source Attribution ──────────────────────── -->
          <div v-if="article.source_name" class="source-row">
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
            Source:
            <a v-if="article.source_url" :href="article.source_url" target="_blank" rel="noopener" class="source-link">
              {{ article.source_name }}
            </a>
            <span v-else>{{ article.source_name }}</span>
          </div>

          <!-- ── Author Card ─────────────────────────────── -->
          <div class="author-card fade-up-delay-3">
            <div class="meta-avatar meta-avatar--initial meta-avatar--xl">
              {{ article.author_name?.charAt(0) || 'A' }}
            </div>
            <div>
              <p class="author-card-name">{{ article.author_name || 'LiveScore Staff' }}</p>
              <p class="author-card-role">Football analyst & journalist</p>
            </div>
          </div>

          <!-- ── Engagement / Share ─────────────────────── -->
          <div class="engage-bar">
            <div class="share-group">
              <span class="meta-text font-semibold">Share:</span>
              <button class="share-btn" @click="shareArticle('twitter')" title="Share on X">
                <svg width="17" height="17" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
              </button>
              <button class="share-btn" @click="shareArticle('facebook')" title="Share on Facebook">
                <svg width="17" height="17" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
              </button>
              <button class="share-btn" @click="copyLink" title="Copy link">
                <svg width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
              </button>
              <Transition name="fade">
                <span v-if="copied" class="copy-label">Link copied!</span>
              </Transition>
            </div>

            <router-link to="/news" class="back-btn">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M15 19l-7-7 7-7"/></svg>
              Back to News
            </router-link>
          </div>

        </div><!-- /article-main -->
      </div><!-- /article-body-wrap -->
    </article>

    <!-- ── Not Found ───────────────────────────────────── -->
    <div v-else class="not-found-card fade-up">
      <div class="text-6xl mb-4">📄</div>
      <h3>Article Not Found</h3>
      <p>This article may have been removed or the link is incorrect.</p>
      <router-link to="/news" class="back-btn back-btn--primary">Browse News</router-link>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axios'
import { formatDate } from '@/utils/formatters'

const route = useRoute()
const articleId = route.params.id

const loading         = ref(true)
const article         = ref(null)
const copied          = ref(false)
const readingProgress = ref(0)
const heroImgRef      = ref(null)

const isDark = computed(() =>
  typeof window !== 'undefined' && window.matchMedia('(prefers-color-scheme: dark)').matches
)

const hasRelatedEntities = computed(() => {
  if (!article.value?.related_entities) return false
  const e = article.value.related_entities
  return (e.teams?.length || e.players?.length || e.matches?.length || e.competitions?.length) > 0
})

// ── Share ────────────────────────────────────────────────
function shareArticle(platform) {
  const url   = window.location.href
  const title = article.value?.title || ''
  const urls  = {
    twitter:  `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`,
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
  }
  if (urls[platform]) window.open(urls[platform], '_blank', 'width=600,height=400')
}

async function copyLink() {
  try {
    await navigator.clipboard.writeText(window.location.href)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2200)
  } catch (e) { /* ignore */ }
}

// ── Scroll: reading progress + parallax ─────────────────
function handleScroll() {
  const scrollTop    = window.pageYOffset || document.documentElement.scrollTop
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight
  readingProgress.value = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0

  // Cinematic parallax
  if (heroImgRef.value) {
    const scale = 1.06 + scrollTop * 0.00025
    heroImgRef.value.style.transform = `scale(${Math.min(scale, 1.15)}) translateY(${scrollTop * 0.12}px)`
  }
}

onMounted(async () => {
  window.addEventListener('scroll', handleScroll, { passive: true })

  try {
    const res = await axios.get(`/api/v1/news/articles/${articleId}/`)
    article.value = res.data
  } catch (e) {
    console.error('Failed to load article:', e)
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
/* ─────────────────────────────────────────────────────────
   PAGE SHELL
───────────────────────────────────────────────────────── */
.article-page {
  max-width: 48rem;
  margin: 0 auto;
  padding: 0 1rem 4rem;
  /* Subtle radial background accent */
  background: radial-gradient(circle at 50% 0, rgba(99,102,241,0.05), transparent 60%);
}

/* ─────────────────────────────────────────────────────────
   PROGRESS BAR
───────────────────────────────────────────────────────── */
.progress-track {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: rgba(0,0,0,0.06);
  z-index: 9998;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(to right, #6366f1, #22c55e);
  box-shadow: 0 0 10px rgba(99,102,241,0.6);
  transition: width 0.15s ease;
}

/* ─────────────────────────────────────────────────────────
   LOADING
───────────────────────────────────────────────────────── */
.loading-center {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 40vh;
}

.loader-ring {
  width: 2.75rem;
  height: 2.75rem;
  border: 3px solid rgba(99,102,241,0.2);
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ─────────────────────────────────────────────────────────
   HERO
───────────────────────────────────────────────────────── */
.hero-wrapper {
  margin: 0 -1rem 2rem;
}

.hero-image-container {
  position: relative;
  height: min(60vh, 28rem);
  overflow: hidden;
  border-radius: 0 0 1.75rem 1.75rem;
}

.hero-img {
  width: 100%;
  height: 120%;
  object-fit: cover;
  transform-origin: center center;
  will-change: transform;
  /* starts slightly zoomed for parallax headroom */
  transform: scale(1.06);
  transition: transform 0.05s linear;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(0,0,0,0.85) 0%,
    rgba(0,0,0,0.4)  50%,
    rgba(0,0,0,0.05) 100%
  );
}

.hero-text {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 2rem 1.75rem;
}

.hero-no-image {
  padding: 3rem 1.75rem;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-radius: 0 0 1.75rem 1.75rem;
}

/* ─────────────────────────────────────────────────────────
   BADGES
───────────────────────────────────────────────────────── */
.hero-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.875rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-decoration: none;
  line-height: 1;
}

.badge--glass {
  background: rgba(255,255,255,0.2);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.3);
  color: #fff;
  transition: background 0.15s ease;
}
.badge--glass:hover { background: rgba(255,255,255,0.3); }

.badge--breaking {
  background: #ef4444;
  color: #fff;
}

.badge--featured {
  background: #fbbf24;
  color: #78350f;
}

.badge-dot {
  width: 6px;
  height: 6px;
  background: #fff;
  border-radius: 50%;
  animation: live-pulse 1.5s ease-in-out infinite;
}

@keyframes live-pulse {
  0%,100% { opacity: 1; }
  50%      { opacity: 0.4; }
}

/* ─────────────────────────────────────────────────────────
   HERO TITLE / SUBTITLE
───────────────────────────────────────────────────────── */
.hero-title {
  font-size: clamp(1.5rem, 4vw, 2.5rem);
  font-weight: 800;
  color: #fff;
  line-height: 1.18;
  letter-spacing: -0.025em;
  margin: 0 0 0.5rem;
}

.hero-title--dark { color: #fff; }
.hero-subtitle {
  font-size: 1.0625rem;
  color: rgba(255,255,255,0.8);
  margin: 0;
}

/* ─────────────────────────────────────────────────────────
   BODY LAYOUT
───────────────────────────────────────────────────────── */
.article-body-wrap {
  position: relative;
  display: flex;
  gap: 2rem;
}

.article-main {
  flex: 1;
  min-width: 0;
}

/* ─────────────────────────────────────────────────────────
   FLOATING SIDE ACTIONS
───────────────────────────────────────────────────────── */
.floating-actions {
  position: sticky;
  top: 6rem;
  flex-direction: column;
  gap: 0.625rem;
  width: 2.75rem;
  flex-shrink: 0;
  height: fit-content;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
  background: #fff;
  color: #6b7280;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  transition: color 0.15s ease, border-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
}

.action-btn:hover {
  color: #4f46e5;
  border-color: #c7d2fe;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(99,102,241,0.15);
}

.action-btn:active { transform: scale(0.9); }

.copy-flash {
  font-size: 0.75rem;
  color: #22c55e;
  font-weight: 700;
  text-align: center;
}

/* ─────────────────────────────────────────────────────────
   META BAR
───────────────────────────────────────────────────────── */
.meta-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.625rem;
  padding: 0.875rem 0;
  border-top: 1px solid #f3f4f6;
  border-bottom: 1px solid #f3f4f6;
  margin-bottom: 1.25rem;
}

.meta-author {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-avatar {
  width: 1.875rem;
  height: 1.875rem;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.meta-avatar--initial {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: #fff;
}

.meta-avatar--xl {
  width: 3rem;
  height: 3rem;
  font-size: 1rem;
}

.meta-author-name {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #111827;
}

.meta-dot { color: #d1d5db; font-size: 1rem; }
.meta-text {
  font-size: 0.8125rem;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.meta-views { gap: 0.3rem; }

/* Reading time visual track */
.read-time-wrap {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.read-time-track {
  width: 3.5rem;
  height: 3px;
  background: #e5e7eb;
  border-radius: 999px;
  overflow: hidden;
}

.read-time-fill {
  height: 100%;
  background: #6366f1;
  border-radius: 999px;
  transition: width 0.3s ease;
}

/* ─────────────────────────────────────────────────────────
   TAGS
───────────────────────────────────────────────────────── */
.tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.tag-chip {
  padding: 0.3125rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  background: #f3f4f6;
  text-decoration: none;
  transition: background 0.15s ease, color 0.15s ease, transform 0.15s ease;
}

.tag-chip:hover {
  background: #eef2ff;
  color: #4f46e5;
  transform: translateY(-2px);
}

/* ─────────────────────────────────────────────────────────
   ARTICLE PROSE
───────────────────────────────────────────────────────── */
.article-prose {
  font-size: 1.0625rem;
  line-height: 1.85;
  letter-spacing: 0.01em;
  color: #374151;
  margin-bottom: 2rem;
}

/* Drop cap on first paragraph */
.article-prose :deep(p:first-of-type::first-letter) {
  font-size: 3.25rem;
  font-weight: 800;
  float: left;
  margin-right: 0.25rem;
  line-height: 1;
  color: #4f46e5;
  padding-right: 4px;
}

.article-prose :deep(p) {
  margin-bottom: 1.5rem;
  color: #374151;
}

.article-prose :deep(h2) {
  font-size: 1.4375rem;
  font-weight: 800;
  margin-top: 2.5rem;
  margin-bottom: 1rem;
  color: #111827;
  border-left: 4px solid #6366f1;
  padding-left: 0.875rem;
  letter-spacing: -0.015em;
}

.article-prose :deep(h3) {
  font-size: 1.1875rem;
  font-weight: 700;
  margin-top: 2rem;
  margin-bottom: 0.75rem;
  color: #1f2937;
}

.article-prose :deep(a) {
  color: #4f46e5;
  text-decoration: underline;
  text-underline-offset: 3px;
  transition: color 0.15s ease;
}

.article-prose :deep(a:hover) { color: #4338ca; }

.article-prose :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 0.875rem;
  box-shadow: 0 6px 24px rgba(0,0,0,0.12);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: zoom-in;
}

.article-prose :deep(img:hover) {
  transform: scale(1.02);
  box-shadow: 0 12px 40px rgba(0,0,0,0.2);
}

/* Callout blocks (add class="callout" in CMS) */
.article-prose :deep(.callout) {
  background: #eef2ff;
  border-left: 4px solid #6366f1;
  padding: 1rem 1.25rem;
  border-radius: 0 0.625rem 0.625rem 0;
  margin: 1.5rem 0;
  font-size: 0.9375rem;
}

/* ─────────────────────────────────────────────────────────
   RELATED ENTITIES
───────────────────────────────────────────────────────── */
.related-section {
  background: #f9fafb;
  border-radius: 1rem;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
}

.related-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9375rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.875rem;
}

.related-scroll {
  display: flex;
  gap: 0.625rem;
  overflow-x: auto;
  padding-bottom: 0.25rem;
}

.related-scroll::-webkit-scrollbar { height: 4px; }
.related-scroll::-webkit-scrollbar-track { background: #f3f4f6; border-radius: 999px; }
.related-scroll::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 999px; }

.related-chip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.875rem;
  border-radius: 0.75rem;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  font-size: 0.8125rem;
  font-weight: 600;
  color: #374151;
  text-decoration: none;
  white-space: nowrap;
  transition: box-shadow 0.15s ease, transform 0.15s ease;
  flex-shrink: 0;
}

.related-chip:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.related-chip-avatar {
  width: 1.5rem;
  height: 1.5rem;
  background: #eef2ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: #4f46e5;
}

/* ─────────────────────────────────────────────────────────
   SOURCE ROW
───────────────────────────────────────────────────────── */
.source-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1rem;
  background: #f9fafb;
  border-radius: 0.75rem;
  font-size: 0.8125rem;
  color: #6b7280;
  margin-bottom: 1.5rem;
}

.source-link {
  color: #4f46e5;
  font-weight: 600;
  text-decoration: none;
}
.source-link:hover { text-decoration: underline; }

/* ─────────────────────────────────────────────────────────
   AUTHOR CARD
───────────────────────────────────────────────────────── */
.author-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: #f9fafb;
  border-radius: 1rem;
  margin-bottom: 1.5rem;
  border: 1px solid #f3f4f6;
}

.author-card-name {
  font-size: 0.9375rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.125rem;
}

.author-card-role {
  font-size: 0.8125rem;
  color: #6b7280;
  margin: 0;
}

/* ─────────────────────────────────────────────────────────
   ENGAGE BAR
───────────────────────────────────────────────────────── */
.engage-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding-top: 1.25rem;
  border-top: 1px solid #f3f4f6;
}

.share-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.share-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 0.625rem;
  border: 1px solid #e5e7eb;
  background: #f9fafb;
  color: #6b7280;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease, transform 0.15s ease;
}

.share-btn:hover { background: #eef2ff; color: #4f46e5; transform: translateY(-2px); }
.share-btn:active { transform: scale(0.88); }

.copy-label {
  font-size: 0.8125rem;
  color: #22c55e;
  font-weight: 600;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  border-radius: 0.625rem;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #6b7280;
  border: 1px solid #e5e7eb;
  background: #fff;
  text-decoration: none;
  transition: background 0.15s ease, color 0.15s ease;
}

.back-btn:hover { background: #f9fafb; color: #374151; }

.back-btn--primary {
  background: #4f46e5;
  color: #fff;
  border-color: transparent;
}

.back-btn--primary:hover { background: #4338ca; color: #fff; }

/* ─────────────────────────────────────────────────────────
   NOT FOUND
───────────────────────────────────────────────────────── */
.not-found-card {
  text-align: center;
  padding: 5rem 1rem;
}

.not-found-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #374151;
  margin: 0 0 0.5rem;
}

.not-found-card p {
  color: #6b7280;
  font-size: 0.9375rem;
  margin: 0 0 1.5rem;
}

/* ─────────────────────────────────────────────────────────
   ENTRANCE ANIMATIONS
───────────────────────────────────────────────────────── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}

.fade-up           { animation: fadeUp 0.6s ease forwards; }
.fade-up-delay-1   { animation: fadeUp 0.6s 0.1s ease both; }
.fade-up-delay-2   { animation: fadeUp 0.6s 0.18s ease both; }
.fade-up-delay-3   { animation: fadeUp 0.6s 0.26s ease both; }

/* ─────────────────────────────────────────────────────────
   TRANSITIONS
───────────────────────────────────────────────────────── */
.fade-enter-active { transition: opacity 0.2s ease; }
.fade-leave-active { transition: opacity 0.15s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* ─────────────────────────────────────────────────────────
   DARK THEME
───────────────────────────────────────────────────────── */
.dark-theme { background: radial-gradient(circle at 50% 0, rgba(99,102,241,0.07), transparent 60%) #0f172a; color: #e2e8f0; }

.dark-theme .meta-author-name, .dark-theme .hero-title--dark { color: #f1f5f9; }
.dark-theme .article-prose { color: #cbd5e1; }
.dark-theme .article-prose :deep(p) { color: #cbd5e1; }
.dark-theme .article-prose :deep(h2) { color: #f1f5f9; }
.dark-theme .article-prose :deep(h3) { color: #e2e8f0; }
.dark-theme .article-prose :deep(.callout) { background: rgba(99,102,241,0.1); }

.dark-theme .meta-bar { border-color: #1e293b; }
.dark-theme .tag-chip { background: #1e293b; color: #94a3b8; }
.dark-theme .tag-chip:hover { background: rgba(99,102,241,0.15); color: #818cf8; }

.dark-theme .related-section { background: #0f172a; }
.dark-theme .related-chip { background: #1e293b; color: #cbd5e1; }

.dark-theme .source-row, .dark-theme .author-card { background: #1e293b; border-color: #334155; }
.dark-theme .author-card-name { color: #f1f5f9; }

.dark-theme .engage-bar { border-color: #1e293b; }
.dark-theme .share-btn { background: #1e293b; border-color: #334155; color: #94a3b8; }
.dark-theme .back-btn  { background: #1e293b; border-color: #334155; color: #94a3b8; }

.dark-theme .action-btn { background: #1e293b; border-color: #334155; color: #94a3b8; }
.dark-theme .not-found-card h3 { color: #e2e8f0; }

/* ─────────────────────────────────────────────────────────
   RESPONSIVE
───────────────────────────────────────────────────────── */
@media (max-width: 640px) {
  .hero-image-container { height: min(55vw, 18rem); }
  .hero-text { padding: 1.25rem; }
  .meta-bar  { gap: 0.375rem; }
}
</style>