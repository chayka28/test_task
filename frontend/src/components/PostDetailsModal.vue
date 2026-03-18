<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card" role="dialog" aria-modal="true" aria-label="Открытая публикация">
      <button class="close-btn" type="button" @click="$emit('close')">×</button>

      <div class="modal-layout">
        <aside class="left-panel">
          <div class="preview-card">
            <div class="preview-media" :style="mediaStyle">
              <div v-if="post.poster_url" class="preview-poster" :style="previewPosterStyle"></div>
              <div class="preview-glow preview-glow--first"></div>
              <div class="preview-glow preview-glow--second"></div>
              <div class="preview-grid"></div>

              <div class="preview-top">
                <div class="preview-tags">
                  <span class="tag-pill">
                    <img src="/assets/icons/Vector.png" alt="" />
                    <span>Reels</span>
                  </span>
                  <span class="tag-pill">
                    <img src="/assets/icons/Vector-15.png" alt="" />
                    <span>X{{ activityMultiplier }}</span>
                  </span>
                </div>

                <div class="preview-actions">
                  <button type="button" class="preview-icon" @click="handleRestrictedAction('Избранное')">♡</button>
                  <button type="button" class="preview-icon" @click="openSource">↗</button>
                </div>
              </div>

              <span class="play-circle">▶</span>

              <div class="preview-stats-overlay">
                <div class="preview-stat">
                  <img src="/assets/icons/Vector-14.png" alt="" />
                  <span>{{ metrics.views }}</span>
                </div>
                <div class="preview-stat">
                  <img src="/assets/icons/Vector-11.png" alt="" />
                  <span>{{ metrics.likes }}</span>
                </div>
                <div class="preview-stat">
                  <img src="/assets/icons/Vector-4.png" alt="" />
                  <span>{{ metrics.comments }}</span>
                </div>
                <div class="preview-stat">
                  <img src="/assets/icons/Vector-3.png" alt="" />
                  <span>{{ metrics.shares }}</span>
                </div>
              </div>
            </div>

            <time class="preview-date">{{ cardDate }}</time>

            <div class="author-row">
              <AppAvatar :seed="post.user_id" :size="42" alt="Креатор" :blurred="true" />
              <div class="author-copy">
                <p class="author-name">{{ handle }}</p>
                <p class="author-sub">{{ followers }}</p>
              </div>
              <button type="button" class="author-tool-btn" @click="handleRestrictedAction('Инструменты публикации')">
                <img src="/assets/icons/Vector-5.png" alt="" />
              </button>
            </div>

            <p class="preview-caption">{{ shortText(post.text, 118) }}</p>
            <button type="button" class="preview-more" @click="handleRestrictedAction('Раскрыть описание')">Еще</button>

            <div class="metric-list">
              <div class="metric-row">
                <span class="metric-label">
                  <img src="/assets/icons/Vector-14.png" alt="" />
                  <span>Просмотры</span>
                </span>
                <span>{{ metrics.views }}</span>
              </div>
              <div class="metric-row">
                <span class="metric-label">
                  <img src="/assets/icons/Vector-11.png" alt="" />
                  <span>Лайки</span>
                </span>
                <span>{{ metrics.likes }}</span>
              </div>
              <div class="metric-row">
                <span class="metric-label">
                  <img src="/assets/icons/Vector-4.png" alt="" />
                  <span>Комментарии</span>
                </span>
                <span>{{ metrics.comments }}</span>
              </div>
              <div class="metric-row">
                <span class="metric-label">
                  <img src="/assets/icons/Vector-3.png" alt="" />
                  <span>Репосты</span>
                </span>
                <span>{{ metrics.shares }}</span>
              </div>
              <div class="metric-row">
                <span class="metric-label">
                  <img src="/assets/icons/Vector-12.png" alt="" />
                  <span>ER</span>
                </span>
                <span>{{ metrics.er }}</span>
              </div>
            </div>
          </div>
        </aside>

        <section class="right-panel">
          <p class="section-overline">Тема видео</p>
          <h2>{{ post.title }}</h2>

          <div class="meta-line">
            <span class="meta-chip">
              <span class="meta-icon">♪</span>
              <span>Tyga - Pop it off</span>
            </span>
            <span class="meta-chip">
              <span class="meta-label">Язык:</span>
              <span class="flag-uk" aria-hidden="true"></span>
              <span>Английский</span>
            </span>
          </div>

          <div class="chips">
            <span class="chip chip-blue">Туториал</span>
            <span class="chip chip-green">Энергичное видео</span>
            <span class="chip chip-orange">Изи монтаж</span>
            <span class="chip chip-red">Трендовый звук</span>
            <span class="chip chip-yellow">Лид магнит</span>
            <span class="chip chip-violet">Красота и здоровье</span>
          </div>

          <div class="service-info">
            <span class="service-pill">user_id: {{ post.user_id }}</span>
            <span class="service-pill">created_at: {{ formatDateTime(post.created_at) }}</span>
            <span class="service-pill">updated_at: {{ formatDateTime(post.updated_at) }}</span>
          </div>

          <div v-if="canManagePost" class="manage-row">
            <button type="button" class="manage-btn" :disabled="isSaving" @click="$emit('edit', post)">
              {{ isSaving ? "Сохраняем..." : "Редактировать" }}
            </button>
            <button type="button" class="manage-btn manage-btn--danger" :disabled="isDeleting" @click="$emit('delete', post)">
              {{ isDeleting ? "Удаляем..." : "Удалить" }}
            </button>
          </div>

          <section v-if="post.video_url" class="content-section">
            <div class="section-head">
              <h3>Видео</h3>
            </div>
            <div class="video-shell">
              <video class="video-player" controls playsinline preload="metadata" :poster="post.poster_url || undefined">
                <source :src="post.video_url" />
              </video>
            </div>
          </section>

          <section class="content-section">
            <div class="section-head">
              <h3>Транскрибация</h3>
              <div class="section-tools">
                <button type="button" class="translated-pill" @click="handleRestrictedAction('Перевод публикации')">Переведено</button>
                <button type="button" class="copy-btn" @click="handleRestrictedAction('Копирование блока')">⧉</button>
              </div>
            </div>

            <div class="copy-card">
              <p v-for="paragraph in transcriptionParagraphs" :key="paragraph">{{ paragraph }}</p>
              <button type="button" class="inline-more" @click="handleRestrictedAction('Раскрыть транскрибацию')">Еще</button>
            </div>
          </section>

          <button class="adapt-btn" type="button" @click="handleRestrictedAction('Адаптировать публикацию')">
            <img src="/assets/icons/Vector-5.png" alt="" />
            <span>Адаптировать</span>
          </button>

          <section class="content-section">
            <div class="section-head">
              <h3>Суть</h3>
            </div>
            <div class="copy-card copy-card--soft">
              <p>{{ essenceText }}</p>
            </div>
          </section>

          <section class="content-section">
            <div class="section-head">
              <h3>Структура</h3>
            </div>
            <div class="timeline-card">
              <div v-for="step in structureSteps" :key="step.time" class="timeline-row">
                <span class="timeline-time">{{ step.time }}</span>
                <span class="timeline-point"></span>
                <div class="timeline-copy">
                  <strong>{{ step.title }}</strong>
                  <p>{{ step.text }}</p>
                </div>
              </div>
            </div>
          </section>

          <section v-for="hook in hookBlocks" :key="hook.title" class="content-section content-section--compact">
            <div class="section-head">
              <h4>{{ hook.title }}</h4>
              <button type="button" class="copy-btn" @click="handleRestrictedAction('Копирование блока')">⧉</button>
            </div>
            <div class="copy-card copy-card--soft">
              <p>{{ hook.text }}</p>
            </div>
          </section>

          <section class="content-section">
            <div class="section-head">
              <h3>Рабочие приемы</h3>
              <button type="button" class="copy-btn" @click="handleRestrictedAction('Копирование блока')">⧉</button>
            </div>
            <div class="copy-card copy-card--article">
              <article v-for="item in workBlocks" :key="item.title" class="article-block">
                <h4>{{ item.title }}</h4>
                <p>{{ item.text }}</p>
              </article>
            </div>
          </section>

          <section class="content-section">
            <div class="section-head">
              <h3>Воронка / Маркетинг</h3>
              <button type="button" class="copy-btn" @click="handleRestrictedAction('Копирование блока')">⧉</button>
            </div>
            <div class="copy-card copy-card--article">
              <article v-for="item in marketingBlocks" :key="item.title" class="article-block article-block--tight">
                <h4>{{ item.title }}</h4>
                <p>{{ item.text }}</p>
              </article>
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

const paragraphs = computed(() => {
  const chunks = (props.post.text || "")
    .split(/\n+/)
    .map((item) => item.trim())
    .filter(Boolean);

  return chunks.length ? chunks : ["Описание публикации пока не заполнено."];
});

const transcriptionParagraphs = computed(() => paragraphs.value.slice(0, 3));

const essenceText = computed(() => {
  return paragraphs.value[1] || paragraphs.value[0];
});

const structureSteps = computed(() => {
  return [
    {
      time: "0–3 сек",
      title: "Шок-сравнение",
      text: shortText(paragraphs.value[0], 104),
    },
    {
      time: "3–15 сек",
      title: "Сюжет",
      text: shortText(paragraphs.value[1] || paragraphs.value[0], 112),
    },
    {
      time: "15–120 сек",
      title: "Финал / CTA",
      text: shortText(paragraphs.value[2] || paragraphs.value[0], 96),
    },
  ];
});

const hookBlocks = computed(() => {
  return [
    {
      title: "Хук фраза",
      text: shortText(paragraphs.value[0], 84),
    },
    {
      title: "Визуальный хук",
      text: shortText(paragraphs.value[1] || paragraphs.value[0], 84),
    },
    {
      title: "Текстовый хук",
      text: shortText(paragraphs.value[2] || paragraphs.value[0], 84),
    },
  ];
});

const workBlocks = computed(() => {
  return [
    {
      title: "2. Суть видео",
      text: shortText(paragraphs.value[0], 220),
    },
    {
      title: "3. Монтаж",
      text: shortText(paragraphs.value[1] || paragraphs.value[0], 220),
    },
    {
      title: "4. Реплики",
      text: shortText(paragraphs.value[2] || paragraphs.value[0], 220),
    },
  ];
});

const marketingBlocks = computed(() => {
  return [
    {
      title: "CTA голос/визуал",
      text: shortText(paragraphs.value[0], 144),
    },
    {
      title: "Триггер",
      text: shortText(paragraphs.value[1] || paragraphs.value[0], 144),
    },
    {
      title: "Куда ведет",
      text: shortText(paragraphs.value[2] || paragraphs.value[0], 144),
    },
    {
      title: "Лид-магнит",
      text: shortText(paragraphs.value[0], 144),
    },
  ];
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
  if (props.post.source_url) {
    window.open(props.post.source_url, "_blank", "noopener,noreferrer");
    return;
  }

  handleRestrictedAction("Открыть источник");
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
  padding: 8px;
}

.modal-card {
  width: min(1110px, calc(100vw - 16px));
  max-height: calc(100vh - 16px);
  overflow: auto;
  background: #ffffff;
  border-radius: 18px;
  padding: 18px 18px 22px;
  position: relative;
  box-shadow: 0 22px 80px rgba(15, 23, 42, 0.18);
}

.close-btn {
  position: absolute;
  right: 16px;
  top: 16px;
  border: 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #eef1f4;
  color: #98a3af;
  font-size: 22px;
  line-height: 1;
  cursor: pointer;
}

.modal-layout {
  display: grid;
  grid-template-columns: 212px minmax(0, 1fr);
  gap: 22px;
}

.preview-card {
  position: sticky;
  top: 0;
}

.preview-media {
  position: relative;
  height: 376px;
  border-radius: 18px;
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
  opacity: 0.92;
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
  background: rgba(255, 255, 255, 0.14);
}

.preview-grid {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 22px 22px;
}

.preview-top {
  position: absolute;
  inset: 12px 12px auto 12px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.preview-tags {
  display: grid;
  gap: 6px;
}

.tag-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 9px;
  background: rgba(35, 29, 24, 0.62);
  backdrop-filter: blur(8px);
  color: #ffffff;
  padding: 5px 8px;
  font-size: 12px;
  line-height: 1;
}

.tag-pill img {
  width: 16px;
  height: 16px;
}

.preview-actions {
  display: grid;
  gap: 8px;
}

.preview-icon {
  width: 36px;
  height: 36px;
  border: 0;
  border-radius: 12px;
  background: rgba(30, 24, 20, 0.56);
  color: #ffffff;
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
}

.play-circle {
  position: absolute;
  inset: 0;
  margin: auto;
  width: 54px;
  height: 54px;
  border-radius: 18px;
  background: rgba(247, 249, 252, 0.96);
  display: grid;
  place-items: center;
  color: #44515f;
  font-size: 18px;
}

.preview-stats-overlay {
  position: absolute;
  left: 16px;
  right: 16px;
  bottom: 14px;
  height: 64px;
  border-radius: 18px;
  background: rgba(52, 23, 15, 0.58);
  backdrop-filter: blur(16px);
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  align-items: center;
  padding: 0 12px;
}

.preview-stat {
  display: grid;
  justify-items: center;
  gap: 6px;
  color: #ffffff;
  font-size: 11px;
  line-height: 1;
}

.preview-stat img {
  width: 18px;
  height: 18px;
}

.preview-date {
  margin-top: 10px;
  display: block;
  color: #a0adb4;
  font-size: 12px;
  line-height: 14px;
}

.author-row {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-copy {
  min-width: 0;
}

.author-name {
  margin: 0;
  color: #2b31b3;
  font-size: 13px;
  line-height: 18px;
  font-weight: 700;
}

.author-sub {
  margin: 0;
  color: #5f7280;
  font-size: 12px;
  line-height: 16px;
}

.author-tool-btn {
  margin-left: auto;
  border: 0;
  padding: 0;
  background: transparent;
  cursor: pointer;
}

.author-tool-btn img {
  width: 24px;
  height: 24px;
}

.preview-caption {
  margin: 8px 0 0;
  color: #3f4d59;
  font-size: 12px;
  line-height: 1.34;
}

.preview-more {
  margin-top: 2px;
  border: 0;
  padding: 0;
  background: transparent;
  color: #111827;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.metric-list {
  margin-top: 8px;
  display: grid;
  gap: 6px;
}

.metric-row {
  min-height: 38px;
  border-radius: 12px;
  background: #f3f5f8;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12px;
  color: #4e616b;
  font-size: 12px;
  line-height: 1;
}

.metric-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.metric-label img {
  width: 14px;
  height: 14px;
}

.right-panel {
  padding-right: 18px;
}

.section-overline {
  margin: 0;
  color: #6f7f8c;
  font-size: 14px;
  line-height: 18px;
}

h2 {
  margin: 6px 0 0;
  color: #151c29;
  font-size: 26px;
  line-height: 1.15;
  font-weight: 800;
  max-width: 720px;
}

.meta-line {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.meta-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #637381;
  font-size: 14px;
}

.meta-icon {
  color: #ffb533;
  font-size: 15px;
}

.meta-label {
  color: #8a97a4;
}

.flag-uk {
  width: 16px;
  height: 12px;
  border-radius: 2px;
  display: inline-block;
  background:
    linear-gradient(90deg, transparent 42%, #ffffff 42% 58%, transparent 58%),
    linear-gradient(transparent 42%, #ffffff 42% 58%, transparent 58%),
    linear-gradient(90deg, transparent 46%, #c2303f 46% 54%, transparent 54%),
    linear-gradient(transparent 46%, #c2303f 46% 54%, transparent 54%),
    #2849b8;
}

.chips {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  border-radius: 999px;
  padding: 7px 12px;
  font-size: 12px;
  line-height: 1;
  font-weight: 700;
}

.chip-blue { background: #dde1ff; color: #4758cd; }
.chip-green { background: #def4d9; color: #4c9a41; }
.chip-orange { background: #ffe8cd; color: #ab6b23; }
.chip-red { background: #ffe0e8; color: #cc4d66; }
.chip-yellow { background: #ffeecb; color: #b17f1b; }
.chip-violet { background: #e4e6ff; color: #5f62cf; }

.service-info {
  margin-top: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.service-pill {
  border-radius: 999px;
  background: #f3f5f8;
  color: #667685;
  padding: 7px 12px;
  font-size: 12px;
  line-height: 1;
}

.manage-row {
  margin-top: 14px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.manage-btn {
  min-width: 144px;
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

.content-section {
  margin-top: 18px;
}

.content-section--compact {
  margin-top: 12px;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.section-head h3,
.section-head h4 {
  margin: 0;
  color: #1c2436;
  font-weight: 800;
}

.section-head h3 {
  font-size: 18px;
  line-height: 1.2;
}

.section-head h4 {
  font-size: 16px;
  line-height: 1.2;
}

.section-tools {
  display: flex;
  align-items: center;
  gap: 8px;
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

.copy-btn {
  width: 32px;
  height: 32px;
  border: 0;
  border-radius: 10px;
  background: #f3f5f8;
  color: #7a8794;
  font-size: 14px;
  line-height: 1;
  cursor: pointer;
}

.copy-card {
  margin-top: 10px;
  border-radius: 12px;
  background: #f3f5f7;
  padding: 14px;
}

.copy-card--soft {
  background: #f4f6f8;
}

.copy-card--article {
  padding: 16px;
}

.copy-card p {
  margin: 0;
  color: #627380;
  font-size: 14px;
  line-height: 1.54;
}

.copy-card p + p {
  margin-top: 12px;
}

.inline-more {
  margin-top: 12px;
  margin-left: auto;
  display: block;
  border: 0;
  padding: 0;
  background: transparent;
  color: #111827;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.video-shell {
  margin-top: 10px;
  border-radius: 12px;
  overflow: hidden;
  background: #0f172a;
}

.video-player {
  display: block;
  width: 100%;
  max-height: 360px;
  background: #0f172a;
}

.adapt-btn {
  margin-top: 18px;
  width: 180px;
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

.timeline-card {
  margin-top: 10px;
  border-radius: 12px;
  padding: 8px 0;
}

.timeline-row {
  display: grid;
  grid-template-columns: 84px 20px minmax(0, 1fr);
  gap: 10px;
  align-items: start;
  padding: 12px 0;
}

.timeline-row + .timeline-row {
  border-top: 1px solid #eef2f6;
}

.timeline-time {
  color: #8f9ba7;
  font-size: 13px;
  line-height: 1.4;
}

.timeline-point {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid #5162dd;
  margin-top: 4px;
  position: relative;
}

.timeline-copy strong {
  display: block;
  color: #111827;
  font-size: 15px;
  line-height: 1.35;
}

.timeline-copy p {
  margin: 6px 0 0;
  color: #627380;
  font-size: 14px;
  line-height: 1.45;
}

.article-block + .article-block {
  margin-top: 18px;
}

.article-block h4 {
  margin: 0 0 8px;
  color: #111827;
  font-size: 16px;
  line-height: 1.35;
}

.article-block p {
  color: #627380;
}

.article-block--tight + .article-block--tight {
  margin-top: 16px;
}

@media (max-width: 980px) {
  .modal-overlay {
    place-items: center;
    padding: 8px;
  }

  .modal-card {
    width: min(920px, 100%);
    border-radius: 14px;
  }

  .modal-layout {
    grid-template-columns: 1fr;
  }

  .preview-card {
    position: static;
    max-width: 228px;
  }

  .right-panel {
    padding-right: 0;
  }
}

@media (max-width: 640px) {
  .modal-card {
    padding: 14px 12px 18px;
  }

  .preview-card {
    max-width: none;
  }

  .preview-media {
    height: 340px;
  }

  h2 {
    font-size: 22px;
  }

  .meta-line,
  .service-info,
  .chips,
  .manage-row {
    gap: 8px;
  }

  .timeline-row {
    grid-template-columns: 70px 16px minmax(0, 1fr);
    gap: 8px;
  }
}
</style>
