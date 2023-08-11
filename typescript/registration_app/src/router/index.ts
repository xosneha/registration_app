import { createRouter, createWebHistory } from 'vue-router'
import Registration from '../components/pages/Registration.vue'
import Login from '../components/pages/Login.vue'
import Profile from '../components/pages/Profile.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Registration
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile
    }
  ]
})

export default router
