<template>
  <div class="profile-overlay" @click.self="$emit('close')">
    <div class="profile-card" role="dialog" aria-modal="true" aria-label="Профиль">
      <button type="button" class="close-btn" @click="$emit('close')">×</button>

      <p class="overline">Профиль</p>
      <h2>{{ localName || "Ваш аккаунт" }}</h2>
      <p class="subline">{{ user.email }}</p>

      <AvatarPicker v-model="localAvatar" />

      <label class="field">
        <span>Имя</span>
        <input v-model.trim="localName" type="text" maxlength="100" :disabled="isLoading" />
      </label>

      <div class="meta-grid">
        <div class="meta-item">
          <span class="meta-label">ID</span>
          <strong>{{ user.id }}</strong>
        </div>
        <div class="meta-item">
          <span class="meta-label">Создан</span>
          <strong>{{ createdAt }}</strong>
        </div>
      </div>

      <div class="actions">
        <button type="button" class="ghost-btn" @click="$emit('logout')">Выйти</button>
        <button type="button" class="save-btn" :disabled="isLoading || !isDirty" @click="handleSave">
          {{ isLoading ? "Сохраняем..." : "Сохранить профиль" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";

import AvatarPicker from "./AvatarPicker.vue";

const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close", "save", "logout"]);

const localName = ref(props.user.name || "");
const localAvatar = ref(props.user.avatar_data || "");

watch(
  () => props.user,
  (nextUser) => {
    localName.value = nextUser.name || "";
    localAvatar.value = nextUser.avatar_data || "";
  },
  { deep: true },
);

const isDirty = computed(() => {
  return localName.value !== (props.user.name || "") || localAvatar.value !== (props.user.avatar_data || "");
});

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
    avatarData: localAvatar.value,
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
  display: grid;
  place-items: center;
  padding: 20px;
}

.profile-card {
  width: min(520px, 100%);
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

.overline {
  margin: 0;
  color: #64748b;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

h2 {
  margin: 8px 0 0;
  color: #151c29;
  font-size: 30px;
  line-height: 1.08;
  font-weight: 800;
}

.subline {
  margin: 8px 0 18px;
  color: #64748b;
  font-size: 14px;
  line-height: 1.4;
}

.field {
  margin-top: 14px;
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
  outline: none;
}

.meta-grid {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.meta-item {
  border-radius: 16px;
  background: #f5f7fb;
  padding: 14px;
}

.meta-label {
  display: block;
  color: #94a3b8;
  font-size: 12px;
  line-height: 1;
}

.meta-item strong {
  display: block;
  margin-top: 6px;
  color: #111827;
  font-size: 15px;
}

.actions {
  margin-top: 18px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.ghost-btn,
.save-btn {
  height: 48px;
  border-radius: 16px;
  padding: 0 18px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
}

.ghost-btn {
  border: 1px solid #d8deea;
  background: #ffffff;
  color: #526878;
}

.save-btn {
  border: 0;
  background: #2b31b3;
  color: #ffffff;
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: default;
}
</style>
