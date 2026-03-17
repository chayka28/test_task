<template>
  <div class="avatar-picker">
    <div class="avatar-preview">
      <AppAvatar :avatar="modelValue" :size="72" alt="Выбранная аватарка" />
      <div class="avatar-copy">
        <p class="avatar-title">Аватар профиля</p>
        <p class="avatar-text">Можно выбрать пресет или загрузить свой файл.</p>
      </div>
    </div>

    <div class="preset-grid">
      <button
        v-for="preset in avatarPresets"
        :key="preset.id"
        type="button"
        class="preset-btn"
        :class="{ 'preset-btn--active': modelValue === preset.id }"
        @click="$emit('update:modelValue', preset.id)"
      >
        <span class="preset-swatch" :style="{ background: preset.background }"></span>
      </button>
    </div>

    <label class="upload-btn">
      <input type="file" accept="image/*" hidden @change="handleFileChange" />
      <span>Загрузить свою аватарку</span>
    </label>

    <p v-if="errorText" class="error-text">{{ errorText }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";

import AppAvatar from "./AppAvatar.vue";
import { avatarPresets } from "../services/avatarPresets";

defineProps({
  modelValue: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["update:modelValue"]);
const errorText = ref("");

function handleFileChange(event) {
  const [file] = event.target.files || [];
  errorText.value = "";

  if (!file) return;

  if (!file.type.startsWith("image/")) {
    errorText.value = "Можно загрузить только изображение.";
    return;
  }

  const reader = new FileReader();
  reader.onload = () => {
    emit("update:modelValue", String(reader.result || ""));
  };
  reader.onerror = () => {
    errorText.value = "Не удалось прочитать файл.";
  };
  reader.readAsDataURL(file);
}
</script>

<style scoped>
.avatar-picker {
  display: grid;
  gap: 12px;
}

.avatar-preview {
  display: flex;
  align-items: center;
  gap: 12px;
  border-radius: 18px;
  background: #f6f7fa;
  padding: 12px;
}

.avatar-title {
  margin: 0;
  color: #111827;
  font-size: 14px;
  line-height: 1.2;
  font-weight: 700;
}

.avatar-text {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 13px;
  line-height: 1.35;
}

.preset-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.preset-btn {
  border: 1px solid #d7deea;
  border-radius: 16px;
  background: #ffffff;
  padding: 10px;
  cursor: pointer;
}

.preset-btn--active {
  border-color: #2b31b3;
  box-shadow: 0 0 0 2px rgba(43, 49, 179, 0.14);
}

.preset-swatch {
  width: 100%;
  aspect-ratio: 1;
  border-radius: 14px;
  display: block;
}

.upload-btn {
  display: inline-flex;
  width: fit-content;
  align-items: center;
  justify-content: center;
  height: 42px;
  padding: 0 16px;
  border-radius: 14px;
  background: #f0f2f6;
  color: #2b31b3;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.error-text {
  margin: 0;
  color: #cb4051;
  font-size: 13px;
  line-height: 1.35;
}
</style>
