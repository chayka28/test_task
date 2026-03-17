<template>
  <div class="auth-overlay" @click.self="$emit('close')">
    <div class="auth-card" role="dialog" aria-modal="true" aria-label="Авторизация">
      <button type="button" class="close-btn" aria-label="Закрыть" @click="$emit('close')">×</button>

      <BrandLogo icon-only />

      <p class="overline">Trendsee</p>
      <h2>{{ mode === 'register' ? "Создайте аккаунт" : "Войдите в аккаунт" }}</h2>
      <p class="text">
        {{ mode === "register" ? "После регистрации можно сохранять избранное, менять профиль и работать со своей подборкой." : "Войдите, чтобы продолжить работу с избранным, подборками и профилем." }}
      </p>

      <div class="mode-switch">
        <button type="button" class="mode-btn" :class="{ 'mode-btn--active': mode === 'register' }" @click="mode = 'register'">
          Регистрация
        </button>
        <button type="button" class="mode-btn" :class="{ 'mode-btn--active': mode === 'login' }" @click="mode = 'login'">
          Вход
        </button>
      </div>

      <form v-if="mode === 'register'" class="form" @submit.prevent="submitRegister">
        <AvatarPicker v-model="registerForm.avatarData" />

        <label class="field">
          <span>Имя</span>
          <input
            v-model.trim="registerForm.name"
            type="text"
            minlength="2"
            maxlength="100"
            placeholder="Например, Александра"
            :disabled="isLoading"
          />
        </label>

        <label class="field">
          <span>Email</span>
          <input
            v-model.trim="registerForm.email"
            type="email"
            placeholder="you@trendsee.app"
            :disabled="isLoading"
          />
        </label>

        <div class="password-grid">
          <label class="field">
            <span>Пароль</span>
            <input
              v-model="registerForm.password"
              type="password"
              minlength="8"
              placeholder="Минимум 8 символов"
              :disabled="isLoading"
            />
          </label>

          <label class="field">
            <span>Повторите пароль</span>
            <input
              v-model="registerForm.confirmPassword"
              type="password"
              minlength="8"
              placeholder="Повторите пароль"
              :disabled="isLoading"
            />
          </label>
        </div>

        <label class="checkbox-row">
          <input v-model="registerForm.accepted" type="checkbox" :disabled="isLoading" />
          <span>Я согласен(а) с правилами платформы и обработкой персональных данных.</span>
        </label>

        <p v-if="registerValidationText" class="error-text">{{ registerValidationText }}</p>
        <p v-else-if="errorText" class="error-text">{{ errorText }}</p>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          {{ isLoading ? "Создаем аккаунт..." : "Создать аккаунт" }}
        </button>
      </form>

      <form v-else class="form" @submit.prevent="submitLogin">
        <label class="field">
          <span>Email</span>
          <input
            v-model.trim="loginForm.email"
            type="email"
            placeholder="you@trendsee.app"
            :disabled="isLoading"
          />
        </label>

        <label class="field">
          <span>Пароль</span>
          <input
            v-model="loginForm.password"
            type="password"
            minlength="8"
            placeholder="Ваш пароль"
            :disabled="isLoading"
          />
        </label>

        <p v-if="loginValidationText" class="error-text">{{ loginValidationText }}</p>
        <p v-else-if="errorText" class="error-text">{{ errorText }}</p>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          {{ isLoading ? "Входим..." : "Войти" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch } from "vue";

import AvatarPicker from "./AvatarPicker.vue";
import BrandLogo from "./BrandLogo.vue";

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
  errorText: {
    type: String,
    default: "",
  },
  initialMode: {
    type: String,
    default: "register",
  },
});

const emit = defineEmits(["register", "login", "close"]);

const mode = ref(props.initialMode);

const registerForm = reactive({
  name: "",
  email: "",
  password: "",
  confirmPassword: "",
  accepted: false,
  avatarData: "preset:midnight",
});

const loginForm = reactive({
  email: "",
  password: "",
});

watch(
  () => props.initialMode,
  (value) => {
    mode.value = value;
  },
);

const registerValidationText = computed(() => {
  if (registerForm.name && registerForm.name.length < 2) return "Имя должно содержать минимум 2 символа.";
  if (registerForm.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registerForm.email)) return "Укажите корректный email.";
  if (registerForm.password && registerForm.password.length < 8) return "Пароль должен содержать минимум 8 символов.";
  if (registerForm.confirmPassword && registerForm.password !== registerForm.confirmPassword) return "Пароли должны совпадать.";
  if ((registerForm.name || registerForm.email || registerForm.password) && !registerForm.accepted) return "Подтвердите согласие, чтобы продолжить.";
  return "";
});

const loginValidationText = computed(() => {
  if (loginForm.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(loginForm.email)) return "Укажите корректный email.";
  if (loginForm.password && loginForm.password.length < 8) return "Пароль должен содержать минимум 8 символов.";
  return "";
});

watch(
  () => props.isLoading,
  (nextValue, previousValue) => {
    if (previousValue && !nextValue && !props.errorText) {
      registerForm.name = "";
      registerForm.email = "";
      registerForm.password = "";
      registerForm.confirmPassword = "";
      registerForm.accepted = false;
      registerForm.avatarData = "preset:midnight";
      loginForm.email = "";
      loginForm.password = "";
    }
  },
);

function submitRegister() {
  if (
    props.isLoading ||
    registerValidationText.value ||
    registerForm.name.length < 2 ||
    !registerForm.email ||
    registerForm.password.length < 8 ||
    registerForm.password !== registerForm.confirmPassword ||
    !registerForm.accepted
  ) {
    return;
  }

  emit("register", {
    name: registerForm.name,
    email: registerForm.email,
    password: registerForm.password,
    avatarData: registerForm.avatarData,
  });
}

function submitLogin() {
  if (props.isLoading || loginValidationText.value || !loginForm.email || loginForm.password.length < 8) {
    return;
  }

  emit("login", {
    email: loginForm.email,
    password: loginForm.password,
  });
}
</script>

<style scoped>
.auth-overlay {
  position: fixed;
  inset: 0;
  z-index: 120;
  background: rgba(17, 22, 35, 0.5);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  overflow-y: auto;
}

.auth-card {
  width: min(560px, 100%);
  position: relative;
  max-height: calc(100vh - 40px);
  overflow-y: auto;
  border-radius: 28px;
  background: #ffffff;
  padding: 28px;
  box-shadow: 0 28px 80px rgba(20, 27, 45, 0.22);
  overscroll-behavior: contain;
  scrollbar-width: thin;
}

.close-btn {
  position: absolute;
  top: 18px;
  right: 18px;
  width: 32px;
  height: 32px;
  border: 0;
  border-radius: 50%;
  background: #eef1f5;
  color: #77818b;
  font-size: 22px;
  line-height: 1;
  cursor: pointer;
}

.overline {
  margin: 18px 0 8px;
  color: #64748b;
  font-size: 13px;
  line-height: 1.2;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

h2 {
  margin: 0;
  color: #151c29;
  font-size: 30px;
  line-height: 1.08;
  font-weight: 800;
}

.text {
  margin: 12px 0 0;
  color: #64748b;
  font-size: 15px;
  line-height: 1.5;
}

.mode-switch {
  margin-top: 18px;
  display: inline-flex;
  padding: 4px;
  border-radius: 16px;
  background: #f2f4f8;
}

.mode-btn {
  border: 0;
  background: transparent;
  color: #6b7280;
  height: 38px;
  padding: 0 18px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.mode-btn--active {
  background: #ffffff;
  color: #2b31b3;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
}

.form {
  margin-top: 18px;
  display: grid;
  gap: 12px;
}

.password-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.field {
  display: grid;
  gap: 8px;
}

.field span {
  color: #475569;
  font-size: 13px;
  line-height: 1.2;
  font-weight: 700;
}

.field input {
  width: 100%;
  height: 52px;
  border: 1px solid #d9e1ea;
  border-radius: 16px;
  padding: 0 16px;
  color: #172033;
  font-size: 15px;
  outline: none;
}

.field input:focus {
  border-color: #2b31b3;
}

.checkbox-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  color: #617283;
  font-size: 13px;
  line-height: 1.45;
}

.checkbox-row input {
  margin-top: 2px;
}

.error-text {
  margin: 0;
  color: #cb4051;
  font-size: 13px;
  line-height: 1.35;
}

.submit-btn {
  height: 56px;
  border: 0;
  border-radius: 18px;
  background: #2b31b3;
  color: #ffffff;
  font-size: 16px;
  line-height: 1;
  font-weight: 700;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: default;
}

@media (max-width: 620px) {
  .auth-overlay {
    padding: 10px;
    align-items: flex-start;
  }

  .auth-card {
    max-height: calc(100vh - 20px);
    padding: 24px 18px 18px;
    border-radius: 24px;
  }

  .password-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-height: 820px) {
  .auth-overlay {
    align-items: flex-start;
  }

  .auth-card {
    margin-block: auto;
  }
}
</style>
