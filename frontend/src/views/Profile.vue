<template>
  <AppLayout>
    <div class="max-w-4xl mx-auto mt-6">
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col md:flex-row">

        <!-- Kiri: Foto, Nama, Divisi -->
        <div class="md:w-72 w-full bg-gradient-to-b from-gray-700 to-gray-900 flex flex-col items-center justify-center py-12 px-8">
          <!-- Avatar -->
          <div class="w-28 h-28 rounded-full border-4 border-white/30 shadow-lg overflow-hidden bg-gray-200 mb-5">
            <img
              src="/src/assets/avatar-default.jpg"
              alt="Foto Profil"
              class="w-full h-full object-cover"
            />
          </div>
          <!-- Nama & Divisi -->
          <h2 class="text-xl font-bold text-white text-center">{{ form.nama || '-' }}</h2>
          <p class="text-sm font-semibold text-gray-300 mt-1 text-center">{{ form.divisi || '-' }}</p>
        </div>

        <!-- Kanan: Detail Info & Tombol Keluar -->
        <div class="flex-1 px-8 py-8 flex flex-col justify-between">
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
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3h6v4H9V3zm-4 14h4v4H5v-4zm10 0h4v4h-4v-4zM12 7v4m0 0H7v6m5-6h5v6" />
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
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422A12.083 12.083 0 0120 17.764L12 22l-8-4.236a12.083 12.083 0 011.84-7.186L12 14z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-400 leading-none mb-0.5">Role</p>
                <p class="text-sm font-semibold text-gray-700 capitalize">{{ form.role || '-' }}</p>
              </div>
            </div>

            <!-- CABANG -->
            <div v-if="form.role === 'user' || form.cabang" class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
              <div class="w-8 h-8 rounded-lg bg-gray-200 flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-400 leading-none mb-0.5">Cabang</p>
                <p class="text-sm font-semibold text-gray-700">{{ form.cabang || '-' }}</p>
              </div>
            </div>

            <!-- USERNAME -->
            <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
              <div class="w-8 h-8 rounded-lg bg-gray-200 flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <g transform="translate(0,2)">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 10a4 4 0 11-8 0 4 4 0 018 0v4a2 2 0 104 0V10a8 8 0 10-8 8" />
                  </g>
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
  role: '',
  cabang: ''
})

onMounted(() => {
  const stored = localStorage.getItem('user')
  if (stored) {
    const user = JSON.parse(stored)
    form.nama = user.nama || ''
    form.divisi = user.divisi || ''
    form.username = user.username || ''
    form.role = user.role || ''
    form.cabang = user.cabang || ''
  }
})

function handleKeluar() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.replace('/masuk')
}
</script>