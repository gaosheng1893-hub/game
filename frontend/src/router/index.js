import { createRouter, createWebHistory } from 'vue-router'
import auth from '../services/auth.js'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/auth',
    name: 'Auth',
    component: () => import('../views/Auth.vue')
  },
  {
    path: '/map',
    name: 'Map',
    component: () => import('../views/Map.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/station/:id',
    name: 'Station',
    component: () => import('../views/Station.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/achievements',
    name: 'Achievements',
    component: () => import('../views/Achievements.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/lottery',
    name: 'Lottery',
    component: () => import('../views/Lottery.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/leaderboard',
    name: 'Leaderboard',
    component: () => import('../views/Leaderboard.vue'),
    meta: { requiresAuth: true }
  },
  // 管理后台路由
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: 'stations',
        name: 'AdminStations',
        component: () => import('../views/admin/Stations.vue')
      },
      {
        path: 'questions',
        name: 'AdminQuestions',
        component: () => import('../views/admin/Questions.vue')
      },
      {
        path: 'achievements',
        name: 'AdminAchievements',
        component: () => import('../views/admin/Achievements.vue')
      },
      {
        path: 'lottery',
        name: 'AdminLottery',
        component: () => import('../views/admin/Lottery.vue')
      },
      {
        path: 'prizes',
        name: 'AdminPrizes',
        component: () => import('../views/admin/Prizes.vue')
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('../views/admin/Users.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !auth.isAuthenticated()) {
    next('/auth')
  } else if (to.meta.requiresAdmin && !auth.isAdmin()) {
    next('/')
  } else {
    next()
  }
})

export default router