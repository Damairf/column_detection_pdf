<template>
  <div class="flex h-screen bg-gray-100 overflow-hidden">

    <aside class="w-56 bg-white flex flex-col shadow-md flex-shrink-0">

      <!-- Profile -->
      <div
        class="flex items-center gap-3 px-4 py-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 transition"
        @click="router.push('/profile')"
        title="Lihat Profile"
      >
        <div class="w-10 h-10 rounded-full overflow-hidden flex-shrink-0 bg-gray-200">
          <img src="/src/assets/avatar-default.jpg" alt="Avatar"
            class="w-full h-full object-cover" @error="handleAvatarError" ref="avatarImg" />
        </div>
        <div class="overflow-hidden">
          <p class="text-sm font-bold text-gray-800 truncate">{{ user.nama || 'Pengguna' }}</p>
          <p class="text-xs text-gray-500 truncate">{{ user.divisi || '-' }}</p>
        </div>
      </div>

      <nav class="flex-1 px-3 py-4 flex flex-col gap-1">

        <router-link to="/beranda"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150"
          :class="isActive('/beranda') ? 'bg-gray-900 text-white shadow' : 'text-gray-600 hover:bg-gray-100'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          Beranda
        </router-link>

        <router-link to="/template"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150"
          :class="isActive('/template') ? 'bg-gray-900 text-white shadow' : 'text-gray-600 hover:bg-gray-100'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Template
        </router-link>

        <router-link v-if="user.role === 'pusat'" to="/pengguna"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150"
          :class="isActive('/pengguna') ? 'bg-gray-900 text-white shadow' : 'text-gray-600 hover:bg-gray-100'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          Pengguna
        </router-link>

      </nav>
    </aside>

    <div class="flex flex-col flex-1 overflow-hidden">

      <header class="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-5 flex-shrink-0 shadow-sm">
        <div class="flex items-center gap-2">
          <span class="text-gray-300 mx-1">|</span>
          <div class="flex items-center gap-1.5 text-sm text-gray-600">
            <span class="text-gray-400">/</span>
            <span class="font-semibold text-gray-800">{{ pageTitle }}</span>
          </div>
        </div>
        <div class="flex items-center">
          <img src="/src/assets/logo-nasmoco.png" alt="Nasmoco" class="h-8 object-contain" />
        </div>
      </header>

      <main class="flex-1 overflow-auto p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router   = useRouter()
const route    = useRoute()
const avatarImg = ref(null)

const user = computed(() => {
  try { return JSON.parse(localStorage.getItem('user')) || {} }
  catch { return {} }
})

const pageTitle = computed(() => {
  const p    = route.path
  const mode = route.query.mode || ''
  const q    = mode === 'detail' ? 'Template / Detail / Ubah' : 'Template / Tambah'

  const map = {
    '/beranda':          'Beranda',
    '/beranda/tambah':   'Beranda / Tambah',
    '/template':         'Template',
    '/template/tambah':  'Template / Tambah',
    '/profile':          'Profile',
    '/profile/ubah':     'Profile / Ubah',
    '/pengguna':     'Pengguna',
  }
  if (map[p]) return map[p]

  if (p === '/kolom/baru') return `${q} / Kolom Baru`
  if (p === '/kolom/edit') return `${q} / Edit Kolom`

  if (/^\/beranda\/detail\/\d+$/.test(p)) return 'Beranda / Detail'

  if (/^\/template\/detail\/\d+$/.test(p))       return 'Template / Detail'
  if (/^\/template\/detail\/\d+\/ubah$/.test(p)) return 'Template / Detail / Ubah'

  return p.replace(/^\//, '')
})

function isActive(basePath) {
  if (basePath === '/template') {
    return route.path === '/template'
      || route.path.startsWith('/template/')
      || route.path === '/kolom/baru'
      || route.path === '/kolom/edit'
  }
  if (basePath === '/beranda') {
    return route.path === '/beranda'
      || route.path.startsWith('/beranda/')
  }
  return route.path === basePath || route.path.startsWith(basePath + '/')
}

function handleAvatarError() {
  if (avatarImg.value) avatarImg.value.style.display = 'none'
}
</script>