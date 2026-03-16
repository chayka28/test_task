<template>
  <article class="post-card">
    <div class="top-meta">
      <time class="date">{{ formattedCreatedAt }}</time>
      <button type="button" class="top-action-btn" @click="$emit('open', post)">Анализ</button>
    </div>

    <button type="button" class="card-hitbox" @click="$emit('open', post)">
      <div class="media">
        <img src="/assets/figma/feed-card-image.png" alt="" class="media-image" />

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
              :class="{
                'is-liked': liked,
                'is-animating': isLikeAnimating,
              }"
              @click.stop="handleLikeClick"
            >
              <img src="/assets/icons/heart-outline.png" alt="" />
            </button>
            <span class="action-pill">
              <img src="/assets/icons/Vector-10.png" alt="" />
            </span>
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
        <img src="/assets/avatar-feed.png" alt="" class="avatar" />
        <div class="author-meta">
          <p class="author-name">{{ handle }}</p>
          <p class="author-sub">{{ followers }}</p>
        </div>
        <img src="/assets/icons/Vector-5.png" alt="" class="author-tool" />
      </div>

      <p class="title">{{ post.title }}</p>
      <p class="text">{{ previewText }}</p>
    </button>
  </article>
</template>

<script setup>
import { computed, ref } from "vue";

import { buildFollowers, buildHandle, buildPostMetrics } from "../services/postPresentation";

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
  liked: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["open", "toggle-like"]);
const isLikeAnimating = ref(false);

const metrics = computed(() => buildPostMetrics(props.post.id));
const handle = computed(() => buildHandle(props.post.user_id));
const followers = computed(() => buildFollowers(props.post.user_id));
const activityMultiplier = computed(() => ((props.post.id % 12) + 3).toString());

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

function handleLikeClick() {
  if (!props.liked) {
    isLikeAnimating.value = true;
    window.setTimeout(() => {
      isLikeAnimating.value = false;
    }, 420);
  }

  emit("toggle-like", props.post.id);
}
</script>

<style scoped>
.post-card {
  width: 220px;
  min-height: 520px;
  border-radius: 16px;
  background: #ffffff;
  padding: 0 0 10px;
}

.top-meta {
  padding: 0 2px 10px;
}

.card-hitbox {
  border: 0;
  background: transparent;
  width: 100%;
  padding: 0;
  text-align: left;
  cursor: pointer;
}

.date {
  display: block;
  margin: 0;
  color: #a0adb4;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
  font-weight: 500;
}

.top-action-btn {
  margin-top: 8px;
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

.media {
  position: relative;
  width: 100%;
  height: 344px;
  border-radius: 16px;
  overflow: hidden;
}

.media-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
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
}

.action-pill img {
  width: 20px;
  height: 20px;
  object-fit: contain;
}

.like-btn {
  border: 0;
  cursor: pointer;
  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.like-btn img {
  filter: brightness(0) invert(1);
  transition: filter 0.25s ease;
}

.like-btn.is-liked img {
  filter: invert(17%) sepia(83%) saturate(4100%) hue-rotate(338deg) brightness(105%) contrast(103%);
}

.like-btn.is-animating {
  animation: like-spin 0.42s ease;
}

.stats-overlay {
  position: absolute;
  left: 12px;
  right: 12px;
  bottom: 8px;
  border-radius: 12px;
  background: rgba(47, 14, 14, 0.34);
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

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
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

.author-tool {
  margin-left: auto;
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

@keyframes like-spin {
  0% {
    transform: rotate(0deg) scale(1);
  }

  50% {
    transform: rotate(90deg) scale(1.14);
  }

  100% {
    transform: rotate(0deg) scale(1);
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
