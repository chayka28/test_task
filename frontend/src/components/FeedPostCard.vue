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

        <div class="media-header">
          <div class="tags">
            <span class="tag-pill">
              <img src="/assets/icons/Vector.png" alt="" />
              <span>Reels</span>
            </span>
            <span class="tag-pill">
              <img src="/assets/icons/Vector-15.png" alt="" />
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
              <img src="/assets/icons/heart-outline.png" alt="" />
            </button>

            <button type="button" class="action-pill external-btn" @click.stop="handleRestrictedAction('Открыть источник')">
              <span>↗</span>
            </button>
          </div>
        </div>

        <div class="stats-overlay">
          <div class="stat-cell">
            <img src="/assets/icons/Vector-14.png" alt="" />
            <span>{{ metrics.views }}</span>
          </div>
          <div class="stat-cell">
            <img src="/assets/icons/Vector-11.png" alt="" />
            <span>{{ metrics.likes }}</span>
          </div>
          <div class="stat-cell">
            <img src="/assets/icons/Vector-4.png" alt="" />
            <span>{{ metrics.comments }}</span>
          </div>
          <div class="stat-cell">
            <img src="/assets/icons/Vector-3.png" alt="" />
            <span>{{ metrics.shares }}</span>
          </div>
        </div>
      </div>

      <div class="author-card">
        <AppAvatar :seed="post.id" :size="40" alt="Креатор" :blurred="true" />
        <div class="author-meta">
          <p class="author-name">{{ handle }}</p>
          <p class="author-sub">{{ followers }}</p>
        </div>
        <button type="button" class="author-tool-btn" @click.stop="handleRestrictedAction('Инструменты карточки')">
          <img src="/assets/icons/Vector-5.png" alt="" class="author-tool" />
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
import { buildFollowers, buildHandle, buildMediaPalette, buildPostMetrics } from "../services/postPresentation";

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
});

const emit = defineEmits(["open", "toggle-like", "placeholder", "auth-required"]);

const isLikeAnimating = ref(false);
let likeAnimationTimerId = null;

const metrics = computed(() => buildPostMetrics(props.post.id));
const handle = computed(() => buildHandle(props.post.user_id));
const followers = computed(() => buildFollowers(props.post.user_id));
const activityMultiplier = computed(() => ((props.post.id % 12) + 3).toString());

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
  if (raw.length <= 78) return raw;
  return `${raw.slice(0, 78)}...`;
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
    }, 720);
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
  width: 220px;
  min-height: 520px;
  border-radius: 16px;
  background: #ffffff;
  padding: 0 0 10px;
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
  height: 344px;
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
  filter: saturate(0.95) contrast(1.02);
  opacity: 0.9;
}

.media-glow {
  position: absolute;
  border-radius: 999px;
  filter: blur(12px);
  opacity: 0.9;
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

.media-header {
  position: absolute;
  inset: 12px 12px auto 12px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.tags {
  display: grid;
  gap: 6px;
}

.tag-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  padding: 4px 8px;
  color: #ffffff;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
  font-weight: 500;
}

.tag-pill img {
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
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  display: grid;
  place-items: center;
  border: 0;
  color: #ffffff;
  cursor: pointer;
}

.action-pill img {
  width: 20px;
  height: 20px;
  object-fit: contain;
}

.like-btn img {
  filter: brightness(0) invert(1);
  transition: filter 0.16s ease;
  transform-origin: center;
}

.like-btn.is-liked img {
  filter: invert(16%) sepia(92%) saturate(7042%) hue-rotate(349deg) brightness(103%) contrast(95%);
}

.like-btn.is-animating img {
  filter: brightness(0) invert(1);
  animation: heart-quarter-turn 0.72s linear forwards;
}

.external-btn span {
  font-size: 22px;
  line-height: 1;
  transform: translateY(-1px);
}

.stats-overlay {
  position: absolute;
  left: 12px;
  right: 12px;
  bottom: 8px;
  border-radius: 12px;
  background: var(--media-surface);
  backdrop-filter: blur(10px);
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  padding: 8px 4px;
}

.stat-cell {
  display: grid;
  justify-items: center;
  gap: 4px;
  color: #ffffff;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
  font-weight: 500;
}

.stat-cell img {
  width: 20px;
  height: 20px;
  object-fit: contain;
}

.author-card {
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
}

.author-meta {
  min-width: 0;
}

.author-name {
  margin: 0;
  color: #2b31b3;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.1px;
  font-weight: 600;
}

.author-sub {
  margin: 0;
  color: #4e616b;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.4px;
  font-weight: 500;
}

.author-tool-btn {
  margin-left: auto;
  border: 0;
  background: transparent;
  padding: 0;
  cursor: pointer;
}

.author-tool {
  width: 24px;
  height: 24px;
}

.title {
  margin: 2px 0 1px;
  color: #25303d;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
  font-weight: 600;
  min-height: 29px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.text {
  margin: 0;
  color: #4e616b;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
  font-weight: 500;
  min-height: 44px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.bottom-meta {
  margin-top: 8px;
}

.date {
  display: block;
  margin: 0 0 8px;
  color: #a0adb4;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
  font-weight: 500;
}

.bottom-action-btn {
  width: 100%;
  height: 40px;
  border: 0;
  border-radius: 12px;
  background: #2b31b3;
  color: #ffffff;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.4px;
  font-weight: 600;
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

@media (max-width: 840px) {
  .post-card {
    width: 262px;
  }

  .media {
    height: 400px;
  }
}
</style>
