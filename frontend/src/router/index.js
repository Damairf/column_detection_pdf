import { createRouter, createWebHistory } from 'vue-router'
import Masuk from '../views/Masuk.vue'
import Daftar from '../views/Daftar.vue'
import Beranda from '../views/Beranda.vue'
import Template from '../views/Template.vue'
import TemplateTambah from '../views/TemplateTambah.vue'
import TemplateDetail from '../views/TemplateDetail.vue'
import TemplateDetailUbah from '../views/TemplateDetailUbah.vue'
import KolomBaru from '../views/KolomBaru.vue'
import KolomEdit from '../views/KolomEdit.vue'
import Profile from '../views/Profile.vue'

const routes = [
  { path: '/', redirect: '/masuk' },
  { path: '/masuk',   name: 'Masuk',   component: Masuk,   meta: { guestOnly: true } },
  { path: '/daftar',  name: 'Daftar',  component: Daftar,  meta: { guestOnly: true } },
  { path: '/beranda', name: 'Beranda', component: Beranda, meta: { requiresAuth: true } },

  { path: '/template',        name: 'Template',       component: Template,       meta: { requiresAuth: true } },
  { path: '/template/tambah', name: 'TemplateTambah', component: TemplateTambah, meta: { requiresAuth: true } },

  // Halaman kolom baru & edit — dipakai dari dua konteks berbeda via query param ?mode=tambah|detail&id=
  { path: '/kolom/baru', name: 'KolomBaru', component: KolomBaru, meta: { requiresAuth: true } },
  { path: '/kolom/edit', name: 'KolomEdit', component: KolomEdit, meta: { requiresAuth: true } },

  { path: '/template/detail/:id',      name: 'TemplateDetail',     component: TemplateDetail,     meta: { requiresAuth: true } },
  { path: '/template/detail/:id/ubah', name: 'TemplateDetailUbah', component: TemplateDetailUbah, meta: { requiresAuth: true } },

  { path: '/profile',      name: 'Profile',     component: Profile, meta: { requiresAuth: true } },
  { path: '/profile/ubah', name: 'ProfileUbah', component: Profile, meta: { requiresAuth: true } },
]

const router = createRouter({ history: createWebHistory(), routes })

function isTokenValid() {
  const token = localStorage.getItem('token')
  if (!token) return false
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const now = Math.floor(Date.now() / 1000)
    if (payload.exp && payload.exp < now) {
      localStorage.removeItem('token'); localStorage.removeItem('user'); return false
    }
    return true
  } catch {
    localStorage.removeItem('token'); localStorage.removeItem('user'); return false
  }
}

router.beforeEach((to, from, next) => {
  const isLoggedIn = isTokenValid()
  if (to.meta.requiresAuth && !isLoggedIn) return next({ name: 'Masuk', replace: true })
  if (to.meta.guestOnly && isLoggedIn) {
    if (from.meta?.requiresAuth) { localStorage.removeItem('token'); localStorage.removeItem('user'); return next() }
    return next({ name: 'Beranda', replace: true })
  }
  next()
})

export default router