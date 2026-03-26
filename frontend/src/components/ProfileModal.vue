<template>
  <div class="profile-overlay" @click.self="$emit('close')">
    <div class="profile-card" role="dialog" aria-modal="true" aria-label="Профиль пользователя">
      <button type="button" class="close-btn" @click="$emit('close')">×</button>

      <div class="profile-hero">
        <AppAvatar :avatar="user.avatar_data" :seed="user.id" :size="72" alt="Пользователь" />

        <div class="profile-copy">
          <p class="overline">Профиль</p>
          <h2>{{ localName || user.name }}</h2>
          <p class="subline">{{ phone || "Номер не указан" }}</p>
          <div class="hero-badges">
            <span class="hero-badge">Личный кабинет</span>
            <span class="hero-badge">{{ postsCount }} публикаций</span>
          </div>
        </div>
      </div>

      <p class="profile-note">
        Здесь можно обновить имя, перейти к своим публикациям и управлять аккаунтом.
      </p>

      <div class="meta-grid">
        <div class="meta-item">
          <span class="meta-label">ID пользователя</span>
          <strong>{{ user.id }}</strong>
        </div>
        <div class="meta-item">
          <span class="meta-label">Публикаций</span>
          <strong>{{ postsCount }}</strong>
        </div>
        <div class="meta-item">
          <span class="meta-label">Создан</span>
          <strong>{{ createdAt }}</strong>
        </div>
        <div class="meta-item">
          <span class="meta-label">Статус</span>
          <strong>Активный аккаунт</strong>
        </div>
      </div>

      <label class="field">
        <span>Имя пользователя</span>
        <input v-model.trim="localName" type="text" maxlength="100" :disabled="isLoading" />
      </label>

      <div class="primary-actions">
        <button type="button" class="save-btn" :disabled="isLoading || !isDirty" @click="handleSave">
          {{ isLoading ? "Сохраняем..." : "Сохранить имя" }}
        </button>
        <button type="button" class="secondary-btn" :disabled="isLoading || isDeleting" @click="$emit('view-posts')">
          Мои публикации
        </button>
        <button type="button" class="secondary-btn" :disabled="isLoading || isDeleting" @click="$emit('create-post')">
          Создать публикацию
        </button>
      </div>

      <div class="secondary-actions">
        <button type="button" class="ghost-btn" @click="$emit('logout')">Выйти</button>
        <button type="button" class="danger-btn" :disabled="isDeleting" @click="$emit('delete-account')">
          {{ isDeleting ? "Удаляем аккаунт..." : "Удалить пользователя" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";

import AppAvatar from "./AppAvatar.vue";

const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
  phone: {
    type: String,
    default: "",
  },
  postsCount: {
    type: Number,
    default: 0,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  isDeleting: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close", "save", "logout", "create-post", "delete-account", "view-posts"]);

const localName = ref(props.user.name || "");

watch(
  () => props.user,
  (nextUser) => {
    localName.value = nextUser.name || "";
  },
  { deep: true },
);

const isDirty = computed(() => localName.value !== (props.user.name || ""));

const createdAt = computed(() => {
  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  }).format(new Date(props.user.created_at));
});

function handleSave() {
  emit("save", {
    name: localName.value,
  });
}
</script>

<style scoped>
.profile-overlay {
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

.profile-card {
  width: min(640px, 100%);
  position: relative;
  max-height: calc(100vh - 40px);
  overflow-y: auto;
  border-radius: 28px;
  background: #ffffff;
  padding: 28px;
  box-shadow: 0 28px 80px rgba(20, 27, 45, 0.22);
  overscroll-behavior: contain;
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

.profile-hero {
  display: flex;
  align-items: center;
  gap: 16px;
}

.profile-copy {
  min-width: 0;
}

.overline {
  margin: 0;
  color: #64748b;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

h2 {
  margin: 6px 0 0;
  color: #151c29;
  font-size: 30px;
  line-height: 1.08;
  font-weight: 800;
}

.subline {
  margin: 8px 0 0;
  color: #64748b;
  font-size: 14px;
  line-height: 1.4;
}

.hero-badges {
  margin-top: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.hero-badge {
  border-radius: 999px;
  background: #eef2ff;
  color: #4352cc;
  padding: 6px 10px;
  font-size: 12px;
  line-height: 1;
  font-weight: 700;
}

.profile-note {
  margin: 16px 0 0;
  color: #5d6d7b;
  font-size: 14px;
  line-height: 1.5;
}

.meta-grid {
  margin-top: 18px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.meta-item {
  border-radius: 18px;
  background: #f5f7fb;
  padding: 14px;
  display: grid;
  gap: 6px;
}

.meta-label {
  color: #94a3b8;
  font-size: 12px;
  line-height: 1.2;
}

.meta-item strong {
  color: #111827;
  font-size: 15px;
  line-height: 1.3;
}

.field {
  margin-top: 18px;
  display: grid;
  gap: 8px;
}

.field span {
  color: #475569;
  font-size: 13px;
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
  line-height: 1.2;
}

.field input:focus {
  outline: none;
  border-color: #2b31b3;
}

.primary-actions {
  margin-top: 22px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.secondary-actions {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.save-btn,
.secondary-btn,
.ghost-btn,
.danger-btn {
  height: 48px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.save-btn {
  border: 0;
  background: #2b31b3;
  color: #ffffff;
}

.secondary-btn {
  border: 1px solid #d8deea;
  background: #ffffff;
  color: #2b31b3;
}

.ghost-btn {
  border: 1px solid #d8deea;
  background: #ffffff;
  color: #526878;
}

.danger-btn {
  border: 1px solid #f1c7ce;
  background: #fff3f5;
  color: #c14558;
}

button:disabled {
  opacity: 0.6;
  cursor: default;
}

@media (max-width: 720px) {
  .profile-card {
    padding: 24px 18px;
  }

  .profile-hero {
    align-items: flex-start;
  }

  .meta-grid,
  .primary-actions,
  .secondary-actions {
    grid-template-columns: 1fr;
  }
}
</style>
