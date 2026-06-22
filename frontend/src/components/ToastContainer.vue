<template>
  <div class="fixed top-4 right-4 z-[100] flex flex-col gap-2 pointer-events-none" style="min-width: 300px; max-width: 360px;">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="pointer-events-auto relative overflow-hidden rounded-xl shadow-lg border"
        :class="toast.type === 'success' ? 'bg-green-50/90 border-green-200' : toast.type === 'warning' ? 'bg-orange-50/90 border-orange-200' : 'bg-red-50/90 border-red-200'"
        style="backdrop-filter: blur(8px);"
      >
        <div class="flex items-start gap-3 px-4 py-3">
          <!-- Icon -->
          <div
            class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center mt-0.5"
            :class="toast.type === 'success' ? 'bg-green-500' : toast.type === 'warning' ? 'bg-orange-400' : 'bg-red-500'"
          >
            <svg v-if="toast.type === 'success'" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
            <svg v-else-if="toast.type === 'warning'" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <!-- Message -->
          <p class="text-sm leading-snug flex-1" :class="toast.type === 'success' ? 'text-green-800' : toast.type === 'warning' ? 'text-orange-800' : 'text-red-800'">
            {{ toast.message }}
          </p>
          <!-- Close button -->
          <button
            @click="$emit('remove', toast.id)"
            class="flex-shrink-0 text-gray-400 hover:text-gray-600 transition mt-0.5"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <!-- Timer bar -->
        <div class="h-1 w-full" :class="toast.type === 'success' ? 'bg-green-100' : toast.type === 'warning' ? 'bg-orange-100' : 'bg-red-100'">
          <div
            :ref="el => setupTimerBar(el, toast)"
            class="h-1"
            :class="toast.type === 'success' ? 'bg-green-400' : toast.type === 'warning' ? 'bg-orange-400' : 'bg-red-400'"
          ></div>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
defineProps({
  toasts: {
    type: Array,
    required: true
  }
})
defineEmits(['remove'])

function setupTimerBar(el, toast) {
  if (!el) return

  const elapsed   = Date.now() - toast.createdAt
  const remaining = Math.max(toast.duration - elapsed, 0)
  const startWidth = toast.duration > 0
    ? Math.max((remaining / toast.duration) * 100, 0)
    : 0

  el.style.transition = 'none'
  el.style.width = startWidth + '%'

  void el.offsetWidth

  requestAnimationFrame(() => {
    if (remaining > 0) {
      el.style.transition = `width linear ${remaining / 1000}s`
      el.style.width = '0%'
    } else {
      el.style.width = '0%'
    }
  })
}
</script>

<style scoped>
.toast-enter-active {
  animation: toast-slide-in 0.3s ease-out forwards;
}
.toast-leave-active {
  animation: toast-slide-out 0.3s ease-in forwards;
}

@keyframes toast-slide-in {
  from { opacity: 0; transform: translateX(100%); }
  to   { opacity: 1; transform: translateX(0); }
}

@keyframes toast-slide-out {
  from { opacity: 1; transform: translateX(0); }
  to   { opacity: 0; transform: translateX(100%); }
}
</style>