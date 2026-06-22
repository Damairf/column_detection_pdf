<template>
  <div class="relative min-h-screen w-full overflow-hidden flex items-center justify-center">

    <!-- Background image (dinamis dari API) -->
    <div class="absolute inset-0 z-0">
      <!-- Placeholder saat loading -->
      <div
        v-if="isBgLoading"
        class="w-full h-full bg-gray-800"
      ></div>
      <!-- Gambar background -->
      <img
        v-else
        :src="bgUrl"
        :key="bgUrl"
        alt="Nasmoco Background"
        class="w-full h-full object-cover"
        @error="handleBgError"
      />
    </div>

    <!-- Card container -->
    <div class="relative z-10 w-full max-w-md mx-6">
      <div
        class="rounded-2xl shadow-2xl px-8 py-8"
        style="background: rgba(100, 110, 120, 0.70); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.15);"
      >

        <!-- Logo -->
        <div class="flex justify-center mb-6">
          <img
            src="/src/assets/logo-nasmoco.png"
            alt="Nasmoco Column Detection"
            class="h-16 object-contain"
          />
        </div>

        <!-- Form -->
        <form @submit.prevent="handleMasuk" novalidate>

          <!-- Username -->
          <div class="mb-3">
            <label class="block text-white font-semibold mb-0.5 text-sm">Username</label>
            <input
              v-model="form.username"
              type="text"
              placeholder="Masukkan username anda....."
              class="w-full px-3 py-2 rounded-lg text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-sky-400 transition text-sm border-0"
              style="background: rgba(255,255,255,0.88);"
              :class="{ 'ring-2 ring-red-400': errors.username }"
            />
            <p v-if="errors.username" class="text-red-700 text-xs mt-1">{{ errors.username }}</p>
          </div>

          <!-- Password -->
          <div class="mb-6">
            <label class="block text-white font-semibold mb-0.5 text-sm">Password</label>
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Masukkan password anda....."
                class="w-full px-3 py-2 rounded-lg text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-sky-400 transition text-sm pr-11 border-0"
                style="background: rgba(255,255,255,0.88);"
                :class="{ 'ring-2 ring-red-400': errors.password }"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="cursor-pointer absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 transition"
              >
                <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 4.411m0 0L21 21" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
            <p v-if="errors.password" class="text-red-700 text-xs mt-1">{{ errors.password }}</p>
          </div>

          <!-- reCAPTCHA v2 -->
          <div class="mb-4 flex flex-col items-center">
            <div
              ref="recaptchaContainer"
              class="recaptcha-wrapper"
            ></div>
            <p v-if="errors.recaptcha" class="text-red-300 text-xs mt-2 text-center">
              {{ errors.recaptcha }}
            </p>
          </div>

          <!-- Error dari server -->
          <div v-if="serverError" class="mb-4 p-3 bg-red-500/30 border border-red-400/50 rounded-lg text-red-200 text-sm text-center">
            {{ serverError }}
          </div>

          <!-- Tombol Masuk -->
          <button
            type="submit"
            :disabled="loading"
            class="cursor-pointer w-full py-2 rounded-lg font-bold text-white text-sm tracking-widest uppercase transition-all duration-200 shadow-md"
            style="background: #29b6f6;"
            :class="loading ? 'opacity-70 cursor-not-allowed' : 'hover:brightness-110 active:scale-95'"
          >
            <span v-if="loading" class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              Memproses...
            </span>
            <span v-else>Masuk</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.recaptcha-wrapper {
  transform: scale(0.85);
  transform-origin: center top;
}

.recaptcha-wrapper :deep(iframe) {
  border-radius: 5px;
  display: block;
}
</style>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router             = useRouter()
const showPassword       = ref(false)
const loading            = ref(false)
const serverError        = ref('')
const isBgLoading        = ref(true)
const bgUrl              = ref('')
const recaptchaToken     = ref('')
const recaptchaSiteKey   = import.meta.env.VITE_RECAPTCHA_SITE_KEY
const recaptchaContainer = ref(null)
let   recaptchaWidgetId  = null

const form = reactive({ username: '', password: '' })
const errors = reactive({ username: '', password: '', recaptcha: '' })

onMounted(async () => {
  await fetchBackground()
  await nextTick()
  initRecaptcha()
})

function initRecaptcha() {
  if (typeof window.grecaptcha === 'undefined' || typeof window.grecaptcha.render === 'undefined') {
    setTimeout(initRecaptcha, 300)
    return
  }

  if (recaptchaWidgetId !== null) {
    try { window.grecaptcha.reset(recaptchaWidgetId) } catch (_) {}
    return
  }

  if (!recaptchaContainer.value) return

  recaptchaWidgetId = window.grecaptcha.render(recaptchaContainer.value, {
    sitekey:           recaptchaSiteKey,
    callback:          (token) => {
      recaptchaToken.value = token
      errors.recaptcha = ''
    },
    'expired-callback': () => {
      recaptchaToken.value = ''
    },
    'error-callback':   () => {
      recaptchaToken.value = ''
      errors.recaptcha = 'reCAPTCHA error, coba refresh halaman.'
    }
  })
}

// ─── Background ───────────────────────────────────────────────────────────────
async function fetchBackground() {
  isBgLoading.value = true
  try {
    const base     = import.meta.env.VITE_API_BASE_URL || ''
    const res      = await axios.get(`${base}/api/kustomisasi/bg-active`)
    const filename = res.data.background || 'bg-nasmoco.avif'
    bgUrl.value    = `${base}/api/kustomisasi/background-file/${filename}?t=${Date.now()}`
  } catch {
    const base  = import.meta.env.VITE_API_BASE_URL || ''
    bgUrl.value = `${base}/api/kustomisasi/background-file/bg-nasmoco.avif?t=${Date.now()}`
  } finally {
    isBgLoading.value = false
  }
}

function handleBgError(e) {
  const base        = import.meta.env.VITE_API_BASE_URL || ''
  const fallbackUrl = `${base}/api/kustomisasi/background-file/bg-nasmoco.avif?t=${Date.now()}`
  if (e.target.src !== fallbackUrl) e.target.src = fallbackUrl
}

// ─── Validasi ─────────────────────────────────────────────────────────────────
function validate() {
  let valid        = true
  errors.username  = ''
  errors.password  = ''
  errors.recaptcha = ''

  if (!form.username.trim()) { errors.username  = 'Username wajib diisi.';             valid = false }
  if (!form.password)        { errors.password  = 'Password wajib diisi.';             valid = false }
  if (!recaptchaToken.value) { errors.recaptcha = 'Harap selesaikan verifikasi reCAPTCHA.'; valid = false }
  return valid
}

// ─── Submit ───────────────────────────────────────────────────────────────────
async function handleMasuk() {
  serverError.value = ''
  if (!validate()) return

  loading.value = true
  try {
    const response = await axios.post('/api/auth/masuk', {
      username:        form.username,
      password:        form.password,
      recaptcha_token: recaptchaToken.value
    })

    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('user', JSON.stringify(response.data.user))
    router.push('/beranda')
  } catch (err) {
    serverError.value = err.response?.data?.detail || 'Terjadi kesalahan. Coba lagi.'

    if (recaptchaWidgetId !== null && window.grecaptcha) {
      window.grecaptcha.reset(recaptchaWidgetId)
    }
    recaptchaToken.value = ''
  } finally {
    loading.value = false
  }
}
</script>