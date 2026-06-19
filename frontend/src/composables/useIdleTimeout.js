import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";

const IDLE_LIMIT_MS = 15 * 60 * 1000;
const WARN_BEFORE_MS = 1 * 60 * 1000;
const WARN_AT_MS = IDLE_LIMIT_MS - WARN_BEFORE_MS;
const ACTIVITY_EVENTS = [
  "mousedown",
  "keydown",
  "touchstart",
  "scroll",
  "wheel",
  "visibilitychange",
];

export function useIdleTimeout() {
  const router = useRouter();

  const showWarningModal = ref(false);
  const countdown = ref(60);

  const warnTimer = ref(null);
  const logoutTimer = ref(null);
  const countdownTimer = ref(null);

  function doLogout() {
    clearAllTimers();
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    router.push({ name: "Masuk", replace: true });
  }

  function clearAllTimers() {
    if (warnTimer.value) clearTimeout(warnTimer.value);
    if (logoutTimer.value) clearTimeout(logoutTimer.value);
    if (countdownTimer.value) clearInterval(countdownTimer.value);
    warnTimer.value = null;
    logoutTimer.value = null;
    countdownTimer.value = null;
  }

  function resetTimer() {
    if (showWarningModal.value) return;

    clearAllTimers();

    warnTimer.value = setTimeout(() => {
      showWarning();
    }, WARN_AT_MS);
  }

  function showWarning() {
    showWarningModal.value = true;
    countdown.value = Math.floor(WARN_BEFORE_MS / 1000);
    countdownTimer.value = setInterval(() => {
      countdown.value--;
      if (countdown.value <= 0) {
        clearInterval(countdownTimer.value);
        countdownTimer.value = null;
      }
    }, 1000);

    logoutTimer.value = setTimeout(() => {
      doLogout();
    }, WARN_BEFORE_MS);
  }

  function stayLoggedIn() {
    showWarningModal.value = false;
    countdown.value = Math.floor(WARN_BEFORE_MS / 1000);
    resetTimer();
  }

  function logoutNow() {
    showWarningModal.value = false;
    doLogout();
  }

  function handleActivity() {
    resetTimer();
  }

  onMounted(() => {
    ACTIVITY_EVENTS.forEach((event) => {
      window.addEventListener(event, handleActivity, { passive: true });
    });
    resetTimer();
  });

  onUnmounted(() => {
    ACTIVITY_EVENTS.forEach((event) => {
      window.removeEventListener(event, handleActivity);
    });
    clearAllTimers();
  });

  return {
    showWarningModal,
    countdown,
    stayLoggedIn,
    logoutNow,
  };
}
