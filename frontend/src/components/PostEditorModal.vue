<template>
  <div class="editor-overlay" @click.self="$emit('close')">
    <div class="editor-card" role="dialog" aria-modal="true" :aria-label="mode === 'create' ? 'Новая публикация' : 'Редактирование публикации'">
      <button type="button" class="close-btn" @click="$emit('close')">×</button>

      <p class="overline">{{ mode === "create" ? "Новая публикация" : "Редактирование" }}</p>
      <h2>{{ mode === "create" ? "Создайте публикацию" : "Обновите публикацию" }}</h2>
      <p class="subline">
        {{ mode === "create" ? "Публикация сразу появится в вашей ленте после сохранения." : "Изменения применятся к карточке и детальной модалке." }}
      </p>

      <form class="form" @submit.prevent="handleSubmit">
        <label class="field">
          <span>Заголовок</span>
          <input
            v-model.trim="localTitle"
            type="text"
            maxlength="200"
            placeholder="Например, Разбор трендового ролика"
            :disabled="isLoading"
          />
        </label>

        <label class="field">
          <span>Текст публикации</span>
          <textarea
            v-model.trim="localText"
            rows="7"
            maxlength="5000"
            placeholder="Опишите публикацию так, как она должна открываться в карточке и модалке."
            :disabled="isLoading"
          ></textarea>
        </label>

        <div class="field-grid">
          <label class="field">
            <span>Ссылка на видео</span>
            <input
              v-model.trim="localVideoUrl"
              type="url"
              placeholder="https://example.com/video.mp4"
              :disabled="isLoading"
            />
          </label>

          <label class="field">
            <span>Ссылка на превью</span>
            <input
              v-model.trim="localPosterUrl"
              type="url"
              placeholder="https://example.com/poster.jpg"
              :disabled="isLoading"
            />
          </label>
        </div>

        <label class="field">
          <span>Источник публикации</span>
          <input
            v-model.trim="localSourceUrl"
            type="url"
            placeholder="https://example.com/source"
            :disabled="isLoading"
          />
        </label>

        <p v-if="validationError" class="error-text">{{ validationError }}</p>

        <div class="actions">
          <button type="button" class="ghost-btn" :disabled="isLoading" @click="$emit('close')">Отмена</button>
          <button type="submit" class="save-btn" :disabled="isLoading || Boolean(validationError)">
            {{ isLoading ? "Сохраняем..." : mode === "create" ? "Создать публикацию" : "Сохранить изменения" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";

const props = defineProps({
  mode: {
    type: String,
    default: "create",
  },
  initialPost: {
    type: Object,
    default: null,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close", "submit"]);

const localTitle = ref(props.initialPost?.title || "");
const localText = ref(props.initialPost?.text || "");
const localVideoUrl = ref(props.initialPost?.video_url || "");
const localPosterUrl = ref(props.initialPost?.poster_url || "");
const localSourceUrl = ref(props.initialPost?.source_url || "");

watch(
  () => props.initialPost,
  (nextPost) => {
    localTitle.value = nextPost?.title || "";
    localText.value = nextPost?.text || "";
    localVideoUrl.value = nextPost?.video_url || "";
    localPosterUrl.value = nextPost?.poster_url || "";
    localSourceUrl.value = nextPost?.source_url || "";
  },
  { deep: true },
);

function isValidUrl(value) {
  if (!value) return true;

  try {
    const normalized = new URL(value);
    return normalized.protocol === "http:" || normalized.protocol === "https:";
  } catch {
    return false;
  }
}

const validationError = computed(() => {
  if (!localTitle.value) return "Укажите заголовок публикации.";
  if (localTitle.value.length > 200) return "Заголовок должен быть не длиннее 200 символов.";
  if (!localText.value) return "Добавьте текст публикации.";
  if (localText.value.length > 5000) return "Текст публикации должен быть не длиннее 5000 символов.";
  if (!isValidUrl(localVideoUrl.value)) return "Укажите корректную ссылку на видео.";
  if (!isValidUrl(localPosterUrl.value)) return "Укажите корректную ссылку на превью.";
  if (!isValidUrl(localSourceUrl.value)) return "Укажите корректную ссылку на источник.";
  return "";
});

function handleSubmit() {
  if (props.isLoading || validationError.value) return;

  emit("submit", {
    title: localTitle.value,
    text: localText.value,
    videoUrl: localVideoUrl.value || null,
    posterUrl: localPosterUrl.value || null,
    sourceUrl: localSourceUrl.value || null,
  });
}
</script>

<style scoped>
.editor-overlay {
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

.editor-card {
  width: min(620px, 100%);
  max-height: calc(100vh - 40px);
  overflow-y: auto;
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
  margin: 10px 0 0;
  color: #64748b;
  font-size: 14px;
  line-height: 1.45;
}

.form {
  margin-top: 18px;
  display: grid;
  gap: 14px;
}

.field {
  display: grid;
  gap: 8px;
}

.field-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.field span {
  color: #475569;
  font-size: 13px;
  font-weight: 700;
}

.field input,
.field textarea {
  width: 100%;
  border: 1px solid #d9e1ea;
  border-radius: 16px;
  padding: 14px 16px;
  color: #172033;
  font-size: 15px;
  outline: none;
  resize: vertical;
  font-family: inherit;
}

.field input {
  height: 52px;
  padding-block: 0;
}

.field input:focus,
.field textarea:focus {
  border-color: #2b31b3;
}

.error-text {
  margin: 0;
  color: #cb4051;
  font-size: 13px;
  line-height: 1.35;
}

.actions {
  display: flex;
  justify-content: flex-end;
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

.save-btn:disabled,
.ghost-btn:disabled {
  opacity: 0.6;
  cursor: default;
}

@media (max-width: 620px) {
  .editor-overlay {
    padding: 10px;
    align-items: flex-start;
  }

  .editor-card {
    max-height: calc(100vh - 20px);
    padding: 24px 18px 18px;
    border-radius: 24px;
  }

  .actions {
    flex-direction: column;
  }

  .field-grid {
    grid-template-columns: 1fr;
  }
}
</style>
