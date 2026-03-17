<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card" role="dialog" aria-modal="true" aria-label="Расширенный просмотр публикации">
      <button class="close-btn" type="button" @click="$emit('close')">×</button>

      <div class="top-layout">
        <aside class="left-col">
          <div class="preview-media" :style="mediaStyle">
            <div v-if="post.poster_url" class="preview-poster" :style="previewPosterStyle"></div>
            <div class="preview-glow preview-glow--first"></div>
            <div class="preview-glow preview-glow--second"></div>
            <div class="preview-grid"></div>

            <div class="preview-tags">
              <span class="tag">
                <img src="/assets/icons/Vector.png" alt="" />
                <span>Reels</span>
              </span>
              <span class="tag">
                <img src="/assets/icons/Vector-15.png" alt="" />
                <span>X{{ activityMultiplier }}</span>
              </span>
            </div>

            <span class="play-circle">▶</span>
          </div>

          <time class="left-date">{{ cardDate }}</time>

          <div class="left-author">
            <AppAvatar :seed="post.id" :size="40" alt="Креатор" :blurred="true" />
            <div class="left-author-meta">
              <p class="left-name">{{ handle }}</p>
              <p class="left-sub">{{ followers }}</p>
            </div>
            <button type="button" class="left-tool-btn" @click="handleRestrictedAction('Инструменты публикации')">
              <img src="/assets/icons/Vector-5.png" alt="" class="left-tool" />
            </button>
          </div>

          <p class="left-preview">{{ shortText(post.text, 108) }}</p>

          <div class="left-stats">
            <div class="left-stat-row">
              <span class="left-stat-label">
                <img src="/assets/icons/Vector-14.png" alt="" />
                <span>Просмотры</span>
              </span>
              <span>{{ metrics.views }}</span>
            </div>
            <div class="left-stat-row">
              <span class="left-stat-label">
                <img src="/assets/icons/Vector-11.png" alt="" />
                <span>Лайки</span>
              </span>
              <span>{{ metrics.likes }}</span>
            </div>
            <div class="left-stat-row">
              <span class="left-stat-label">
                <img src="/assets/icons/Vector-4.png" alt="" />
                <span>Комментарии</span>
              </span>
              <span>{{ metrics.comments }}</span>
            </div>
            <div class="left-stat-row">
              <span class="left-stat-label">
                <img src="/assets/icons/Vector-3.png" alt="" />
                <span>Репосты</span>
              </span>
              <span>{{ metrics.shares }}</span>
            </div>
            <div class="left-stat-row">
              <span class="left-stat-label">
                <img src="/assets/icons/Vector-12.png" alt="" />
                <span>ER</span>
              </span>
              <span>{{ metrics.er }}</span>
            </div>
          </div>
        </aside>

        <section class="right-col">
          <p class="meta-overline">Тема видео</p>
          <h2>{{ post.title }}</h2>

          <div class="info-line">
            <span class="info-pill">
              <span class="info-label">user_id:</span>
              <span>{{ post.user_id }}</span>
            </span>
            <span class="info-pill">
              <span class="info-label">created_at:</span>
              <span>{{ formatDateTime(post.created_at) }}</span>
            </span>
            <span class="info-pill">
              <span class="info-label">updated_at:</span>
              <span>{{ formatDateTime(post.updated_at) }}</span>
            </span>
            <button
              v-if="post.source_url"
              type="button"
              class="info-pill info-pill--link"
              @click="openSource"
            >
              <span class="info-label">source:</span>
              <span>Открыть</span>
            </button>
          </div>

          <div v-if="canManagePost" class="manage-row">
            <button type="button" class="manage-btn" :disabled="isSaving" @click="$emit('edit', post)">
              {{ isSaving ? "Сохраняем..." : "Редактировать" }}
            </button>
            <button type="button" class="manage-btn manage-btn--danger" :disabled="isDeleting" @click="$emit('delete', post)">
              {{ isDeleting ? "Удаляем..." : "Удалить" }}
            </button>
          </div>

          <div class="chips">
            <span class="chip chip-blue">Туториал</span>
            <span class="chip chip-green">Энергичное видео</span>
            <span class="chip chip-orange">Изи монтаж</span>
            <span class="chip chip-red">Трендовый звук</span>
            <span class="chip chip-yellow">Лид-магнит</span>
            <span class="chip chip-violet">Красота и здоровье</span>
          </div>

          <section v-if="post.video_url" class="content-block">
            <h3>Видео</h3>
            <div class="video-shell">
              <video class="video-player" controls playsinline preload="metadata" :poster="post.poster_url || undefined">
                <source :src="post.video_url" />
              </video>
            </div>
          </section>

          <section class="content-block">
            <div class="block-header">
              <h3>Транскрибация</h3>
              <button type="button" class="translated-pill" @click="handleRestrictedAction('Перевод публикации')">
                Переведено
              </button>
            </div>

            <div class="block-body">
              <p>{{ shortText(post.text, 320) }}</p>
              <p>{{ shortText(post.text, 260) }}</p>
            </div>
          </section>

          <button class="adapt-btn" type="button" @click="handleRestrictedAction('Адаптировать публикацию')">
            <img src="/assets/icons/Vector-5.png" alt="" />
            <span>Адаптировать</span>
          </button>

          <section class="content-block">
            <h3>Суть</h3>
            <div class="block-body">
              <p>{{ post.text }}</p>
            </div>
          </section>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

import AppAvatar from "./AppAvatar.vue";
import { formatDateTime } from "../services/dateFormatter";
import { buildFollowers, buildHandle, buildMediaPalette, buildPostMetrics } from "../services/postPresentation";

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
  canManagePost: {
    type: Boolean,
    default: false,
  },
  isSaving: {
    type: Boolean,
    default: false,
  },
  isDeleting: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close", "placeholder", "edit", "delete"]);

const metrics = computed(() => buildPostMetrics(props.post.id));
const handle = computed(() => buildHandle(props.post.user_id));
const followers = computed(() => buildFollowers(props.post.user_id));
const activityMultiplier = computed(() => ((props.post.id % 12) + 3).toString());

const mediaStyle = computed(() => {
  const palette = buildMediaPalette(props.post.id);

  return {
    "--preview-start": palette.start,
    "--preview-end": palette.end,
    "--preview-glow": palette.glow,
  };
});

const previewPosterStyle = computed(() => {
  if (!props.post.poster_url) return {};

  return {
    backgroundImage: `url(${props.post.poster_url})`,
  };
});

const cardDate = computed(() => {
  if (!props.post.created_at) return "—";
  const date = new Date(props.post.created_at);
  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  }).format(date);
});

function handleRestrictedAction(label) {
  emit("placeholder", label);
}

function shortText(text, maxLength) {
  if (!text) return "";
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength)}...`;
}

function openSource() {
  if (!props.post.source_url) return;
  window.open(props.post.source_url, "_blank", "noopener,noreferrer");
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(7, 9, 15, 0.62);
  backdrop-filter: blur(2px);
  display: grid;
  place-items: start end;
}

.modal-card {
  width: clamp(640px, 72vw, 980px);
  max-height: 100vh;
  overflow: auto;
  background: #ffffff;
  border-radius: 16px 0 0 16px;
  padding: 16px;
  position: relative;
}

.close-btn {
  position: absolute;
  right: 16px;
  top: 16px;
  border: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #eef1f4;
  color: #98a3af;
  font-size: 20px;
  line-height: 1;
  cursor: pointer;
}

.top-layout {
  display: grid;
  grid-template-columns: 228px minmax(0, 1fr);
  gap: 22px;
}

.preview-media {
  position: relative;
  height: 350px;
  border-radius: 16px;
  overflow: hidden;
  background:
    radial-gradient(circle at 24% 22%, var(--preview-glow) 0, transparent 34%),
    linear-gradient(160deg, var(--preview-start) 0%, var(--preview-end) 100%);
}

.preview-poster {
  position: absolute;
  inset: 0;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  opacity: 0.9;
}

.preview-glow {
  position: absolute;
  border-radius: 999px;
  filter: blur(12px);
}

.preview-glow--first {
  width: 156px;
  height: 156px;
  right: -14px;
  top: 56px;
  background: var(--preview-glow);
}

.preview-glow--second {
  width: 122px;
  height: 122px;
  left: -20px;
  bottom: 94px;
  background: rgba(255, 255, 255, 0.15);
}

.preview-grid {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 22px 22px;
}

.preview-tags {
  position: absolute;
  left: 12px;
  top: 12px;
  display: grid;
  gap: 6px;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  color: #ffffff;
  padding: 4px 8px;
  font-size: 12px;
  line-height: 14.5px;
}

.tag img {
  width: 16px;
  height: 16px;
}

.play-circle {
  position: absolute;
  inset: 0;
  margin: auto;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(240, 244, 249, 0.95);
  display: grid;
  place-items: center;
  color: #4d5a65;
  font-size: 14px;
}

.left-date {
  margin-top: 8px;
  display: block;
  color: #a0adb4;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
}

.left-author {
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.left-name {
  margin: 0;
  color: #2b31b3;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.1px;
  font-weight: 600;
}

.left-sub {
  margin: 0;
  color: #4e616b;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.4px;
}

.left-tool-btn {
  margin-left: auto;
  border: 0;
  background: transparent;
  padding: 0;
  cursor: pointer;
}

.left-tool {
  width: 24px;
  height: 24px;
}

.left-preview {
  margin: 6px 0 0;
  color: #4e616b;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
}

.left-stats {
  margin-top: 6px;
  display: grid;
  gap: 4px;
}

.left-stat-row {
  min-height: 28px;
  border-radius: 8px;
  background: #f5f7fa;
  border: 1px solid #ecf0f3;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 10px;
  color: #4e616b;
  font-size: 12px;
  line-height: 14.5px;
}

.left-stat-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.left-stat-label img {
  width: 14px;
  height: 14px;
}

.right-col {
  padding-right: 24px;
}

.meta-overline {
  margin: 0;
  color: #6f7f8c;
  font-size: 14px;
  line-height: 18px;
}

h2 {
  margin: 6px 0 0;
  color: #151c29;
  font-size: 46px;
  line-height: 1.06;
  letter-spacing: -0.03em;
  font-weight: 700;
}

.info-line {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.info-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  border-radius: 999px;
  background: #f3f5f8;
  color: #5e7180;
  padding: 6px 10px;
  font-size: 12px;
  line-height: 1;
}

.info-pill--link {
  border: 0;
  cursor: pointer;
}

.info-label {
  color: #9ca7b0;
}

.manage-row {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.manage-btn {
  min-width: 142px;
  height: 40px;
  border: 1px solid #d5ddf0;
  border-radius: 12px;
  background: #f8fafc;
  color: #2b31b3;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.manage-btn--danger {
  border-color: #f0c5cd;
  background: #fff4f6;
  color: #c34b5e;
}

.manage-btn:disabled {
  opacity: 0.6;
  cursor: default;
}

.chips {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 12px;
  line-height: 14px;
  font-weight: 700;
}

.chip-blue { background: #dde1ff; color: #4758cd; }
.chip-green { background: #def4d9; color: #4c9a41; }
.chip-orange { background: #ffe8cd; color: #ab6b23; }
.chip-red { background: #ffe0e8; color: #cc4d66; }
.chip-yellow { background: #ffeecb; color: #b17f1b; }
.chip-violet { background: #e4e6ff; color: #5f62cf; }

.content-block {
  margin-top: 14px;
}

.block-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.content-block h3 {
  margin: 0 0 8px;
  color: #1c2436;
  font-size: 32px;
  line-height: 1.1;
  font-weight: 700;
}

.translated-pill {
  border: 0;
  border-radius: 999px;
  background: #f2f4fb;
  color: #5a63d0;
  padding: 8px 12px;
  font-size: 13px;
  line-height: 1;
  font-weight: 700;
  cursor: pointer;
}

.block-body {
  border-radius: 8px;
  background: #f2f4f6;
  padding: 12px;
}

.block-body p {
  margin: 0;
  color: #5f7280;
  font-size: 14px;
  line-height: 1.45;
}

.block-body p + p {
  margin-top: 8px;
}

.video-shell {
  border-radius: 12px;
  overflow: hidden;
  background: #0f172a;
}

.video-player {
  display: block;
  width: 100%;
  max-height: 420px;
  background: #0f172a;
}

.adapt-btn {
  margin-top: 14px;
  width: 220px;
  height: 56px;
  border: 0;
  border-radius: 12px;
  background: #2b31b3;
  color: #ffffff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
}

.adapt-btn img {
  width: 20px;
  height: 20px;
}

@media (max-width: 980px) {
  .modal-overlay {
    place-items: center;
    padding: 8px;
  }

  .modal-card {
    width: min(920px, 100%);
    border-radius: 12px;
  }

  .top-layout {
    grid-template-columns: 1fr;
  }

  .left-col {
    width: 228px;
  }

  .right-col {
    padding-right: 0;
  }

  h2 {
    font-size: 28px;
  }
}
</style>
