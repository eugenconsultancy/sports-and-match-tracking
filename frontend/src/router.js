import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('@/pages/HomePage.vue'),
    },
    {
        path: '/live',
        name: 'LiveMatches',
        component: () => import('@/pages/LiveMatchesPage.vue'),
    },
    {
        path: '/match/:id',
        name: 'MatchDetail',
        component: () => import('@/pages/MatchPage.vue'),
        props: true,
    },
    {
        path: '/competitions',
        name: 'Competitions',
        component: () => import('@/pages/CompetitionsPage.vue'),
    },
    {
        path: '/competition/:id',
        name: 'CompetitionDetail',
        component: () => import('@/pages/CompetitionPage.vue'),
        props: true,
    },
    {
        path: '/team/:id',
        name: 'TeamDetail',
        component: () => import('@/pages/TeamPage.vue'),
        props: true,
    },
    {
        path: '/player/:id',
        name: 'PlayerDetail',
        component: () => import('@/pages/PlayerPage.vue'),
        props: true,
    },
    {
        path: '/news',
        name: 'News',
        component: () => import('@/pages/NewsPage.vue'),
    },
    {
        path: '/news/:id',
        name: 'ArticleDetail',
        component: () => import('@/pages/ArticlePage.vue'),
        props: true,
    },
    // POLLS ROUTES
    {
        path: '/polls',
        name: 'Polls',
        component: () => import('@/pages/PollsPage.vue'),
    },
    {
        path: '/poll/:id',
        name: 'PollDetail',
        component: () => import('@/pages/PollPage.vue'),
        props: true,
    },
    // STATIC PAGES
    {
        path: '/about',
        name: 'About',
        component: () => import('@/pages/AboutPage.vue'),
    },
    {
        path: '/contact',
        name: 'Contact',
        component: () => import('@/pages/ContactPage.vue'),
    },
    {
        path: '/terms',
        name: 'Terms',
        component: () => import('@/pages/TermsPage.vue'),
    },
    {
        path: '/privacy',
        name: 'Privacy',
        component: () => import('@/pages/PrivacyPage.vue'),
    },
    // AUTH ROUTES
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/pages/LoginPage.vue'),
    },
    {
        path: '/signup',
        name: 'Signup',
        component: () => import('@/pages/SignupPage.vue'),
    },
    // USER ROUTES
    {
        path: '/favorites',
        name: 'Favorites',
        component: () => import('@/pages/FavoritesPage.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/search',
        name: 'Search',
        component: () => import('@/pages/SearchPage.vue'),
    },
    {
        path: '/settings',
        name: 'Settings',
        component: () => import('@/pages/SettingsPage.vue'),
        meta: { requiresAuth: true },
    },
    // 404 CATCH-ALL
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('@/pages/NotFoundPage.vue'),
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        }
        return { top: 0 }
    },
})

// Navigation guard for auth-required routes
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access_token')

    if (to.meta.requiresAuth && !token) {
        next({ name: 'Login', query: { redirect: to.fullPath } })
    } else {
        next()
    }
})

export default router