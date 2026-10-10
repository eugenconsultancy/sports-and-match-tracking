# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).


frontend/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── style.css
│   ├── axios.js
│   ├── router.js
│   ├── constants/
│   │   └── index.js
│   ├── validators/
│   │   └── index.js
│   ├── layouts/
│   │   ├── MainLayout.vue
│   │   └── AuthLayout.vue
│   ├── pages/
│   │   ├── HomePage.vue
│   │   ├── LiveMatchesPage.vue
│   │   ├── MatchPage.vue
│   │   ├── CompetitionsPage.vue
│   │   ├── CompetitionPage.vue
│   │   ├── TeamPage.vue
│   │   ├── PlayerPage.vue
│   │   ├── NewsPage.vue
│   │   ├── ArticlePage.vue
│   │   ├── LoginPage.vue
│   │   ├── SignupPage.vue
│   │   ├── FavoritesPage.vue
│   │   ├── SearchPage.vue
│   │   ├── SettingsPage.vue
│   │   └── NotFoundPage.vue
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Button.vue
│   │   │   ├── Card.vue
│   │   │   ├── Modal.vue
│   │   │   ├── Loader.vue
│   │   │   ├── Toast.vue
│   │   │   ├── Input.vue
│   │   │   ├── Badge.vue
│   │   │   ├── Tabs.vue
│   │   │   ├── Skeleton.vue
│   │   │   └── Dropdown.vue
│   │   ├── Navbar.vue
│   │   ├── Sidebar.vue
│   │   ├── LiveMatchBar.vue
│   │   ├── MatchWidget.vue
│   │   ├── NewsCard.vue
│   │   ├── PlayerStatsCard.vue
│   │   ├── PollWidget.vue
│   │   ├── StandingsTable.vue
│   │   ├── TeamCard.vue
│   │   ├── CompetitionCard.vue
│   │   ├── NotificationBell.vue
│   │   └── SearchModal.vue
│   ├── stores/
│   │   ├── auth.js
│   │   ├── matches.js
│   │   ├── competitions.js
│   │   ├── notifications.js
│   │   └── ui.js
│   ├── services/
│   │   ├── api.js
│   │   └── auth.js
│   ├── composables/
│   │   ├── useWebSocket.js
│   │   ├── useInfiniteScroll.js
│   │   └── useLocalStorage.js
│   ├── utils/
│   │   ├── formatters.js
│   │   └── websocket.js
│   └── assets/
│       ├── hero.png
│       ├── vite.svg
│       └── vue.svg