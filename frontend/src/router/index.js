import { createRouter, createWebHistory } from 'vue-router'
import LedgerList from '../views/LedgerList.vue'
import LedgerDetail from '../views/LedgerDetail.vue'
import UserList from '../views/UserList.vue'
import UserDetail from '../views/UserDetail.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: LedgerList
  },
  {
    path: '/ledger',
    name: 'ledger-list',
    component: LedgerList
  },
  {
    path: '/ledger/:id',
    name: 'ledger-detail',
    component: LedgerDetail
  },
  {
    path: '/users',
    name: 'user-list',
    component: UserList
  },
  {
    path: '/users/:id',
    name: 'user-detail',
    component: UserDetail
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/register',
    name: 'register',
    component: Register
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  next()
})

export default router