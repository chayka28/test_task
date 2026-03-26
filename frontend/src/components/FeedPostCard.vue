<template>
  <article class="post-card">
    <div
      class="card-hitbox"
      role="button"
      tabindex="0"
      @click="$emit('open', post)"
      @keydown.enter.prevent="$emit('open', post)"
      @keydown.space.prevent="$emit('open', post)"
    >
      <div class="media" :style="mediaStyle">
        <div v-if="post.poster_url" class="media-poster" :style="mediaPosterStyle"></div>
        <div class="media-glow media-glow--first"></div>
        <div class="media-glow media-glow--second"></div>
        <div class="media-grid"></div>

        <div v-if="badgeToRender" class="showcase-badge" :class="`showcase-badge--${badgeToRender.tone}`">
          <img src="/assets/icons/Vector-40.png" alt="" />
          <span>{{ badgeToRender.label }}</span>
        </div>

        <div class="media-header">
          <div class="tags" :class="{ 'tags--offset': badgeToRender }">
            <span class="tag-pill">
              <img src="/assets/icons/Vector-33.png" alt="" class="tag-icon" />
              <span>Reels</span>
            </span>
            <span class="tag-pill">
              <img src="/assets/icons/Vector-1.png" alt="" class="tag-icon" />
              <span>X{{ activityMultiplier }}</span>
            </span>
          </div>

          <div class="actions">
            <button
              type="button"
              class="action-pill like-btn"
              :class="{ 'is-liked': liked, 'is-animating': isLikeAnimating }"
              @click.stop="handleLikeClick"
            >
              <img src="/assets/icons/Heart.png" alt="" />
            </button>

            <button type="button" class="action-pill external-btn" @click.stop="handleRestrictedAction('Открыть источник')">
              <img src="/assets/icons/external-link.png" alt="" />
            </button>
          </div>
        </div>

        <div class="stats-overlay">
          <div class="stat-cell">
            <img src="/assets/icons/Vector-2.png" alt="" />
            <span>{{ metrics.views }}</span>
          </div>
          <div class="stat-cell">
            <img src="/assets/icons/Heart.png" alt="" />
            <span>{{ metrics.likes }}</span>
          </div>
          <div class="stat-cell">
            <img src="/assets/icons/Vector-4.png" alt="" />
            <span>{{ metrics.comments }}</span>
          </div>
          <div class="stat-cell">
            <img src="/assets/icons/Icon.png" alt="" />
            <span>{{ metrics.shares }}</span>
          </div>
        </div>
      </div>

      <div class="author-card" role="button" tabindex="0" @click.stop="$emit('open-user-posts', post)">
        <AppAvatar :avatar="post.poster_url || ''" :seed="post.id" :size="32" alt="Креатор" />
        <div class="author-meta">
          <p class="author-name">{{ authorHandle }}</p>
          <p class="author-sub">{{ followers }}</p>
        </div>
        <button type="button" class="author-tool-btn" @click.stop="handleRestrictedAction('Инструменты карточки')">
          <img src="/assets/icons/Icon-1.png" alt="" class="author-tool" />
        </button>
      </div>

      <p class="title">{{ post.title }}</p>
      <p class="text">{{ previewText }}</p>
    </div>

    <div class="bottom-meta">
      <time class="date">{{ formattedCreatedAt }}</time>
      <button type="button" class="bottom-action-btn" @click="$emit('open', post)">Анализ</button>
    </div>
  </article>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from "vue";

import AppAvatar from "./AppAvatar.vue";
import {
  buildFollowers,
  buildMediaPalette,
  buildPostMetrics,
  buildUserHandle,
} from "../services/postPresentation";

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
  liked: {
    type: Boolean,
    default: false,
  },
  canInteract: {
    type: Boolean,
    default: false,
  },
  leaderBadge: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["open", "toggle-like", "placeholder", "auth-required", "open-user-posts"]);

const isLikeAnimating = ref(false);
let likeAnimationTimerId = null;

const metrics = computed(() => buildPostMetrics(props.post.id));
const authorHandle = computed(() => buildUserHandle(props.post.user_name, props.post.user_id));
const followers = computed(() => buildFollowers(props.post.user_id));
const activityMultiplier = computed(() => ((props.post.id % 12) + 3).toString());
const badgeToRender = computed(() => props.leaderBadge);

const mediaStyle = computed(() => {
  const palette = buildMediaPalette(props.post.id);

  return {
    "--media-start": palette.start,
    "--media-end": palette.end,
    "--media-glow": palette.glow,
    "--media-surface": palette.surface,
  };
});

const mediaPosterStyle = computed(() => {
  if (!props.post.poster_url) return {};

  return {
    backgroundImage: `url(${props.post.poster_url})`,
  };
});

const previewText = computed(() => {
  const raw = props.post.text || "";
  if (raw.length <= 74) return raw;
  return `${raw.slice(0, 74)}...`;
});

const formattedCreatedAt = computed(() => {
  if (!props.post.created_at) return "-";
  const date = new Date(props.post.created_at);
  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  }).format(date);
});

function handleRestrictedAction(label) {
  if (label === "Открыть источник" && props.post.source_url) {
    window.open(props.post.source_url, "_blank", "noopener,noreferrer");
    return;
  }

  emit("placeholder", label);
}

function handleLikeClick() {
  if (!props.canInteract) {
    emit("auth-required", "Избранное");
    return;
  }

  if (!props.liked) {
    isLikeAnimating.value = true;

    if (likeAnimationTimerId) {
      window.clearTimeout(likeAnimationTimerId);
    }

    likeAnimationTimerId = window.setTimeout(() => {
      isLikeAnimating.value = false;
      likeAnimationTimerId = null;
    }, 760);
  }

  emit("toggle-like", props.post);
}

onBeforeUnmount(() => {
  if (likeAnimationTimerId) {
    window.clearTimeout(likeAnimationTimerId);
  }
});
</script>

<style scoped>
.post-card {
  width: 100%;
  min-height: 0;
  border-radius: 16px;
  background: transparent;
}

.card-hitbox {
  width: 100%;
  padding: 0;
  text-align: left;
  cursor: pointer;
}

.media {
  position: relative;
  width: 100%;
  aspect-ratio: 264 / 404;
  border-radius: 16px;
  overflow: hidden;
  background:
    radial-gradient(circle at 24% 22%, var(--media-glow) 0, transparent 34%),
    linear-gradient(160deg, var(--media-start) 0%, var(--media-end) 100%);
}

.media-poster {
  position: absolute;
  inset: 0;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  filter: saturate(0.96) contrast(1.02);
  opacity: 0.92;
}

.media-glow {
  position: absolute;
  border-radius: 999px;
  filter: blur(12px);
  opacity: 0.88;
}

.media-glow--first {
  width: 148px;
  height: 148px;
  right: -16px;
  top: 54px;
  background: var(--media-glow);
}

.media-glow--second {
  width: 118px;
  height: 118px;
  left: -18px;
  bottom: 96px;
  background: rgba(255, 255, 255, 0.16);
}

.media-grid {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 22px 22px;
  opacity: 0.45;
}

.showcase-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  height: 24px;
  border-radius: 8px;
  padding: 0 9px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #ffffff;
  font-size: 11px;
  line-height: 1;
  font-weight: 700;
  z-index: 1;
  max-width: calc(100% - 54px);
}

.showcase-badge img {
  width: 12px;
  height: 12px;
  object-fit: contain;
}

.showcase-badge--views {
  background: #ad7dff;
}

.showcase-badge--likes {
  background: #ff5b8f;
}

.showcase-badge--comments {
  background: #46c625;
}

.media-header {
  position: absolute;
  inset: 12px 10px auto 10px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.tags {
  display: grid;
  gap: 6px;
}

.tags--offset {
  margin-top: 30px;
}

.tag-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 30px;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.42);
  backdrop-filter: blur(8px);
  padding: 0 9px;
  color: #ffffff;
  font-size: 12px;
  line-height: 1;
  letter-spacing: 0.02em;
  font-weight: 500;
}

.tag-icon {
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.actions {
  display: grid;
  gap: 8px;
}

.action-pill {
  width: 36px;
  height: 36px;
  border-radius: 11px;
  background: rgba(0, 0, 0, 0.42);
  backdrop-filter: blur(8px);
  display: grid;
  place-items: center;
  border: 0;
  color: #ffffff;
  cursor: pointer;
}

.action-pill img {
  width: 18px;
  height: 18px;
  object-fit: contain;
}

.like-btn img {
  transform-origin: center;
}

.like-btn.is-liked img {
  filter: invert(17%) sepia(98%) saturate(5042%) hue-rotate(338deg) brightness(105%) contrast(104%);
}

.like-btn.is-animating img {
  animation: heart-quarter-turn 0.76s steps(4, end) forwards;
}

.external-btn img {
  width: 18px;
  height: 18px;
}

.stats-overlay {
  position: absolute;
  left: 12px;
  right: 12px;
  bottom: 9px;
  border-radius: 14px;
  background: rgba(60, 27, 28, 0.74);
  backdrop-filter: blur(10px);
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  padding: 8px 6px 9px;
}

.stat-cell {
  display: grid;
  justify-items: center;
  gap: 5px;
  color: #ffffff;
  font-size: 12px;
  line-height: 1;
  font-weight: 500;
}

.stat-cell img {
  width: 18px;
  height: 18px;
  object-fit: contain;
}

.author-card {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  text-align: left;
}

.author-meta {
  min-width: 0;
}

.author-name {
  margin: 0;
  color: #2f38c7;
  font-size: var(--font-heading-6-size);
  line-height: var(--font-heading-6-line);
  font-weight: var(--font-heading-6-weight);
}

.author-sub {
  margin: 2px 0 0;
  color: #7d8a96;
  font-size: var(--font-caption-size);
  line-height: var(--font-caption-line);
  font-weight: var(--font-caption-weight);
}

.author-tool-btn {
  margin-left: auto;
  border: 0;
  background: transparent;
  padding: 2px;
  display: grid;
  place-items: center;
  cursor: pointer;
}

.author-tool {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.title {
  margin: 8px 0 2px;
  color: #202b38;
  font-size: var(--font-caption-size);
  line-height: var(--font-caption-line);
  font-weight: var(--font-caption-weight);
  min-height: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.text {
  margin: 0;
  color: #536875;
  font-size: var(--font-caption-size);
  line-height: var(--font-caption-line);
  font-weight: var(--font-caption-weight);
  min-height: 45px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.bottom-meta {
  margin-top: 10px;
}

.date {
  display: block;
  margin: 0 0 9px;
  color: #a3aeb8;
  font-size: var(--font-caption-size);
  line-height: var(--font-caption-line);
  font-weight: var(--font-caption-weight);
}

.bottom-action-btn {
  width: 100%;
  height: 40px;
  border: 0;
  border-radius: 11px;
  background: #3138c8;
  color: #ffffff;
  font-size: 14px;
  line-height: 1;
  font-weight: 700;
  cursor: pointer;
}

@keyframes heart-quarter-turn {
  0% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(90deg);
  }
  50% {
    transform: rotate(180deg);
  }
  75% {
    transform: rotate(270deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 480px) {
  .post-card {
    min-height: auto;
  }

  .media {
    aspect-ratio: 264 / 404;
  }
}
</style>
