import { ref } from "vue";

const toasts = ref([]);
let toastIdCounter = 0;

const TOAST_DURATION = 4000;

function addToast(message, type = "success") {
  const id = ++toastIdCounter;
  const toast = {
    id,
    message,
    type,
    createdAt: Date.now(),
    duration: TOAST_DURATION,
  };
  toasts.value.push(toast);

  setTimeout(() => removeToast(id), TOAST_DURATION);
}

function removeToast(id) {
  const idx = toasts.value.findIndex((t) => t.id === id);
  if (idx !== -1) toasts.value.splice(idx, 1);
}

export function useToast() {
  return {
    toasts,
    addToast,
    removeToast,
  };
}
