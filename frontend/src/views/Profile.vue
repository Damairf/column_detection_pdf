<template>
  <AppLayout>
    <div class="max-w-lg mx-auto mt-6">
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">

        <!-- Header card abu -->
        <div class="h-24 bg-gradient-to-r from-gray-700 to-gray-900"></div>

        <!-- Foto & Info -->
        <div class="px-8 pb-8">

          <!-- Avatar -->
          <div class="flex justify-center -mt-12 mb-4">
            <div class="w-24 h-24 rounded-full border-4 border-white shadow-md overflow-hidden bg-gray-200">
              <img
                src="/src/assets/avatar-default.jpg"
                alt="Foto Profil"
                class="w-full h-full object-cover"
              />
            </div>
          </div>

          <!-- Nama & Divisi -->
          <div class="text-center mb-6">
            <h2 class="text-xl font-bold text-gray-800">{{ form.nama || '-' }}</h2>
            <p class="text-sm text-gray-500">{{ form.divisi || '-' }}</p>
          </div>

          <!-- Mode Lihat -->
          <div class="space-y-3 mb-6">
            <!-- NAMA -->
            <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
              <div class="w-8 h-8 rounded-lg bg-gray-200 flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-400 leading-none mb-0.5">Nama</p>
                <p class="text-sm font-semibold text-gray-700">{{ form.nama || '-' }}</p>
              </div>
            </div>

            <!-- DIVISI -->
            <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
              <div class="w-8 h-8 rounded-lg bg-gray-200 flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-400 leading-none mb-0.5">Divisi</p>
                <p class="text-sm font-semibold text-gray-700">{{ form.divisi || '-' }}</p>
              </div>
            </div>

            <!-- ROLE -->
            <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
              <div class="w-8 h-8 rounded-lg bg-gray-200 flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-400 leading-none mb-0.5">Role</p>
                <p class="text-sm font-semibold text-gray-700 capitalize">{{ form.role || '-' }}</p>
              </div>
            </div>

            <!-- USERNAME -->
            <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
              <div class="w-8 h-8 rounded-lg bg-gray-200 flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-400 leading-none mb-0.5">Username</p>
                <p class="text-sm font-semibold text-gray-700">{{ form.username || '-' }}</p>
              </div>
            </div>
          </div>

          <!-- Tombol Keluar -->
          <div class="flex flex-col gap-2">
            <button
              @click="handleKeluar"
              class="cursor-pointer w-full py-2.5 rounded-xl font-semibold text-sm text-white bg-red-600 hover:bg-red-800 transition-all duration-200 active:scale-95"
            >
              Keluar
            </button>
          </div>

        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'

const router = useRouter()

const form = reactive({
  nama: '',
  divisi: '',
  username: '',
  role: ''
})

onMounted(() => {
  const stored = localStorage.getItem('user')
  if (stored) {
    const user = JSON.parse(stored)
    form.nama = user.nama || ''
    form.divisi = user.divisi || ''
    form.username = user.username || ''
    form.role = user.role || ''
  }
})

function handleKeluar() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.replace('/masuk')
}
</script>