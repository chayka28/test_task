<template>
  <article class="mobile-card">
    <div class="media">
      <img src="/assets/figma/feed-card-image.png" alt="" class="media-image" />

      <div class="media-header">
        <div class="tags">
          <span class="tag">
            <img src="/assets/icons/Vector.png" alt="" />
            <span>Reels</span>
          </span>
          <span class="tag">
            <img src="/assets/icons/Vector-15.png" alt="" />
            <span>X{{ activityMultiplier }}</span>
          </span>
        </div>

        <div class="actions">
          <span class="action"><img src="/assets/icons/heart-outline.png" alt="" /></span>
          <span class="action"><img src="/assets/icons/Vector-10.png" alt="" /></span>
        </div>
      </div>

      <div class="stats">
        <div class="cell">
          <img src="/assets/icons/Vector-14.png" alt="" />
          <span>{{ metrics.views }}</span>
        </div>
        <div class="cell">
          <img src="/assets/icons/Vector-11.png" alt="" />
          <span>{{ metrics.likes }}</span>
        </div>
        <div class="cell">
          <img src="/assets/icons/Vector-4.png" alt="" />
          <span>{{ metrics.comments }}</span>
        </div>
        <div class="cell">
          <img src="/assets/icons/Vector-3.png" alt="" />
          <span>{{ metrics.shares }}</span>
        </div>
      </div>
    </div>

    <div class="author-row">
      <img src="/assets/avatar-feed.png" alt="" class="avatar" />
      <div class="author-meta">
        <p class="name">{{ handle }}</p>
        <p class="subs">{{ followers }}</p>
      </div>
      <img src="/assets/icons/Vector-5.png" alt="" class="tool" />
    </div>

    <p class="title">{{ sourcePost.title }}</p>
    <p class="description">{{ previewText }}</p>
    <time class="date">{{ formattedCreatedAt }}</time>
    <button type="button" class="action-btn">Анализ</button>
  </article>
</template>

<script setup>
import { computed } from "vue";

import { buildFollowers, buildHandle, buildPostMetrics } from "../services/postPresentation";

const props = defineProps({
  post: {
    type: Object,
    default: null,
  },
});

const sourcePost = computed(() => {
  return (
    props.post || {
      id: 1,
      user_id: 1,
      title: "Разбор ролика: почему это видео зашло",
      text: "500 000 лайков на ютубе делаем, разберем механику удержания и лид-магнит.",
      created_at: new Date().toISOString(),
    }
  );
});

const metrics = computed(() => buildPostMetrics(sourcePost.value.id));
const handle = computed(() => buildHandle(sourcePost.value.user_id));
const followers = computed(() => buildFollowers(sourcePost.value.user_id));
const activityMultiplier = computed(() => ((sourcePost.value.id % 12) + 3).toString());

const previewText = computed(() => {
  const raw = sourcePost.value.text || "";
  if (raw.length <= 68) return raw;
  return `${raw.slice(0, 68)}...`;
});

const formattedCreatedAt = computed(() => {
  const date = new Date(sourcePost.value.created_at);
  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  }).format(date);
});
</script>

<style scoped>
.mobile-card {
  width: 262px;
  border-radius: 16px;
  background: #ffffff;
  padding: 4px 4px 8px;
}

.media {
  width: 254px;
  height: 400px;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
}

.media-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.media-header {
  position: absolute;
  inset: 12px 12px auto;
  display: flex;
  justify-content: space-between;
}

.tags {
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
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
  padding: 4px 8px;
}

.tag img {
  width: 16px;
  height: 16px;
}

.actions {
  display: grid;
  gap: 8px;
}

.action {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  display: grid;
  place-items: center;
}

.action img {
  width: 20px;
  height: 20px;
}

.stats {
  position: absolute;
  left: 12px;
  right: 12px;
  bottom: 8px;
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(4px);
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  padding: 8px 4px;
}

.cell {
  display: grid;
  justify-items: center;
  gap: 4px;
  color: #ffffff;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
}

.cell img {
  width: 20px;
  height: 20px;
}

.author-row {
  margin-top: 4px;
  padding: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.name {
  margin: 0;
  color: #2b31b3;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.1px;
  font-weight: 600;
}

.subs {
  margin: 0;
  color: #4e616b;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.4px;
}

.tool {
  margin-left: auto;
  width: 24px;
  height: 24px;
}

.title {
  margin: 0;
  padding: 0 4px;
  color: #25303d;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
  font-weight: 600;
}

.description {
  margin: 2px 0 0;
  padding: 0 4px;
  min-height: 44px;
  color: #4e616b;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
}

.date {
  display: block;
  margin-top: 4px;
  padding: 0 4px;
  color: #a0adb4;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
}

.action-btn {
  margin: 8px 4px 0;
  width: calc(100% - 8px);
  height: 40px;
  border: 0;
  border-radius: 12px;
  background: #2b31b3;
  color: #ffffff;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.4px;
  font-weight: 600;
}
</style>
