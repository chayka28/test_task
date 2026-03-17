<template>
  <div class="auth-overlay" @click.self="$emit('close')">
    <div class="auth-card" role="dialog" aria-modal="true" aria-label="Регистрация">
      <button type="button" class="close-btn" aria-label="Закрыть" @click="$emit('close')">×</button>

      <div class="logo-mark" aria-hidden="true">
        <img src="/assets/logo/logo-outline.png" alt="" class="logo-outline" />
        <img src="/assets/logo/logo-center.png" alt="" class="logo-center" />
      </div>

      <p class="overline">Trendsee</p>
      <h2>Создайте аккаунт и сохраните свою ленту</h2>
      <p class="text">
        Регистрация открывает персональный профиль, сохранение избранного и быстрый доступ к вашей подборке публикаций.
      </p>

      <form class="form" @submit.prevent="submitForm">
        <label class="field">
          <span>Имя</span>
          <input
            v-model.trim="form.name"
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
            v-model.trim="form.email"
            type="email"
            placeholder="you@trendsee.app"
            :disabled="isLoading"
          />
        </label>

        <div class="password-grid">
          <label class="field">
            <span>Пароль</span>
            <input
              v-model="form.password"
              type="password"
              minlength="8"
              placeholder="Минимум 8 символов"
              :disabled="isLoading"
            />
          </label>

          <label class="field">
            <span>Повторите пароль</span>
            <input
              v-model="form.confirmPassword"
              type="password"
              minlength="8"
              placeholder="Повторите пароль"
              :disabled="isLoading"
            />
          </label>
        </div>

        <label class="checkbox-row">
          <input v-model="form.accepted" type="checkbox" :disabled="isLoading" />
          <span>Я согласен(а) с правилами платформы и обработкой персональных данных.</span>
        </label>

        <p v-if="validationText" class="error-text">{{ validationText }}</p>
        <p v-else-if="errorText" class="error-text">{{ errorText }}</p>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          {{ isLoading ? "Создаем аккаунт..." : "Создать аккаунт" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, watch } from "vue";

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
  errorText: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["submit", "close"]);

const form = reactive({
  name: "",
  email: "",
  password: "",
  confirmPassword: "",
  accepted: false,
});

const validationText = computed(() => {
  if (form.name && form.name.length < 2) {
    return "Имя должно содержать минимум 2 символа.";
  }

  if (form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    return "Укажите корректный email.";
  }

  if (form.password && form.password.length < 8) {
    return "Пароль должен содержать минимум 8 символов.";
  }

  if (form.confirmPassword && form.password !== form.confirmPassword) {
    return "Пароли должны совпадать.";
  }

  if ((form.name || form.email || form.password || form.confirmPassword) && !form.accepted) {
    return "Подтвердите согласие, чтобы продолжить.";
  }

  return "";
});

watch(
  () => props.isLoading,
  (nextValue, previousValue) => {
    if (previousValue && !nextValue && !props.errorText) {
      form.name = "";
      form.email = "";
      form.password = "";
      form.confirmPassword = "";
      form.accepted = false;
    }
  },
);

function submitForm() {
  if (
    props.isLoading ||
    validationText.value ||
    form.name.length < 2 ||
    !form.email ||
    form.password.length < 8 ||
    form.password !== form.confirmPassword ||
    !form.accepted
  ) {
    return;
  }

  emit("submit", {
    name: form.name,
    email: form.email,
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
  display: grid;
  place-items: center;
  padding: 20px;
}

.auth-card {
  width: min(540px, 100%);
  position: relative;
  border-radius: 28px;
  background: #ffffff;
  padding: 28px;
  box-shadow: 0 28px 80px rgba(20, 27, 45, 0.22);
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

.logo-mark {
  position: relative;
  width: 34px;
  height: 34px;
}

.logo-outline {
  position: absolute;
  inset: 3px 0 0 0;
  width: 34px;
  height: 24px;
  object-fit: contain;
}

.logo-center {
  position: absolute;
  left: 11px;
  top: 1px;
  width: 14px;
  height: 17px;
  object-fit: contain;
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

.form {
  margin-top: 20px;
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

.submit-btn:not(:disabled):hover {
  transform: translateY(-1px);
}

@media (max-width: 620px) {
  .auth-card {
    padding: 24px 18px 18px;
  }

  .password-grid {
    grid-template-columns: 1fr;
  }
}
</style>
